from src import exceptions
from src.renderorder import RenderOrder
import random


class Action:
    """ The template for a game action that affects gameplay."""
    def __init__(self, entity):
        super().__init__()
        self.entity = entity
        self.msg = ''

    @property
    def engine(self):
        """Return the engine this action belongs to."""
        return self.entity.gamemap.engine

    def perform(self):
        """ Perform this action with the objects needed to determine its scope.

            `self.engine` is the scope this action is being performed in.
            `self.entity` is the object performing the action.

            This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class ActionWithDirection(Action):
    def __init__(self, entity, dx, dy):
        super().__init__(entity)
        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self):
        """Returns this actions destination as Tuple[int, int]."""
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self):
        """Return the blocking entity at this actions destination.."""
        # return self.engine.game_map.blocking_entity_at(*self.dest_xy)
        # TODO: Make sure this doesn't breakstuff!
        return self.entity.gamemap.blocking_entity_at(*self.dest_xy)

    @property
    def target_actor(self):
        """Return the actor at this actions destination."""
        # return self.engine.game_map.get_actor_at(*self.dest_xy)
        # TODO: Make sure this doesn't breakstuff!
        return self.entity.gamemap.get_actor_at(*self.dest_xy)

    def perform(self):
        raise NotImplementedError()


class BumpAction(ActionWithDirection):
    """ When acting in a direction, decides which class, between MeleeAction and
        MovementAction to return.
    """
    def perform(self):
        if self.target_actor:
            return MeleeAction(self.entity, self.dx, self.dy)

        else:
            return MovementAction(self.entity, self.dx, self.dy)


class ItemAction(Action):
    def __init__(self, entity, item, target_xy=None):
        super().__init__(entity)
        self.item = item
        if not target_xy:
            target_xy = entity.x, entity.y
        self.target_xy = target_xy

    @property
    def target_actor(self):
        """Return the actor at this actions destination."""
        # return self.engine.game_map.get_actor_at(*self.target_xy)
        return self.entity.gamemap.get_actor_at(*self.target_xy)

    def perform(self):
        """Invoke the items ability, this action will be given to provide context."""
        if self.item.consumable:
            # TODO: Get msg
            self.item.consumable.activate(self)


class DropItem(ItemAction):
    def perform(self):
        """ Removes an item from an entity's inventory and places it on the
            current game map, at the entity's coordinates.
        """
        # If the item is an equipped item, first unequip it.
        if self.entity.equipment.item_is_equipped(self.item):
            self.entity.equipment.toggle_equip(self.item)

        # Remove it from inventory
        result = self.entity.inventory.rm_item(self.item)

        if result:
            # Put it on the map
            # self.item.place(self.entity.x, self.entity.y, self.entity.gamemap)

            self.entity.gamemap.entities.add(self.item)
            self.item.x = self.entity.x
            self.item.y = self.entity.y

            self.msg = f"You dropped the {self.item.name}."
        else:
            raise exceptions.Impossible("You cannot drop an item you do not have!")


class EquipAction(Action):
    def __init__(self, entity, item):
        super().__init__(entity)
        self.item = item

    def perform(self):
        self.msg = self.entity.equipment.toggle_equip(self.item)


class MeleeAction(ActionWithDirection):
    def __init__(self, entity, dx, dy):
        super().__init__(entity, dx, dy)
        # Determine if the entity will hit or miss the target entity.
        # The entity will roll a 20 sided die, and try to get below a target number.
        self.target_base = 10
        self.die = 20

    def perform(self):
        target = self.target_actor
        if not target:
            raise exceptions.Impossible("Nothing to attack!")

        # Setup for the attack descriptions
        entity = self.entity.name.capitalize()
        target_number = self.calc_target_number(target)

        if self.roll_hit_die() < self.calc_target_number(target):
            # It's a hit!
            result = 0
            # Calculate the damage
            if self.entity.equipment.weapon:
                dmg = self.hit_with_weapon(target)
            else:
                dmg = self.hit_with_barehands(target)

            target.fighter.hp -= dmg

            # Check if the target is dead...
            if target.fighter.is_dead():
                return DieAction(entity=target, cause=self.entity)

        else:
            self.miss(target)

    def calc_target_number(self, target):
        return self.target_base + target.fighter.ac + target.level.current_level

    def roll_hit_die(self):
        # Rolls a 1d20 die to determine if the attacker will land the hit.
        return random.randint(1, self.die)

    def hit_with_weapon(self, target):
        # Get the damage from the weapon
        weapon = self.entity.equipment.weapon
        dmg = weapon.equippable.attack.roll_dmg()
        # atk_text = self.entity.fighter.attacks.description
        self.msg = f"The {self.entity} hits the {target.name} with a {weapon.name} for {dmg}! "

        # TODO Case where we hit something
        # TODO Case where something hits us

        return dmg

    def hit_with_barehands(self, target):
        # We'll use the entities "natural" attack, or Bare-Handed for our Hero.
        dmg = self.entity.fighter.attacks.roll_dmg()
        self.msg = f"The {self.entity} hits the {target.name} for {dmg}! "

        # TODO Case where we hit something
        # TODO Case where something hits us
        return dmg

    def miss(self, target):
        self.msg = f"The {self.entity.name.capitalize()} misses the {target.name}. "
        # TODO Add "Wildly misses"


class MovementAction(ActionWithDirection):
    """ Moves an entity to a new set of coordinates."""

    def perform(self):
        dest_x, dest_y = self.dest_xy

        if not self.entity.gamemap.in_bounds(dest_x, dest_y):
            # Destination is out of bounds.
            raise exceptions.Impossible("That way is out of bounds!")

        if not self.entity.gamemap.tiles["walkable"][dest_x, dest_y]:
            # Destination is blocked by a tile.
            raise exceptions.Impossible("That way is not walkable!")

        # Theoretically, this bit of code won’t ever trigger, but it's a
        # safeguard.
        if self.entity.gamemap.blocking_entity_at(dest_x, dest_y):
            # Destination is blocked by an entity.
            raise exceptions.Impossible("That way is blocked.")

        self.entity.move(self.dx, self.dy)


class PickupAction(Action):
    """Pickup an item and add it to the inventory, if there is room for it."""
    def __init__(self, entity):
        super().__init__(entity)

    def perform(self):
        # TODO: Support for piles
        # TODO: Pickup menu handler

        actor_location_x = self.entity.x
        actor_location_y = self.entity.y
        inventory = self.entity.inventory

        for item in self.entity.gamemap.items:
            if actor_location_x == item.x and actor_location_y == item.y:
                if len(inventory.items) >= inventory.capacity:
                    raise exceptions.Impossible("Your inventory is full.")

                self.entity.gamemap.entities.remove(item)
                item.parent = self.entity.inventory
                inventory.add_item(item)
                self.msg = f"You picked up the {item.name}. "
                return

        raise exceptions.Impossible("There is nothing here to pick up.")


class TakeStairsAction(Action):
    def perform(self):
        """ Take the stairs, if any exist at the entity's location. """
        if (self.entity.x, self.entity.y) == self.engine.game_map.downstairs_location:
            self.engine.game_world.generate_floor()

            self.msg = "You descend the staircase."
        else:
            raise exceptions.Impossible("There are no stairs here.")


class WaitAction(Action):
    # Entity does nothing this turn
    def perform(self) -> None:
        pass


class DieAction(Action):
    def __init__(self, entity, cause):
        super().__init__(entity)
        self.cause = cause

    def perform(self):
        # TODO: What if the cause is a non-actor? Trap, drowning, bomb, etc.

        # if self.entity == self.engine.player:
        if self.entity.name == "Player":
            self.msg = "You died!"
        elif self.cause.name == "Player":
            self.msg = f"You kill the {self.entity.name}!"

            # You get xp for the kill
            self.cause.level.add_xp(self.entity.level.xp_given)
        else:
            self.msg = f"The {self.cause.name} kills the {self.entity.name}!"

            # The causing entity gets xp for the kill
            self.cause.level.add_xp(self.entity.level.xp_given)

        # Kill the entity
        self.entity.char = "%"
        self.entity.color = (191, 0, 0)
        self.entity.blocks_movement = False
        self.entity.ai = None
        self.entity.name = f"{self.entity.name} corpse"
        self.entity.render_order = RenderOrder.CORPSE

