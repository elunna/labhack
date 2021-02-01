""" Tests for procgen.py """

import game_map
import procgen
import pytest
import rectangle
import tile_types


@pytest.fixture
def wall_map():
    return game_map.GameMap(width=20, height=10)


@pytest.fixture
def test_map():
    return procgen.generate_map(
        max_rooms=5,
        room_min_size=3,
        room_max_size=4,
        map_width=20,
        map_height=10,
        floor_number=0
    )


def test_generate_map_returns_GameMap(test_map):
    # Verify generate_map returns a GameMap
    assert isinstance(test_map, game_map.GameMap)

    # Verify width/height
    assert test_map.width == 20
    assert test_map.height == 10

    # TODO: Map contains its dungeon level
    # assert test_map.level_num == 0

    # Entities/Items - verify they are empty
    assert len(test_map.entities) == 0
    # assert len(test_map.items) == 0  # Generator...

    # Verify downstair was placed
    assert test_map.downstairs_location

    # Verify upstair was placed
    assert test_map.upstairs_location

    # assert test_map.tiles[test_map.downstairs_location] == tile_types.up_stairs


def test_mk_room_3x3(wall_map):
    rect = procgen.mk_room(wall_map, 3, 3)
    # x1 can be 0-17, x2 can be 2-19
    assert rect.x1 >= 0 and rect.x1 <= 17
    assert rect.x2 >= 2 and rect.x2 <= 19

    # y1 can be 0-7, y2 can be 2-9
    assert rect.y1 >= 0 and rect.y1 <= 7
    assert rect.y2 >= 2 and rect.y2 <= 9

    # self.engine.game_map.tiles["walkable"][dest_x, dest_y]
    pass

def test_dig_room(wall_map):
    rect = rectangle.Rectangle(x=0, y=0, width=3, height=3)
    procgen.dig_room(wall_map, rect)

    # Only 1 tile should be dug out
    assert wall_map.tiles["walkable"][1, 1]

    # Surrounding tiles should still be wall
    assert not wall_map.tiles["walkable"][0, 0]
    assert not wall_map.tiles["walkable"][1, 0]
    assert not wall_map.tiles["walkable"][2, 0]
    assert not wall_map.tiles["walkable"][0, 1]
    assert not wall_map.tiles["walkable"][2, 1]
    assert not wall_map.tiles["walkable"][0, 2]
    assert not wall_map.tiles["walkable"][1, 2]
    assert not wall_map.tiles["walkable"][2, 2]

def test_tunnel_between__horz_first(wall_map):
    rect = rectangle.Rectangle(x=0, y=0, width=3, height=3)
    start = (0, 0)
    end = (2, 2)
    result = procgen.tunnel_between(start, end, twist=1)

    # corner is repeated
    assert list(result) == [
        (0, 0), (1, 0), (2, 0), (2, 0), (2, 1), (2, 2)
    ]


def test_tunnel_between__vert_first(wall_map):
    rect = rectangle.Rectangle(x=0, y=0, width=3, height=3)
    start = (0, 0)
    end = (2, 2)
    result = procgen.tunnel_between(start, end, twist=2)

    # corner is repeated
    assert list(result) == [
        (0, 0), (0, 1), (0, 2), (0, 2), (1, 2), (2, 2)
    ]


item_chances = {
    # keys in the dictionary represent the floor number,
    # and the value is a list of tuples.
    # 0: [(health_potion, 35), (confusion_potion, 35)],
    0: [('a', 5), ('b', 5)],
    1: [('a', 10), ('c', 5)],
    2: [('a', 15), ('d', 5)],
}


@pytest.mark.skip(reason='Create sample tables for testing')
def test_get_max_value_for_floor():
    pass


@pytest.mark.skip(reason='Create sample tables for testing')
def test_get_entities_at_random():
    pass

@pytest.mark.skip(reason='Method too complicated')
def test_place_entities():
    pass


