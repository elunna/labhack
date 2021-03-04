from actions.actions import ActionWithDirection
from actions.trap_action import TrapAction
from src import exceptions


class MovementAction(ActionWithDirection):
    """ Moves an entity to a new set of coordinates."""

    def perform(self):
        dest_x, dest_y = self.dest_xy

        if not self.entity.gamemap.in_bounds(dest_x, dest_y):
            # Destination is out of bounds.
            raise exceptions.Impossible("That way is out of bounds!")

        if not self.entity.gamemap.walkable(dest_x, dest_y):
            # Destination is blocked by a tile.
            # TODO: Update with component type/breed check
            if self.entity.name == "player":
                raise exceptions.Impossible("That way is not walkable!")

            # No msg for other monsters
            return

        # Theoretically, this won’t ever trigger, it's a safeguard.
        if self.blocking_entity:
            # Destination is blocked by an entity.
            # TODO: Update with component type/breed check
            if self.entity.name == "player":
                raise exceptions.Impossible("That way is blocked.")

            # No msg for other monsters
            return

        self.entity.move(self.dx, self.dy)

        # Did we trigger a trap?
        trap = self.entity.gamemap.get_trap_at(dest_x, dest_y)
        if trap:
            # Trigger it
            return TrapAction(self.entity, trap)


class WriggleAction(ActionWithDirection):
    """ Lets an actor wriggle to get out of a trap """
    def perform(self):
        # Reduce the trapped timeout by
        delta = abs(self.dx) + abs(self.dy)
        self.entity.states.states["trapped"] -= delta