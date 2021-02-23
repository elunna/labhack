from src import settings
from . import procgen


class GameWorld:
    """ Holds the settings for the GameMap, and generates new maps when moving down the stairs.
    """
    def __init__(self, engine):
        self.engine = engine
        self.current_floor = 0

    def generate_floor(self):
        # Generate new map each time we go down a floor.
        self.current_floor += 1

        new_map = procgen.generate_map(
            max_rooms=settings.max_rooms,
            room_min_size=settings.room_min_size,
            room_max_size=settings.room_max_size,
            map_width=settings.map_width,
            map_height=settings.map_height,
            max_distance=50,
            engine=self.engine
        )

        self.engine.game_map = new_map

        # Add player
        player = self.engine.player
        new_map.entities.add(player)
        new_map.player = player

        # Place player on upstair.
        player.place(*new_map.upstairs_location, new_map)

        # Place entities, items, etc.
        procgen.populate_map(new_map, self.engine)
