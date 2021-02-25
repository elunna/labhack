from src import factory
from src import settings
from . import procgen


class Dungeon:
    """ Holds the settings for the GameMap, and generates new maps when moving down the stairs.
    """
    def __init__(self, engine=None):
        self.map_list = []
        self.dlevel = 0  # The number of the current floor the player is on.
        self.engine = engine

    @property
    def current_map(self):
        # Returns the floor that the player is currently on.
        if self.map_list:
            return self.map_list[self.dlevel - 1]
        return None

    def generate_floor(self):
        # Generate new map each time we go down a floor.
        # Adds the map to the list of maps and returns the created map.

        # Increment the current floor - done in generate map
        self.dlevel += 1

        new_map = procgen.generate_map(
            max_rooms=settings.max_rooms,
            room_min_size=settings.room_min_size,
            room_max_size=settings.room_max_size,
            map_width=settings.map_width,
            map_height=settings.map_height,
            max_distance=50,
        )

        # Place entities, items, etc.
        factory.populate_map(new_map, self.dlevel)

        # Add map to list
        self.map_list.append(new_map)

        # Return the map for other uses
        return new_map

    def move_downstairs(self):
        # Returns True if successful, False otherwise.

        # This manages moving an entity between levels
        player = self.current_map.player

        # Remove the player from current map
        self.current_map.player = None
        self.current_map.entities.remove(player)

        # Do we have a level below us yet?
        if self.dlevel == len(self.map_list):
            # Generate a new level and add it to the map_list
            self.generate_floor()

        # Add the player to the new map
        self.current_map.entities.add(player)
        self.current_map.player = player

        # Set the player's location to the next level's upstair.
        player.x, player.y = self.current_map.upstairs_location

        # set the players parent
        player.parent = self.current_map

        # Add the map to the engine
        self.engine.game_map = self.current_map

        # Add the engine to the map
        self.current_map.engine = self.engine

    def move_upstairs(self):
        pass

    def place_hero(self, level, x, y):
        pass

    # set_dlevel(num)
    # get_map(num)
    # add_map
    # Branches? Each map should get a code as well as a level depth.