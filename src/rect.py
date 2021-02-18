import random


class Rect:
    def __init__(self, x, y, width, height):
        if width < 3 or height < 3:
            raise ValueError("Width and height must be at least 3 or greater.")

        self.x1, self.y1 = x, y
        self.x2 = x + width - 1  # (width - 1) because grid starts from 0
        self.y2 = y + height - 1  # (height - 1) because grid starts from 0
        self.width = width
        self.height = height
        self.connected = False  # Used for tracking if a tunnel connects this to another room

    @property
    def center(self):
        # describes the “x” and “y” coordinates of the center of a room. I
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        # Returns a Tuple[int, int]
        return center_x, center_y

    # TODO: Fix x2 and y2 so we don't have to -1
    @property
    def nw_corner(self):
        return self.x1, self.y1

    @property
    def ne_corner(self):
        return self.x2, self.y1

    @property
    def sw_corner(self):
        return self.x1, self.y2

    @property
    def se_corner(self):
        return self.x2, self.y2

    def corners(self):
        return {
            self.nw_corner, self.ne_corner,
            self.sw_corner, self.se_corner
        }

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
        # Ex: Rectangle with coordinates (1, 1) to (6, 6)

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
        """Return True if this room overlaps with another RectangularRoom."""
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )

    def perimeter(self):
        # Returns a set of coordinates that represent the perimeter of the rectangle.
        return self.horz_walls().union(self.vert_walls())  # Union of both sets

    def horz_walls(self):
        # Returns a set of all coordinates that represent the horizontal lines of the rectangle.
        # Includes corners
        return {(x, y) for y in [self.y1, self.y2] for x in range(self.x1, self.x2 + 1)}

    def vert_walls(self):
        # Returns a set of all coordinates that represent the vertical lines of the rectangle.
        # Includes corners
        return {(x, y) for x in [self.x1, self.x2] for y in range(self.y1, self.y2 + 1)}

    def random_point_inside(self):
        x = random.randint(self.x1 + 1, self.x2 - 1)
        y = random.randint(self.y1 + 1, self.y2 - 1)
        return x, y

    def random_door_loc(self):
        return random.choice(list(self.perimeter().difference(self.corners())))

    def all_coords(self):
        return [(self.x1 + x, self.y1 + y) for x in range(self.width) for y in range(self.height)]