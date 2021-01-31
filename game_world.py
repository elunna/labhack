from procgen import generate_dungeon

import logger
import settings
log = logger.get_logger(__name__)

class GameWorld:
    """ Holds the settings for the GameMap, and generates new maps when moving down the stairs.
    """
    def __init__(self, *, engine, current_floor=0):
        log.debug(f'Initializing new GameWorld')

        self.engine = engine
        self.current_floor = current_floor

    def generate_floor(self):
        # Generate new map each time we go down a floor.
        self.current_floor += 1

        self.engine.game_map = generate_dungeon(
            max_rooms=settings.max_rooms,
            room_min_size=settings.room_min_size,
            room_max_size=settings.room_max_size,
            map_width=settings.map_width,
            map_height=settings.map_height,
            engine=self.engine,
        )
