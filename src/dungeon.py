from src import factory, db
from src import settings
from . import procgen


class Dungeon:
    """ Manages the collection of levels in the game, keeps track of the current map,
     and generates new maps when moving down the stairs.
    """
    def __init__(self, engine=None, test_map=None):
        self.engine = engine  # This must be set before generate_floor.

        self.dlevel = 1  # The number of the current floor the player is on.
        self.map_list = []
        self.test_map = test_map  # Just pass a reference to the function.

        # Entity factory
        self.entity_factory = factory.EntityFactory(
            entity_dict=db.actor_dict,
            dungeon=self,
            player=self.engine.player
        )

        # Create a first map for the dungeon
        self.generate_floor()
        self.populate_map(self.dlevel)

        # Set the engine's map ref
        self.engine.game_map = self.current_map

    @property
    def current_map(self):
        """Returns the floor that the player is currently on."""
        if self.map_list:
            return self.map_list[self.dlevel - 1]
        return None

    def generate_floor(self):
        """Generate new map each time we go down a floor. Adds the map to the list of maps and
        returns the created map.
        """
        if self.test_map:
            # Easy way to speed up testing with test maps.
            new_map = self.test_map()  # Generate a new test map each time.
        else:
            new_map = procgen.generate_map(
                max_rooms=settings.max_rooms,
                room_min_size=settings.room_min_size,
                room_max_size=settings.room_max_size,
                map_width=settings.map_width,
                map_height=settings.map_height,
                max_distance=50,
                difficulty=self.dlevel
            )

        # Add map to list
        self.map_list.append(new_map)

        # Add the engine to the map
        new_map.engine = self.engine

        # Return the map for other uses
        return new_map

    def populate_map(self, dlevel):
        """Place entities, items, and actors in a new map."""
        # map_to_populate = self.get_map(dlevel)
        self.entity_factory.populate_level(dlevel)
        # factory.populate_map(map_to_populate, self.dlevel)

    def summon_random_monster(self, player_level):
        """Creates a new monster for the level and places it randomly."""
        map_to_populate = self.get_map(self.dlevel)

        # Create a new monster based on difficulty
        new_monster = self.entity_factory.difficulty_specific_monster(self.dlevel, player_level)
        # Place it at a random open spot in the level.
        x, y = self.current_map.get_random_unoccupied_tile()

        # Spawn the monster to the current level
        factory.spawn(new_monster, self.current_map, x, y)

    def move_downstairs(self, entity):
        """Moves the specified entity downstairs to the next upstair."""
        # Unlatch the player from the old level
        self.current_map.player = None

        # This manages moving an entity between levels
        next_level = self.dlevel + 1

        # We can't move below the levels that exist
        if next_level > len(self.map_list):
            return False

        # Set the player's location to the next level's upstair.
        x, y = self.get_map(next_level).upstairs_location
        self.place_entity(entity, next_level, x, y)

        # Latch the player to the new level
        self.current_map.player = entity

        # Set the engine's map ref
        self.engine.game_map = self.current_map
        return True

    def move_upstairs(self, entity):
        """Moves the specified entity upstairs to the next downstair."""
        # Unlatch the player from the old level
        self.current_map.player = None

        # This manages moving an entity between levels
        next_level = self.dlevel - 1

        # For now, do not allow going upstairs on the top level.
        if next_level <= 0:
            return False

        # Set the player's location to the next level's upstair.
        x, y = self.get_map(next_level).downstairs_location
        self.place_entity(entity, next_level, x, y)

        # Latch the player to the new level
        self.current_map.player = entity

        # Set the engine's map ref
        self.engine.game_map = self.current_map

        return True

    def place_entity(self, entity, map_num, x, y):
        """Places an entity at a map by the map level at a specific x, y coordinate."""
        # Returns True if successful, False otherwise.

        # Remove the entity from current map
        if entity in self.current_map.entities:
            self.current_map.entities.remove(entity)

        # Change the dlevel
        self.set_dlevel(map_num)

        # Add the player to the new map
        self.current_map.entities.add(entity)

        # set the players parent
        entity.parent = self.current_map

        # Change the entity position
        entity.x, entity.y = x, y

    def set_dlevel(self, new_dlevel):
        """Sets the number of the current level.
        Checks that the level number is valid and sets it.
        Returns True if successful, False otherwise.
        """

        if new_dlevel <= 0:
            raise ValueError("Cannot set the dungeon level to 0 or less!")

        elif new_dlevel > len(self.map_list):
            raise ValueError("Cannot set dungeon level greater than the number of levels that exist!")

        if new_dlevel <= len(self.map_list):
            self.dlevel = new_dlevel
            return True

        return False

    def get_map(self, dlevel):
        """Returns the current map."""
        return self.map_list[dlevel - 1]

    # get_map(num)
    # add_map
    # Branches? Each map should get a code as well as a level depth.