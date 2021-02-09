from actions.actions import ActionWithDirection
from src import exceptions


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