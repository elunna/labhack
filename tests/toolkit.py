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
    player.x = 5
    player.y = 5
    new_map.entities.add(player)
    new_map.player = player

    # Set the player parent to the map
    player.parent = new_map

    # Give the player items for testing
    dagger = copy.deepcopy(factory.dagger)
    dagger.parent = player.inventory
    player.inventory.add_item(dagger)

    leather_armor = copy.deepcopy(factory.leather_vest)
    leather_armor.parent = player.inventory
    player.inventory.add_item(leather_armor)

    health_potion = copy.deepcopy(factory.health_potion)
    health_potion.parent = player.inventory
    player.inventory.add_item(health_potion)

    # Create a grid bug at 2, 5
    factory.grid_bug.spawn(new_map, 2, 5)

    # Create a grid bug at 5, 4
    factory.orc.spawn(new_map, 5, 4)

    return new_map
