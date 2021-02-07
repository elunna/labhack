from src import color
from src import exceptions
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
        return self.engine.game_map.blocking_entity_at(*self.dest_xy)

    @property
    def target_actor(self):
        """Return the actor at this actions destination."""
        return self.engine.game_map.get_actor_at(*self.dest_xy)

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
        return self.engine.game_map.get_actor_at(*self.target_xy)

    def perform(self):
        """Invoke the items ability, this action will be given to provide context."""
        if self.item.consumable:
            # TODO: Get msg
            self.item.consumable.activate(self)


class DropItem(ItemAction):
    def perform(self):
        """Drop an item from an entity's possession."""
        # If the item is an equipped item, first unequip it.
        if self.entity.equipment.item_is_equipped(self.item):
            self.entity.equipment.toggle_equip(self.item)

        # TODO: Get msg
        self.entity.inventory.drop(self.item)


class EquipAction(Action):
    def __init__(self, entity, item):
        super().__init__(entity)
        self.item = item

    def perform(self):
        # TODO: Get msg
        self.msg = self.entity.equipment.toggle_equip(self.item)


class MeleeAction(ActionWithDirection):
    def perform(self):
        target = self.target_actor
        if not target:
            raise exceptions.Impossible("Nothing to attack!")

        die = 20
        target_base = 10
        target_number = target_base + target.fighter.ac + target.level.current_level
        roll = random.randint(1, die)

        if roll < target_number:
            # It's a HIT!
            dmg = self.entity.fighter.power
            attack_desc = f"The {self.entity.name.capitalize()} hits the {target.name} for {dmg}! "
            result = target.fighter.take_dmg(dmg)
            self.msg = attack_desc + result
        else:
            self.msg = f"The {self.entity.name.capitalize()} misses the {target.name}."


class MovementAction(ActionWithDirection):
    """ Moves an entity to a new set of coordinates."""

    def perform(self):
        dest_x, dest_y = self.dest_xy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            # Destination is out of bounds.
            raise exceptions.Impossible("That way is blocked.")

        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            # Destination is blocked by a tile.
            raise exceptions.Impossible("That way is blocked.")

        # Theoretically, this bit of code won’t ever trigger, but it's a
        # safeguard.
        if self.engine.game_map.blocking_entity_at(dest_x, dest_y):
            # Destination is blocked by an entity.
            raise exceptions.Impossible("That way is blocked.")

        self.entity.move(self.dx, self.dy)


class PickupAction(Action):
    """Pickup an item and add it to the inventory, if there is room for it."""
    def __init__(self, entity):
        super().__init__(entity)

    def perform(self):
        actor_location_x = self.entity.x
        actor_location_y = self.entity.y
        inventory = self.entity.inventory

        for item in self.engine.game_map.items:
            if actor_location_x == item.x and actor_location_y == item.y:
                if len(inventory.items) >= inventory.capacity:
                    raise exceptions.Impossible("Your inventory is full.")


                self.engine.game_map.entities.remove(item)
                item.parent = self.entity.inventory
                inventory.add_item(item)
                self.msg = f"You picked up the {item.name}!"
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
