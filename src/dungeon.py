import src.factory
from src import settings
from . import procgen


class Dungeon:
    """ Holds the settings for the GameMap, and generates new maps when moving down the stairs.
    """
    def __init__(self, engine):
        self.engine = engine
        self.map_list = []
        self.current_floor = 0
        self.current_map = None

    def generate_floor(self):
        # Generate new map each time we go down a floor.
        self.current_floor += 1

        # Try a few different templates for variety.
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

        # Place entities, items, etc.
        src.factory.populate_map(new_map, self.engine)

    # set_current_map(level)
    # get_map(int)
    # add_map

    # Branches? Each map should get a code as well as a level depth.