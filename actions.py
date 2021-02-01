import exceptions
import logger

log = logger.get_logger(__name__)


class Action:
    """ The template for a game action that affects gameplay."""

    def __init__(self, entity):
        super().__init__()
        self.entity = entity

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
        return self.engine.game_map.get_blocking_entity_at_location(*self.dest_xy)

    @property
    def target_actor(self):
        """Return the actor at this actions destination."""
        return self.engine.game_map.get_actor_at_location(*self.dest_xy)

    def perform(self):
        raise NotImplementedError()


class BumpAction(ActionWithDirection):
    """ When acting in a direction, decides which class, between MeleeAction and
        MovementAction to return.
    """

    def perform(self):
        log.debug(f'{self.entity.name}: BumpAction ({self.dx},{self.dy})')

        if self.target_actor:
            return MeleeAction(self.entity, self.dx, self.dy).perform()

        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()


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
        return self.engine.game_map.get_actor_at_location(*self.target_xy)

    def perform(self):
        """Invoke the items ability, this action will be given to provide context."""
        log.debug(f'{self.item.name} has been invoked')
        if self.item.consumable:
            self.item.consumable.activate(self)


class DropItem(ItemAction):
    def perform(self):
        """Drop an item from an entity's possession."""
        # If the item is an equipped item, first unequip it.
        if self.entity.equipment.item_is_equipped(self.item):
            log.debug(f'{self.item.name} is being unequipped before dropping..')
            self.entity.equipment.toggle_equip(self.item)

        log.debug(f'{self.entity.name} drops the {self.item.name}.')
        self.entity.inventory.drop(self.item)


class EquipAction(Action):
    def __init__(self, entity, item):
        super().__init__(entity)
        self.item = item

    def perform(self):
        log.debug(f'{self.entity.name} is having its equip status being toggled.')
        self.entity.equipment.toggle_equip(self.item)


class MeleeAction(ActionWithDirection):
    def perform(self):
        target = self.target_actor

        if not target:
            raise exceptions.Impossible("Nothing to attack!")
        elif self.target_actor == self.entity:
            log.debug(f'{self.entity.name} targeted a MeleeAction at itself.')
            self.engine.msg_log.add_message(
                f"The {self.entity.name} mutters angrily to itself...",
            )
            return WaitAction(self.entity)

        damage = self.entity.fighter.power - target.fighter.defense
        attack_desc = f"The {self.entity.name.capitalize()} hits the {target.name}"

        if damage > 0:
            target.fighter.hp -= damage
        else:
            attack_desc += "... but does no damage!"

        self.engine.msg_log.add_message(attack_desc)


class MovementAction(ActionWithDirection):
    """ Moves an entity to a new set of coordinates."""
    def perform(self):
        dest_x, dest_y = self.dest_xy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            # Destination is out of bounds.
            raise exceptions.Impossible("That way is blocked.")

        if not self.engine.game_map.walkable(dest_x, dest_y):

            # TODO: Find a better place for this import, at the top it causes a circular import....
            from components.ai import ConfusedAI

            # Destination is blocked by a tile
            if isinstance(self.entity.ai, ConfusedAI):
                if self.entity == self.engine.player:
                    self.engine.msg_log.add_message(f"You bonk into the wall...")
                else:
                    self.engine.msg_log.add_message(f"The {self.entity.name} bonks into the wall...")
                return

            raise exceptions.Impossible("That way is blocked.")

        # Theoretically, this bit of code won’t ever trigger, but it's a
        # safeguard.
        if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            # Destination is blocked by an entity.
            raise exceptions.Impossible("That way is blocked.")

        log.debug(f'{self.entity.name} moves {self.dx,self.dy}.')
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
                inventory.items.append(item)

                self.engine.msg_log.add_message(f"You picked up the {item.name}!")
                return

        raise exceptions.Impossible("There is nothing here to pick up.")


class TakeStairsAction(Action):
    def perform(self):
        """ Take the stairs, if any exist at the entity's location. """
        if (self.entity.x, self.entity.y) == self.engine.game_map.downstairs_location:
            self.engine.game_world.generate_floor()
            self.engine.msg_log.add_message(
                "You descend the staircase.",
            )
        else:
            raise exceptions.Impossible("There are no stairs here.")


class WaitAction(Action):
    # Entity does nothing this turn
    def perform(self) -> None:
        pass
