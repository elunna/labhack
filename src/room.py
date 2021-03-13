import random
from collections import defaultdict

from src import tiles
from src.door import Door


class Room:
    """Represents a room in a single map."""
    def __init__(self, x, y, width, height):
        if width < 3 or height < 3:
            raise ValueError("Width and height must be at least 3 or greater.")

        self.x1, self.y1 = x, y
        self.x2 = x + width - 1  # (width - 1) because grid starts from 0
        self.y2 = y + height - 1  # (height - 1) because grid starts from 0
        self.width = width
        self.height = height
        self.connections = []  # List of which rooms this room is connected to
        self.doors = []
        self.label = None  # This will be set externally on map generation

        self.char_dict = self.get_char_dict()

    @property
    def center(self):
        """ Returns the coordinate closest to the center of the room."""
        # describes the “x” and “y” coordinates of the center of a room. I
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    @property
    def nw_corner(self):
        """Returns the coordinate representing the northwest corner."""
        return self.x1, self.y1

    @property
    def ne_corner(self):
        """Returns the coordinate representing the northeast corner."""
        return self.x2, self.y1

    @property
    def sw_corner(self):
        """Returns the coordinate representing the southwest corner."""
        return self.x1, self.y2

    @property
    def se_corner(self):
        """Returns the coordinate representing the southeast corner."""
        return self.x2, self.y2

    def corners(self):
        """Returns the coordinates of all the corners as a set."""
        return {
            self.nw_corner, self.ne_corner,
            self.sw_corner, self.se_corner
        }

    @property
    def full_slice(self):
        """Return the inner area of this room as a 2D array index."""
        return slice(self.x1, self.x2 + 1), slice(self.y1, self.y2 + 1)

    @property
    def inner(self):
        """Return the inner area of this room as a 2D array index."""
        # TODO: Change this to return a set of coordinates
        # Returns a Tuple[slice, slice]
        # We add 1 to x1 and y1 to return the inner
        # We don't have to -1 from x2 or y2 because the slice end range takes care of that automatically.
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

        # Explanation for + 1 on self.x1 and self.y1
        # Ex: room at coordinates (1, 1) that goes to (6, 6).

        #   0 1 2 3 4 5 6 7
        # 0 # # # # # # # #
        # 1 # . . . . . . #
        # 2 # . . . . . . #
        # 3 # . . . . . . #
        # 4 # . . . . . . #
        # 5 # . . . . . . #
        # 6 # . . . . . . #
        # 7 # # # # # # # #

        # If we carve out the entire area like this, we miss the outer wall.
        # A bordering room would 'merge' into this room.
        # Ex: We put a room right next to as (7, 1) to (9, 6)

        #   0 1 2 3 4 5 6 7 8 9 10
        # 0 # # # # # # # # # # #
        # 1 # . . . . . . . . . #
        # 2 # . . . . . . . . . #
        # 3 # . . . . . . . . . #
        # 4 # . . . . . . . . . #
        # 5 # . . . . . . . . . #
        # 6 # . . . . . . . . . #
        # 7 # # # # # # # # # # #

        # As a result, we need to take the walls into account
        # Ex: Room with coordinates (1, 1) to (6, 6)

        #   0 1 2 3 4 5 6 7
        # 0 # # # # # # # #
        # 1 # # # # # # # #
        # 2 # # . . . . # #
        # 3 # # . . . . # #
        # 4 # # . . . . # #
        # 5 # # . . . . # #
        # 6 # # # # # # # #
        # 7 # # # # # # # #

    def intersects(self, other):
        """Return True if this room overlaps with another Room."""
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )

    def perimeter(self):
        """Returns a set of coordinates that represent the perimeter of the room."""
        return self.horz_walls().union(self.vert_walls())  # Union of both sets

    def horz_walls(self):
        """Returns a set of all coordinates that represent the horizontal lines of the room.
        Includes corners. """
        return {(x, y) for y in [self.y1, self.y2] for x in range(self.x1, self.x2 + 1)}

    def vert_walls(self):
        """Returns a set of all coordinates that represent the vertical lines of the room.
        Includes corners"""
        return {(x, y) for x in [self.x1, self.x2] for y in range(self.y1, self.y2 + 1)}

    def random_point_inside(self):
        """ Returns a random coordinate anywhere in the area of the inner room floor."""
        x = random.randint(self.x1 + 1, self.x2 - 1)
        y = random.randint(self.y1 + 1, self.y2 - 1)
        return x, y

    def random_door_loc(self):
        """ Returns a random location that a door could be created."""
        return random.choice(list(self.perimeter().difference(self.corners())))

    def all_coords(self):
        """Returns the set of all coordinates representing the room, including walls."""
        return [(self.x1 + x, self.y1 + y) for x in range(self.width) for y in range(self.height)]

    def valid_door_loc(self, x, y):
        """Returns True if the door could be a valid location, False otherwise.
        Doors cannot appear in corners, so corner locations returns False.
        """
        return (x, y) in self.perimeter() and (x, y) not in self.corners()

    def direction_facing(self, x, y):
        """Returns which cardinal direction the coordinate is facing. The coordinate must not be a
        corner, and must be on a wall to be facing a direction.
        """
        # Corners face diagonally, so we won't count them yet.
        if (x, y) in self.corners():
            return None

        if x == self.x1:
            return 'W'
        elif x == self.x2:
            return 'E'
        elif y == self.y1:
            return 'N'
        elif y == self.y2:
            return 'S'

    def match_facing_doors(self, room2):
        """This finds all the valid door positions in this room and another room, it then compares all
        the combinations to match only the doors which face each other and returns it as a list."""
        room1_doors = self.get_all_possible_doors()
        room2_doors = room2.get_all_possible_doors()

        matches = []
        for a in room1_doors:
            for b in room2_doors:
                if a.facing_other(b):
                    matches.append({a, b})
        return matches

    def get_all_possible_doors(self):
        """Returns a list of all the possible door locations in the room."""
        walls = self.perimeter().difference(self.corners())
        return [Door(self, x, y) for x, y in walls]

    def get_char_dict(self):
        """Builds a dict of coordinates and the tile to represent that tile in the room"""
        char_dict = {}
        # vertical walls
        for x, y in self.vert_walls():
            char_dict[(x, y)] = tiles.room_vert_wall

        # horizontal walls
        for x, y in self.horz_walls():
            char_dict[(x, y)] = tiles.room_horz_wall

        # Corners (overwrites somes values from vert_walls and horz_walls
        char_dict[self.ne_corner] = tiles.room_ne_corner
        char_dict[self.nw_corner] = tiles.room_nw_corner
        char_dict[self.se_corner] = tiles.room_se_corner
        char_dict[self.sw_corner] = tiles.room_sw_corner
        return char_dict

    def wall_light_dict(self):
        d = {}
        for x in range(self.x1, self.x2 + 1):
            d[(x, self.y1)] = (x, self.y1 + 1)  # top row (add 1 y)
            d[(x, self.y2)] = (x, self.y2 - 1)  # bottom row (minus 1 y)

        for y in range(self.y1, self.y2 + 1):
            d[(self.x1, y)] = (self.x1 + 1, y)  # left col (add 1 x)
            d[(self.x2, y)] = (self.x2 - 1, y)  # right col (minux 1 x)

        d[self.nw_corner] = self.x1 + 1, self.y1 + 1  # nw corner: (+1, +1)
        d[self.ne_corner] = self.x2 - 1, self.y1 + 1  # ne corner: (-1, +1)
        d[self.sw_corner] = self.x1 + 1, self.y2 - 1  # sw corner: (+1, -1)
        d[self.se_corner] = self.x2 - 1, self.y2 - 1  # se corner: (-1, -1)
        return d

    def floor_light_dict(self):
        d = defaultdict(set)
        for x in range(self.x1 + 1, self.x2):  # Ignore corners
            d[(x, self.y1 + 1)].add((x, self.y1))  # top row (add 1 y)
            d[(x, self.y2 - 1)].add((x, self.y2))  # bottom row (minus 1 y)

        for y in range(self.y1 + 1, self.y2):  # Ignore corners
            d[(self.x1 + 1, y)].add((self.x1, y))  # left col (add 1 x)
            d[(self.x2 - 1, y)].add((self.x2, y))  # right col (minux 1 x)

        d[self.x1 + 1, self.y1 + 1].add(self.nw_corner)  # nw corner: (+1, +1)
        d[self.x2 - 1, self.y1 + 1].add(self.ne_corner)  # ne corner: (-1, +1)
        d[self.x1 + 1, self.y2 - 1].add(self.sw_corner)  # sw corner: (+1, -1)
        d[self.x2 - 1, self.y2 - 1].add(self.se_corner)  # se corner: (-1, -1)

        return d