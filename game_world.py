from procgen import generate_map
import logger
import settings

log = logger.get_logger(__name__)


class GameWorld:
    """ Holds the settings for the GameMap, and generates new maps when moving
        down the stairs.
        This class might be bulky, we'll see if we keep it around or if we merge
        it into Engine...
    """
    def __init__(self, *, engine, current_floor=0):
        log.debug(f'Initializing new GameWorld')

        self.engine = engine
        self.current_floor = current_floor

        # Auto generate the first level
        self.generate_floor()

    def generate_floor(self):
        # Generate new map each time we go down a floor.
        self.current_floor += 1

        new_map = generate_map(
            max_rooms=settings.max_rooms,
            room_min_size=settings.room_min_size,
            room_max_size=settings.room_max_size,
            map_width=settings.map_width,
            map_height=settings.map_height,
            floor_number=self.current_floor,
        )

        # Add the engine to the map.
        new_map.engine = self.engine

        # Set the engine's current map to the new map
        self.engine.game_map = new_map
