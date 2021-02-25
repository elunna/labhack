""" Tools for testing """
from src import factory
from src import gamemap
from src import tiles
import copy


def cp_player():
    return copy.deepcopy(factory.player)


def test_map():
    # Door pending

    #   0 1 2 3 4 5
    # 0 # # . . . .
    # 1 # # . . . .
    # 2 . + . . . .
    # 3 # # . . # .
    # 4 # # . . # o
    # 5 # # x . . @

    new_map = gamemap.GameMap(
        width=6,
        height=6,
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

    # Create a player at 5, 5
    player = copy.deepcopy(factory.player)
    new_map.add_entity(player, 5, 5)
    new_map.player = player

    # Set the player parent to the map
    player.parent = new_map

    # Give the player items for testing
    dagger = copy.deepcopy(factory.dagger)
    player.inventory.add_item(dagger)

    leather_armor = copy.deepcopy(factory.leather_vest)
    player.inventory.add_item(leather_armor)

    health_potion = copy.deepcopy(factory.health_potion)
    player.inventory.add_item(health_potion)

    # Create a grid bug at 2, 5
    factory.grid_bug.spawn(new_map, 2, 5)

    # Create a grid bug at 5, 4
    factory.orc.spawn(new_map, 5, 4)

    return new_map


def stair_map():
    new_map = gamemap.GameMap(
        width=10,
        height=10,
        fill_tile=tiles.floor
    )
    new_map.tiles[0, 0] = tiles.up_stairs
    new_map.tiles[9, 9] = tiles.down_stairs

    return new_map