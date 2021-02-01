import actors
import items
import logger
import numpy as np
import tile_types

log = logger.get_logger(__name__)


class GameMap:
    """ Defines the dimensions and tiles of a single map in the game. """
    def __init__(self,
                 width,
                 height,
                 entities=(),
                 engine=None,
                 fill_tile=tile_types.wall):
        log.debug(f'Initializing new GameMap: width={width} height={height}')

        self.width, self.height = width, height
        self.entities = set(entities)
        self.downstairs_location = (0, 0)
        self.upstairs_location = (0, 0)
        self.engine = engine

        # create a 2D array, filled with the same values: walls.
        self.tiles = np.full(
            (width, height),
            fill_value=fill_tile,
            order="F"
        )

        self.visible = np.full(
            (width, height),
            fill_value=False,
            order="F"
        )  # Tiles the player can currently see

        self.explored = np.full(
            (width, height),
            fill_value=False,
            order="F"
        )  # Tiles the player has seen before


    @property
    def gamemap(self):
        return self

    @property
    def actors(self):
        """Iterate over this maps actors."""
        yield from (
            entity
            for entity in self.entities
            # if isinstance(entity, Actor) and entity.is_alive
            if isinstance(entity, actors.Actor)
        )

    @property
    def items(self):
        yield from (entity for entity in self.entities if isinstance(entity, items.Item))

    def get_blocker_at(self, location_x, location_y):
        for entity in self.entities:
            if (
                    entity.blocks_movement
                    and entity.x == location_x
                    and entity.y == location_y
            ):
                return entity

        return None

    def get_actor_at(self, x, y):
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor

        return None

    def in_bounds(self, x, y):
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height


    def walkable(self, x, y):
        return self.tiles["walkable"][x, y]


    def get_names_at_location(self, x, y):
        """ takes “x” and “y” variables, though these represent a spot on the map.
            We first check that the x and y coordinates are within the map, and are
            currently visible to the player. If they are, then we create a string of
            the entity names at that spot, separated by a comma. We then return that
            string, adding capitalize to make sure the first letter in the string is
            capitalized.
        """
        if not self.in_bounds(x, y) or not self.visible[x, y]:
            return ""

        names = ", ".join(
            entity.name for entity in self.entities if entity.x == x and entity.y == y
        )

        return names.capitalize()
