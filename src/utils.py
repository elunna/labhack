def myround(x, base=25):
    """ Simple rounding function to make xp levels look cleaner.
        Rounds to the nearest 'base'
    """
    return base * round(x/base)