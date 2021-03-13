import math


def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def myround(x, base=25):
    """ Simple rounding function to make xp levels look cleaner.
        Rounds to the nearest 'base'
    """
    return base * round(x/base)


def pluralize_str(string):
    string += "s"
    return string

    # broken_up = string.split()
    # last_word = broken_up[-1]


def radius(x, y, radius):
    """Generates coordinates for an area surrounding the specified coordinates. """
    max_x = x + radius
    min_x = x - radius
    max_y = y + radius
    min_y = y - radius
    tiles = set()

    for x2 in range(min_x, max_x + 1):
        for y2 in range(min_y, max_y + 1):
            if distance(x, y, x2, y2) <= radius:
                tiles.add((x2, y2))
    return tiles
