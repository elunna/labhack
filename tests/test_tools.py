from src import factory
from src import gamemap
from src import tiles

def test_map():
    # Door pending

    #   0 1 2 3 4 5
    # 0 # # . . . .
    # 1 # # . . . .
    # 2 . + . . . .
    # 3 # # . . # .
    # 4 # # . . # .
    # 5 # # . . . @

    new_map = gamemap.GameMap(
        width=6,
        height=6,
        entities=(),
        engine=None,
        fill_tile=tiles.floor
    )
    walls = [(0, 0), (1, 0),
             (0, 1), (1, 1),
             (0, 3), (1, 3), (4, 3),
             (0, 4), (1, 4), (4, 4),
             (0, 5), (1, 5),
             ]

    for x, y in walls:
        new_map.tiles[x, y] = tiles.wall

    factory.player.spawn(new_map, 5, 5)
    return new_map
