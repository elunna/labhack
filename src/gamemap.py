import random

from . import actor, settings
from . import item
from . import tiles
from .entity import Entity
from .entity_manager import EntityManager
from .room import Room
import numpy as np

# TODO: Clean up query functions
# TODO: Get entities at... with filters - and the others use it.


class GameMap(EntityManager):
    """ Defines the dimensions and tiles of a single map in the game. """
    def __init__(self, width, height, fill_tile=tiles.wall):
        super().__init__()
        self.engine = None  # This can be set later if needed
        self.width, self.height = width, height
        self.rooms = []  # Start with an empty list of rooms.
        self.doors = []  # Empty list of doors, helps in map generation.
        self.downstairs_location = (-1, -1)
        self.upstairs_location = (-1, -1)
        self.room_coords = None

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



    def get_trap_at(self, x, y):
        traps = self.filter("trap", x=x, y=y)
        if traps:
            return traps.pop()
        return None

    def in_bounds(self, x, y):
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

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
        # Filter out hidden
        entities = [e for e in self.filter(x=x, y=y) if "hidden" not in e]
        names = ", ".join(e.name for e in entities)
        return names.capitalize()

    def walkable(self, x, y):
        return self.tiles["walkable"][x, y]

    def room_coordinates(self):
        """ Creates a dict of coordinate keys and room values so we have an easy reference
            to see what coordinates belong to a room - and a quick check to see if they don't.
        """
        return {p: r for r in self.rooms for p in r.all_coords()}

    @staticmethod
    def tiles_around(x, y, radius):
        length = (radius * 2) + 1
        # Create a helper Rect so we can use it's perimeter.
        temp_rect = Room(x - radius, y - radius, length, length)
        return temp_rect.perimeter()

    def valid_door_neighbors(self, room, x, y):
        """ Checks if the tiles around the point allow for placing a door (and more importantly, a closet)
            If valid, returns the coordinates for the closet space outside the door.
        """
        # First obvious check that the door will occupy part of the perimeter (but not a corner)
        if not room.valid_door_loc(x, y):
            return False

        facing = room.direction_facing(x, y)

        # Is it flanked by room walls to east and west (if facing north or south)?
        if facing in ['N', 'S']:
            # east
            dx, dy = settings.CARDINAL_DIR['E']
            if self.tiles[x + dx][y + dy] not in tiles.room_walls:
                return False
            # west
            dx, dy = settings.CARDINAL_DIR['W']
            if self.tiles[x + dx][y + dy] not in tiles.room_walls:
                return False

        # Is it flanked by room walls to north and south (if facing east or west)?
        elif facing in ['E', 'W']:
            # north
            dx, dy = settings.CARDINAL_DIR['N']
            if self.tiles[x + dx][y + dy] not in tiles.room_walls:
                return False
            # south
            dx, dy = settings.CARDINAL_DIR['S']
            if self.tiles[x + dx][y + dy] not in tiles.room_walls:
                return False
        """
        for direction in settings.CARDINAL_DIR.values():
            dx, dy = direction

            # Check around for other doors.
            if new_map.tiles[d.x + dx][d.y + dy] == tiles.door:
                # Oh no, a door is adjacent! Abort mission!
                valid_door = False
                continue
        """
        # Does it have a "closet" space outside directly outside of the door that is not part of another room?
        dx, dy = settings.CARDINAL_DIR[facing]
        closet_x, closet_y = x + dx, y + dy

        # Is this a valid tile?
        if not self.in_bounds(closet_x, closet_y):
            return False

        # Is it wall or floor (both are valid)
        if not self.tiles[closet_x][closet_y] in [tiles.wall, tiles.floor]:
            return False

        return True

    def get_nearest_unconnected_room(self, room):
        # Use tiles_around to look for a tiles that belong to rooms.
        # Keep pushing outward until we find a room that is not connected to this room.
        x, y = room.center

        min_radius = 3  # Required to create the minimum sized Rect.

        for r in range(min_radius, self.height):
            # Get all the tiles in the new radius
            surrounding_tiles = self.tiles_around(x, y, r)

            for st in surrounding_tiles:
                # Check each tile and see if it belongs to a room.
                result = self.room_coords.get(st)
                if not result:
                    continue
                # Make sure it's not the same room we are looking out from.
                if room.label == result.label:
                    continue
                # Make sure it's not connected to this room already.
                if result.label in room.connections:
                    continue

                # Passed all checks!
                return result

    def on_edge_of_map(self, x, y):
        """ Checks if a coordinate is on the edge of the map perimeter.
        returns True if it is, False otherwise.
        """
        if x == 0 or y == 0:
            return True
        elif x == (self.width - 1) or y == (self.height - 1):
            return True

        return False

    def get_random_unoccupied_tile(self):
        # Get every walkable tile, choose a random one until one is found.
        floors = [(x, y) for x in range(self.width)
                  for y in range(self.height) if self.walkable(x, y)]

        while floors:
            result = random.choice(floors)
            if not self.get_actor_at(*result):
                return result
            floors.remove(result)
        return None
