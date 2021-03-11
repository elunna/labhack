from actions.actions import ActionWithDirection
from actions.trap_action import TrapAction
from src import exceptions


class MovementAction(ActionWithDirection):
    """ Moves an entity to a new set of coordinates."""

    def perform(self):
        """Attempts to moves the entity a destination coordinate. We conduct a thorough set of checks to
        make sure the move is valid, and then move the entity. If the entity walks into a trap, we return a
        TrapAction for that trap.
        """
        if "trapped" in self.entity.states.states:
            # return WriggleAction(self.entity, self.dx, self.dy)
            raise exceptions.Impossible("Actor is trapped and cannot move!")

        dest_x, dest_y = self.dest_xy

        if not self.entity.gamemap.in_bounds(dest_x, dest_y):
            # Destination is out of bounds.
            raise exceptions.Impossible("That way is out of bounds!")

        if not self.entity.gamemap.walkable(dest_x, dest_y):
            # Destination is blocked by a tile.
            if self.entity.is_player():
                raise exceptions.Impossible("That way is not walkable!")

            # No msg for other monsters
            return

        # Theoretically, this won’t ever trigger, it's a safeguard.
        if self.blocking_entity:
            # Destination is blocked by an entity.
            if self.entity.is_player:
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
        # Reduce the trapped timeout by the direction.
        # Cardinal directions reduce by one, and diagonal directions by 2.
        delta = abs(self.dx) + abs(self.dy)
        self.entity.states.states["trapped"] -= delta
