import actors
import items
import logger
import numpy as np
import tile_types

log = logger.get_logger(__name__)


class GameMap:
    """ Defines the dimensions and tiles of a single map in the game. """
    def __init__(self, width, height, entities=(), engine=None):
        log.debug(f'Initializing new GameMap: width={width} height={height}')

        self.width, self.height = width, height
        self.entities = set(entities)
        self.downstairs_location = (0, 0)
        self.upstairs_location = (0, 0)
        self.engine = engine

        # create a 2D array, filled with the same values: walls.
        self.tiles = np.full(
            (width, height),
            fill_value=tile_types.wall,
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
        # TODO: What is the purpose of this?
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

    # TODO: Rename to get_blocker_at
    def get_blocking_entity_at_location(self, location_x, location_y):
        for entity in self.entities:
            if (
                    entity.blocks_movement
                    and entity.x == location_x
                    and entity.y == location_y
            ):
                return entity

        return None

    # TODO: Rename to get_actor_at
    def get_actor_at_location(self, x, y):
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor

        return None

    def in_bounds(self, x, y):
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height


    def walkable(self, x, y):
        return self.tiles["walkable"][x, y]
