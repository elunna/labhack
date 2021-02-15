import random


class Rect:
    def __init__(self, x, y, width, height):
        if width < 3 or height < 3:
            raise ValueError("Width and height must be at least 3 or greater.")

        self.x1 = x
        self.y1 = y
        # Should this be width - 1?
        self.x2 = x + width
        # Should this be height - 1?
        self.y2 = y + height

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
        return self.x2 - 1, self.y1

    @property
    def sw_corner(self):
        return self.x1, self.y2 - 1

    @property
    def se_corner(self):
        return self.x2 - 1, self.y2 - 1

    @property
    def inner(self):
        """Return the inner area of this room as a 2D array index."""
        # Returns a Tuple[slice, slice]
        return slice(self.x1 + 1, self.x2 - 1), slice(self.y1 + 1, self.y2 - 1)

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
        perimeter = []
        for x in range(self.x1, self.x2):
            perimeter.extend([(x, self.y1), (x, self.y2 - 1)])
        for y in range(self.y1 + 1, self.y2 - 1):
            perimeter.extend([(self.x1, y), (self.x2 - 1, y)])
        return perimeter

    def horz_walls(self):
        return [(x, y) for y in [self.y1, self.y2 - 1] for x in range(self.x1 + 1, self.x2 - 1)]

    def vert_walls(self):
        return [(x, y) for x in [self.x1, self.x2 - 1] for y in range(self.y1 + 1, self.y2 - 1)]

    def random_point_inside(self):
        x = random.randint(self.x1 + 1, self.x2 - 2)
        y = random.randint(self.y1 + 1, self.y2 - 2)
        return x, y
