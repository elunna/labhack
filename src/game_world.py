class GameWorld:
    """ Holds the settings for the GameMap, and generates new maps when moving down the stairs.
    """
    def __init__(
            self,
            *,
            engine,
            map_width,
            map_height,
            max_rooms,
            room_min_size,
            room_max_size,
            current_floor=0
    ):
        self.engine = engine
        self.map_width = map_width
        self.map_height = map_height
        self.max_rooms = max_rooms
        self.room_min_size = room_min_size
        self.room_max_size = room_max_size
        self.current_floor = current_floor

    def generate_floor(self):
        # Generate new map each time we go down a floor.
        from .procgen import generate_dungeon

        self.current_floor += 1

        self.engine.game_map = generate_dungeon(
            max_rooms=self.max_rooms,
            room_min_size=self.room_min_size,
            room_max_size=self.room_max_size,
            map_width=self.map_width,
            map_height=self.map_height,
            engine=self.engine,
        )