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