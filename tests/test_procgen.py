""" Tests for procgen.py """
from src import procgen


def test_generate_random_room__in_bounds():
    map_width, map_height = 100, 50
    min_size, max_size = 5, 10
    r = procgen.generate_random_room(map_width, map_height, min_size, max_size)
    assert r.x1 >= 0 and r.y1 >= 0
    assert r.x2 < map_width
    assert r.y2 < map_height


def test_generate_random_room__within_max_size():
    map_width, map_height = 100, 50
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
