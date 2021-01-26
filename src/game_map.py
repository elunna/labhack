from . import tile_types
from .item import Item
from .actor import Actor
import numpy as np


class GameMap:
    """ Defines the dimensions and tiles of a single map in the game. """
    def __init__(self, engine, width, height, entities=()):
        self.engine = engine
        self.width, self.height = width, height
        self.entities = set(entities)

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

        self.downstairs_location = (0, 0)

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
            if isinstance(entity, Actor)
        )

    @property
    def items(self):
        yield from (entity for entity in self.entities if isinstance(entity, Item))

    def get_blocking_entity_at_location(self, location_x, location_y):
        for entity in self.entities:
            if (
                    entity.blocks_movement
                    and entity.x == location_x
                    and entity.y == location_y
            ):
                return entity

        return None

    def get_actor_at_location(self, x, y):
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor

        return None

    def in_bounds(self, x, y):
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height
