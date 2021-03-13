import numpy as np

# Tile graphics structured type compatible with Console.tiles_rgb.
# dtype creates a data type which Numpy can use, which behaves similarly to a
# struct in a language like C. Our data type is made up of three parts:

#   ch: The character, represented in integer format. We’ll translate it from
#       the integer into Unicode.
#   fg: The foreground color. “3B” means 3 unsigned bytes, which can be used
#       for RGB color codes.
#   bg: The background color. Similar to fg.
from src import settings

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
        ("diggable", np.bool),  # True if it can be dug out by map generators.
        ("dark", graphic_dt),  # Graphics for when this tile is not in FOV.
        ("light", graphic_dt),  # Graphics for when the tile is in FOV.
    ]
)


def new_tile(*, walkable, transparent, diggable, dark, light):
    """Helper function for defining individual tile types """
    # *: Enforce the use of keywords, so that parameter order doesn't matter.
    # dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]

    # First arg = shape?
    return np.array((walkable, transparent, diggable, dark, light), dtype=tile_dt)


# SHROUD represents unexplored, unseen tiles (as black tiles)
SHROUD = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)


floor = new_tile(
    walkable=True,
    transparent=True,
    diggable=True,
    # dark=(ord(" "), (255, 255, 255), (50, 50, 150)),  # Original
    # light=(ord(" "), (255, 255, 255), (200, 180, 50)),  # Original
    dark=(ord(settings.floor), (100, 100, 100), (0, 0, 0)),  # Traditional
    light=(ord(settings.floor), (200, 200, 200), (0, 0, 0)),  # Traditional
)

room_floor = new_tile(
    walkable=True,
    transparent=True,
    diggable=False,
    dark=(ord(settings.room_floor_dark), (100, 100, 100), (0, 0, 0)),  # Traditional
    light=(ord(settings.room_floor_light), (200, 200, 200), (0, 0, 0)),  # Traditional
)

wall = new_tile(
    walkable=False,
    transparent=False,
    diggable=True,
    dark=(ord(settings.wall), (100, 100, 100), (0, 0, 0)),  # Traditional
    light=(ord(settings.wall), (200, 200, 200), (0, 0, 0)),  # Traditional
)

room_vert_wall = new_tile(
    walkable=False,
    transparent=False,
    diggable=False,
    dark=(ord(settings.vert_wall), (100, 100, 100), (0, 0, 0)),  # Old dark setting
    # dark=(ord(settings.vert_wall), (200, 200, 200), (0, 0, 0)),
    light=(ord(settings.vert_wall), (200, 200, 200), (0, 0, 0)),
)

room_horz_wall = new_tile(
    walkable=False,
    transparent=False,
    diggable=False,
    dark=(ord(settings.horz_wall), (100, 100, 100), (0, 0, 0)),  # Old dark setting
    # dark=(ord(settings.horz_wall), (200, 200, 200), (0, 0, 0)),
    light=(ord(settings.horz_wall), (200, 200, 200), (0, 0, 0)),
)

room_ne_corner = new_tile(
    walkable=False,
    transparent=False,
    diggable=False,
    dark=(ord(settings.ne_corner), (100, 100, 100), (0, 0, 0)),  # Old dark setting
    # dark=(ord(settings.ne_corner), (200, 200, 200), (0, 0, 0)),
    light=(ord(settings.ne_corner), (200, 200, 200), (0, 0, 0)),
)

room_sw_corner = new_tile(
    walkable=False,
    transparent=False,
    diggable=False,
    dark=(ord(settings.sw_corner), (100, 100, 100), (0, 0, 0)),  # Old dark setting
    # dark=(ord(settings.sw_corner), (200, 200, 200), (0, 0, 0)),
    light=(ord(settings.sw_corner), (200, 200, 200), (0, 0, 0)),
)


room_nw_corner = new_tile(
    walkable=False,
    transparent=False,
    diggable=False,
    dark=(ord(settings.nw_corner), (100, 100, 100), (0, 0, 0)),  # Old dark setting
    # dark=(ord(settings.nw_corner), (200, 200, 200), (0, 0, 0)),
    light=(ord(settings.nw_corner), (200, 200, 200), (0, 0, 0)),
)

room_se_corner = new_tile(
    walkable=False,
    transparent=False,
    diggable=False,
    dark=(ord(settings.se_corner), (100, 100, 100), (0, 0, 0)),# Old dark setting
    # dark=(ord(settings.se_corner), (200, 200, 200), (0, 0, 0)),
    light=(ord(settings.se_corner), (200, 200, 200), (0, 0, 0)),
)

door = new_tile(
    walkable=True,
    transparent=True,
    diggable=False,
    dark=(ord(settings.closed_door), (100, 100, 100), (0, 0, 0)),
    light=(ord(settings.closed_door), (200, 200, 200), (0, 0, 0)),
)

down_stairs = new_tile(
    walkable=True,
    transparent=True,
    diggable=False,
    # dark=(ord(">"), (0, 0, 100), (50, 50, 150)),  # Original
    # light=(ord(">"), (255, 255, 255), (200, 180, 50)),  # Original
    dark=(ord(">"), (100, 100, 100), (0, 0, 0)),  # Traditional
    light=(ord(">"), (200, 200, 200), (0, 0, 0)),  # Traditional

)

up_stairs = new_tile(
    walkable=True,
    transparent=True,
    diggable=False,
    # dark=(ord("<"), (0, 0, 100), (50, 50, 150)),  # Original
    # light=(ord("<"), (255, 255, 255), (200, 180, 50)),  # Original
    dark=(ord("<"), (100, 100, 100), (0, 0, 0)),  # Traditional
    light=(ord("<"), (200, 200, 200), (0, 0, 0)),  # Traditional
)

room_walls = (
    room_vert_wall,
    room_horz_wall,
    room_ne_corner,
    room_nw_corner,
    room_sw_corner,
    room_se_corner,
)

room_corners = (
    room_ne_corner,
    room_nw_corner,
    room_sw_corner,
    room_se_corner,
)