""" Tests for rect.py """

import pytest
from src import room


def test_Room_init():
    r = room.Room(0, 0, 3, 3)
    assert r


def test_Room_init__connections():
    r = room.Room(0, 0, 3, 3)
    assert r.connections == []


def test_Room_init__label():
    r = room.Room(0, 0, 3, 3)
    assert r.label is None


def test_Room_init_x2():
    r = room.Room(0, 0, 5, 10)
    assert r.x2 == 4


def test_Room_init_y2():
    r = room.Room(0, 0, 5, 10)
    assert r.y2 == 9


def test_Room_init_negative_x_raises_ValueError():
    with pytest.raises(ValueError):
        room.Room(-2, 2, 2, 2)


def test_Room_init_negative_y_raises_ValueError():
    with pytest.raises(ValueError):
        room.Room(2, -2, 2, 2)


def test_Room_init_low_w_raises_ValueError():
    with pytest.raises(ValueError):
        room.Room(2, 2, 2, 3)


def test_Room_init_low_h_raises_ValueError():
    with pytest.raises(ValueError):
        room.Room(2, 2, 3, 2)


def test_Room_center():
    r = room.Room(0, 0, 3, 3)
    center = (1, 1)
    assert r.center == center


def test_Room_nw_corner():
    r = room.Room(0, 0, 3, 3)
    assert r.nw_corner == (0, 0)


def test_Room_ne_corner():
    r = room.Room(0, 0, 3, 3)
    assert r.ne_corner == (2, 0)


def test_Room_sw_corner():
    r = room.Room(0, 0, 3, 3)
    assert r.sw_corner == (0, 2)


def test_Room_se_corner():
    r = room.Room(0, 0, 3, 3)
    assert r.se_corner == (2, 2)


def test_Room_corners():
    r = room.Room(0, 0, 3, 3)
    assert r.corners() == {(0, 0), (0, 2), (2, 0), (2, 2)}


def test_Room_inner_3x3_square_room():
    r = room.Room(0, 0, 3, 3)
    inner = r.inner
    assert len(inner) == 2  # We should get a Tuple length 2
    assert inner[0] == slice(1, 2, None)  # x slice
    assert inner[1] == slice(1, 2, None)  # y slice


def test_Room_inner_4x4_square_room():
    r = room.Room(0, 0, 4, 4)
    inner = r.inner
    assert len(inner) == 2  # We should get a Tuple length 2
    assert inner[0] == slice(1, 3, None)  # x slice
    assert inner[1] == slice(1, 3, None)  # y slice


def test_Room_inner_4x3_square_room():
    r = room.Room(0, 0, 4, 3)
    inner = r.inner
    assert inner[0] == slice(1, 3, None)  # x slice
    assert inner[1] == slice(1, 2, None)  # y slice


def test_Room_intersects_no_intersect_returns_False():
    r1 = room.Room(0, 0, 3, 3)
    r2 = room.Room(10, 10, 3, 3)
    assert r1.intersects(r2) is False
    assert r2.intersects(r1) is False


def test_Room_intersects_both_rooms_intersect_returns_True():
    r1 = room.Room(0, 0, 3, 3)
    r2 = room.Room(1, 1, 3, 3)
    assert r1.intersects(r2)
    assert r2.intersects(r1)


def test_Room_perimeter_3x3_room():
    r = room.Room(0, 0, 3, 3)
    result = r.perimeter()
    assert result == {
        (0, 0), (1, 0), (2, 0),
        (0, 1), (2, 1),
        (0, 2), (1, 2), (2, 2),
    }


def test_Room_perimeter_4x4_room():
    r = room.Room(0, 0, 4, 4)
    result = r.perimeter()
    assert result == {
        (0, 0), (1, 0), (2, 0), (3, 0),
        (0, 1), (3, 1),
        (0, 2), (3, 2),
        (0, 3), (1, 3), (2, 3), (3, 3)
    }


def test_horz_walls_3x3_room():
    r = room.Room(0, 0, 3, 3)
    result = r.horz_walls()
    assert result == {
        (0, 0), (1, 0), (2, 0),
        (0, 2), (1, 2), (2, 2),
    }


def test_horz_walls_4x4_room():
    r = room.Room(0, 0, 4, 4)
    result = r.horz_walls()
    assert result == {
        (0, 0), (1, 0), (2, 0), (3, 0),
        (0, 3), (1, 3), (2, 3), (3, 3),
    }


def test_vert_walls_3x3_room():
    r = room.Room(0, 0, 3, 3)
    result = r.vert_walls()
    assert result == {
        (0, 0), (0, 1), (0, 2),
        (2, 0), (2, 1), (2, 2),
    }


def test_vert_walls_4x4_room():
    r = room.Room(0, 0, 4, 4)
    result = r.vert_walls()
    assert result == {
        (0, 0), (0, 1), (0, 2), (0, 3),
        (3, 0), (3, 1), (3, 2), (3, 3),
    }


def test_Room_random_point_inside__3x3_room():
    r = room.Room(0, 0, 3, 3)
    result = r.random_point_inside()
    # Only one spot available!
    assert result == (1, 1)


def test_Room_random_door_loc__3x3_room():
    r = room.Room(0, 0, 3, 3)
    result = r.random_door_loc()
    assert result in {(1, 0), (0, 1), (2, 1), (1, 2)}


def test_Room_all_coords__3x3_room():
    r = room.Room(0, 0, 3, 3)
    result = r.all_coords()
    assert result == [
        (0, 0), (0, 1), (0, 2),
        (1, 0), (1, 1), (1, 2),
        (2, 0), (2, 1), (2, 2),
    ]


def test_Room_valid_door_loc__corner_is_not_valid():
    r = room.Room(0, 0, 3, 3)
    assert not r.valid_door_loc(0, 0)


def test_Room_valid_door_loc__inner_perimeter_is_valid():
    r = room.Room(0, 0, 3, 3)
    assert r.valid_door_loc(1, 0)


def test_Room_direction_facing__N():
    r = room.Room(0, 0, 3, 3)
    assert r.direction_facing(1, 0) == 'N'


def test_Room_direction_facing__S():
    r = room.Room(0, 0, 3, 3)
    assert r.direction_facing(1, 2) == 'S'


def test_Room_direction_facing__E():
    r = room.Room(0, 0, 3, 3)
    assert r.direction_facing(2, 1) == 'E'


def test_Room_direction_facing__W():
    r = room.Room(0, 0, 3, 3)
    assert r.direction_facing(0, 1) == 'W'


def test_Room_direction_facing__inner_point_returns_None():
    r = room.Room(0, 0, 3, 3)
    assert r.direction_facing(1, 1) is None


def test_Room_direction_facing__corner_returns_None():
    r = room.Room(0, 0, 3, 3)
    assert r.direction_facing(0, 0) is None


def test_Door_init__room():
    r = room.Room(0, 0, 3, 3)
    d = room.Door(r, 1, 0)
    assert d.room == r


def test_Door_init__coords():
    r = room.Room(0, 0, 3, 3)
    d = room.Door(r, 1, 0)
    assert d.x == 1
    assert d.y == 0


def test_Door_init__invalid_location__raises_exception():
    r = room.Room(0, 0, 3, 3)
    with pytest.raises(ValueError):
        d = room.Door(r, 0, 0)


def test_Door_init__not_in_its_room__raises_exception():
    r = room.Room(0, 0, 3, 3)
    with pytest.raises(ValueError):
        d = room.Door(r, 100, 1000)


def test_Door_init__facing_other__same_room():
    r = room.Room(0, 0, 3, 3)
    d1 = room.Door(r, 1, 0)
    d2 = room.Door(r, 2, 1)
    assert d1.facing_other(d2) is False


def test_Door_init__facing_other__vertical():
    r1 = room.Room(0, 0, 3, 3)
    d1 = room.Door(r1, 1, 2)

    r2 = room.Room(0, 5, 4, 3)
    d2 = room.Door(r2, 1, 5)
    d3 = room.Door(r2, 2, 5)
    assert d1.facing_other(d2)  # Lined up vertically
    assert d2.facing_other(d1)  # Lined up vertically
    assert d1.facing_other(d3)  # Off by one
    assert d3.facing_other(d1)  # Off by one


def test_Door_init__facing_other__horizontal():
    r1 = room.Room(0, 0, 3, 3)
    d1 = room.Door(r1, 2, 1)

    r2 = room.Room(5, 0, 3, 4)
    d2 = room.Door(r2, 5, 1)
    d3 = room.Door(r2, 5, 2)
    assert d1.facing_other(d2)  # Lined up horizontally
    assert d2.facing_other(d1)  # Lined up horizontally
    assert d1.facing_other(d3)  # Off by one
    assert d3.facing_other(d1)  # Off by one


def test_Door_init__facing_other__facing_away_vertically():
    r1 = room.Room(0, 0, 3, 3)
    d1 = room.Door(r1, 1, 0)  # Facing N

    r2 = room.Room(0, 5, 4, 3)
    d2 = room.Door(r2, 1, 7)  # Facing S
    assert d1.facing_other(d2) is False  # Lined up vertically
    assert d2.facing_other(d1) is False  # Lined up vertically


def test_Door_init__facing_other__facing_away_horizontally():
    r1 = room.Room(0, 0, 3, 3)
    d1 = room.Door(r1, 0, 1)  # Facing west

    r2 = room.Room(5, 0, 3, 4)
    d2 = room.Door(r2, 7, 1)  # Facing east
    assert d1.facing_other(d2) is False  # Lined up horizontally
    assert d2.facing_other(d1) is False  # Lined up horizontally


@pytest.mark.skip(reason="This is okay, allows rooms to be next to eachother.")
def test_Door_init__facing_other__doors_lined_up_horizontally():
    # These doors do not share the same x-axis, there is 1 space between them,
    # but we need at least 2 spaces for them to be facing eachother.
    r1 = room.Room(0, 0, 3, 3)
    d1 = room.Door(r1, 2, 1)  # Facing east

    r2 = room.Room(3, 4, 3, 3)
    d2 = room.Door(r2, 3, 5)  # Facing west
    assert d1.facing_other(d2) is False  # Lined up horizontally
    assert d2.facing_other(d1) is False  # Lined up horizontally


@pytest.mark.skip(reason="This is okay, allows rooms to be next to eachother.")
def test_Door_init__facing_other__doors_lined_up_vertically():
    # These doors do not share the same y-axis, there is 1 space between them,
    # but we need at least 2 spaces for them to be facing eachother.
    r1 = room.Room(0, 0, 3, 3)
    d1 = room.Door(r1, 1, 2)  # Facing south

    r2 = room.Room(4, 3, 3, 3)
    d2 = room.Door(r2, 5, 3)  # Facing north
    assert d1.facing_other(d2) is False  # Lined up vertically
    assert d2.facing_other(d1) is False  # Lined up vertically