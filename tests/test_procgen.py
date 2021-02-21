""" Tests for procgen.py """
from src import procgen
import pytest

# place entities
# generate_dungeon


def test_tunnel_between__horz_first():
    start = (0, 0)
    end = (2, 2)
    result = procgen.tunnel_between(start, end, twist=1)

    # corner is repeated
    assert result == [
        (0, 0), (1, 0), (2, 0), (2, 0), (2, 1), (2, 2)
    ]


def test_tunnel_between__vert_first():
    start = (0, 0)
    end = (2, 2)
    result = procgen.tunnel_between(start, end, twist=2)

    # corner is repeated
    assert result == [
        (0, 0), (0, 1), (0, 2), (0, 2), (1, 2), (2, 2)
    ]


def test_tunnel_between__straight_line_vert():
    # Proof that this can draw straight lines as well.
    start = (0, 0)
    end = (0, 2)
    result = procgen.tunnel_between(start, end, twist=2)

    # corner is repeated
    assert result == [(0, 0), (0, 1), (0, 2), (0, 2)]



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