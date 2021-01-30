import numpy as np

# Tile graphics structured type compatible with Console.tiles_rgb.
# dtype creates a data type which Numpy can use, which behaves similarly to a
# struct in a language like C. Our data type is made up of three parts:

#   ch: The character, represented in integer format. We’ll translate it from
#       the integer into Unicode.
#   fg: The foreground color. “3B” means 3 unsigned bytes, which can be used
#       for RGB color codes.
#   bg: The background color. Similar to fg.

graphic_dt = np.dtype(
    [
        ("ch", np.int32),  # Unicode codepoint.
        ("fg", "3B"),  # 3 unsigned bytes, for RGB colors.
        ("bg", "3B"),
    ]
)

# Tile struct used for statically defined tile data.
tile_dt = np.dtype(
    [
        ("walkable", np.bool),  # True if this tile can be walked over.
        ("transparent", np.bool),  # True if this tile doesn't block FOV.
        ("dark", graphic_dt),  # Graphics for when this tile is not in FOV.
        ("light", graphic_dt),  # Graphics for when the tile is in FOV.
    ]
)


def new_tile(*, walkable, transparent, dark, light):
    """Helper function for defining individual tile types """
    # *: Enforce the use of keywords, so that parameter order doesn't matter.
    # dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]
    return np.array((walkable, transparent, dark, light), dtype=tile_dt)


# SHROUD represents unexplored, unseen tiles (as black tiles)
SHROUD = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)


floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), (50, 50, 150)),  # Original
    light=(ord(" "), (255, 255, 255), (200, 180, 50)),  # Original
    # dark=(ord("."), (100, 100, 100), (0, 0, 0)),  # Traditional
    # light=(ord("."), (200, 200, 200), (0, 0, 0)),  # Traditional
)

wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord(" "), (255, 255, 255), (0, 0, 100)),  # Original
    light=(ord(" "), (255, 255, 255), (130, 110, 50)),  # Original
    # dark=(ord("#"), (100, 100, 100), (0, 0, 0)),  # Traditional
    # light=(ord("#"), (200, 200, 200), (0, 0, 0)),  # Traditional
)

down_stairs = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(">"), (0, 0, 100), (50, 50, 150)),  # Original
    light=(ord(">"), (255, 255, 255), (200, 180, 50)),  # Original
    # dark=(ord(">"), (100, 100, 100), (0, 0, 0)),  # Traditional
    # light=(ord(">"), (200, 200, 200), (0, 0, 0)),  # Traditional
)
