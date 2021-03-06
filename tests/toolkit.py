""" Tools for testing """

from src import factory
from src import gamemap
from src import tiles


def cp_player():
    return factory.make("player")


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
    player = factory.spawn("player", new_map, 5, 5)
    new_map.player = player

    # Set the player parent to the map
    player.parent = new_map

    # Give the player items for testing
    dagger = factory.make("dagger")
    player.inventory.add_inv_item(dagger)

    leather_armor = factory.make("leather vest")
    player.inventory.add_inv_item(leather_armor)

    health_vial = factory.make("healing vial")
    player.inventory.add_inv_item(health_vial)

    # Create a grid bug at 2, 5
    factory.spawn("grid bug", new_map, 2, 5)

    # Create a spider drone at 5, 4
    factory.spawn("henchman", new_map, 5, 4)

    return new_map


def hidden_map():
    # Door pending

    #   0 1 2 3 4
    # 0 # # . # #
    # 1 # # b # #   b=hidden banana trap
    # 2 . + @ % .   +=hidden door, and %=hidden corridor
    # 3 # # ^ # #   ^=hidden bear trap
    # 4 # # . # #

    new_map = gamemap.GameMap(
        width=6,
        height=6,
        fill_tile=tiles.wall
    )
    floors = [(2, 0), (2, 1), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (2, 3), (2, 4)]

    for x, y in floors:
        new_map.tiles[x, y] = tiles.floor

    # Create a player at 5, 5
    player = factory.spawn("player", new_map, 2, 2)
    new_map.player = player

    # Create bear trap at 2, 3
    new_trap = factory.make("bear trap")
    new_map.place(new_trap, 2, 3)

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
