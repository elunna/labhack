from actions.action_with_direction import ActionWithDirection
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
            if self.entity.name == "Player":
                raise exceptions.Impossible("That way is not walkable!")

            # No msg for other monsters
            return

        # Theoretically, this won’t ever trigger, it's a safeguard.
        if self.entity.gamemap.blocking_entity_at(dest_x, dest_y):
            # Destination is blocked by an entity.
            if self.entity.name == "Player":
                raise exceptions.Impossible("That way is blocked.")

            # No msg for other monsters
            return

        self.entity.move(self.dx, self.dy)
