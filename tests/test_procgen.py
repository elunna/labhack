""" Tests for procgen.py """
from src import procgen
import pytest


def test_generate_random_room__in_bounds():
    map_width, map_height= 100, 50
    min_size, max_size = 5, 10
    r = procgen.generate_random_room(map_width, map_height, min_size, max_size)
    assert r.x1 >= 0 and r.y1 >= 0
    assert r.x2 < map_width
    assert r.y2 < map_height


def test_generate_random_room__within_max_size():
    map_width, map_height= 100, 50
    min_size, max_size = 5, 10
    r = procgen.generate_random_room(map_width, map_height, min_size, max_size)
    assert r.width <= max_size
    assert r.height <= max_size


def test_generate_random_room__within_min_size():
    map_width, map_height = 100, 50
    min_size, max_size = 5, 10
    r = procgen.generate_random_room(map_width, map_height, min_size, max_size)
    assert r.width >= min_size
    assert r.height >= min_size


def test_get_L_path__horz_first():
    start = (0, 0)
    end = (2, 2)
    result = procgen.create_L_path(start, end, twist=1)

    # corner is repeated
    assert result == [
        (0, 0), (1, 0), (2, 0), (2, 1), (2, 2)
    ]


def test_get_L_path__vert_first():
    start = (0, 0)
    end = (2, 2)
    result = procgen.create_L_path(start, end, twist=2)

    # corner is repeated
    assert result == [
        (0, 0), (0, 1), (0, 2), (1, 2), (2, 2)
    ]


def test_get_L_path__straight_line_vert():
    # Proof that this can draw straight lines as well.
    start = (0, 0)
    end = (0, 2)
    result = procgen.create_L_path(start, end, twist=2)

    # corner is repeated
    assert result == [(0, 0), (0, 1), (0, 2)]



max_foos_by_floor = [
    (0, 1), (2, 2), (3, 3), (5, 5)
]


def test_get_max_value_for_floor__negative():
    result = procgen.get_max_value_for_floor(max_foos_by_floor, -1)
    assert result == 0


def test_get_max_value_for_floor__listed_floor():
    result = procgen.get_max_value_for_floor(max_foos_by_floor, 0)
    assert result == 1


def test_get_max_value_for_floor__inbetween_floor():
    result = procgen.get_max_value_for_floor(max_foos_by_floor, 1)
    assert result == 1


def test_get_max_value_for_floor__higher_floor():
    result = procgen.get_max_value_for_floor(max_foos_by_floor, 1000)
    assert result == 5


weighted_chances = {
    # keys in the dictionary represent the floor number,
    # and the value is a list of tuples.
    # 0: [(health_potion, 35), (confusion_potion, 35)],
    0: [('a', 5), ('b', 5)],
    1: [('a', 10), ('c', 5)],
    2: [('a', 15), ('d', 5)],
}


@pytest.mark.skip(reason='Create sample tables for testing')
def test_get_entities_at_random():
    pass


@pytest.mark.skip(reason='Create sample rooms for testing')
def test_minimum_spanning_tree():
    pass


def test_distance__same_point_0():
    assert procgen.distance(0, 0, 0, 0) == 0


def test_distance__1_sq_east_1():
    assert procgen.distance(0, 0, 1, 0) == 1


def test_distance__1_sq_diagonal():
    result = procgen.distance(0, 0, 1, 1)
    assert  round(result, 2) == 1.41

