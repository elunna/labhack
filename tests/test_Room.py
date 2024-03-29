""" Tests for rect.py """
import pytest
from src import room


def test_Room_init():
    r = room.Room(0, 0, 3, 3)
    assert r


def test_init__connections():
    r = room.Room(0, 0, 3, 3)
    assert r.connections == []


def test_init__label():
    r = room.Room(0, 0, 3, 3)
    assert r.label is None


def test_init_x2():
    r = room.Room(0, 0, 5, 10)
    assert r.x2 == 4


def test_init_y2():
    r = room.Room(0, 0, 5, 10)
    assert r.y2 == 9


def test_init_negative_x_raises_ValueError():
    with pytest.raises(ValueError):
        room.Room(-2, 2, 2, 2)


def test_init_negative_y_raises_ValueError():
    with pytest.raises(ValueError):
        room.Room(2, -2, 2, 2)


def test_init_low_w_raises_ValueError():
    with pytest.raises(ValueError):
        room.Room(2, 2, 2, 3)


def test_init_low_h_raises_ValueError():
    with pytest.raises(ValueError):
        room.Room(2, 2, 3, 2)


def test_center():
    r = room.Room(0, 0, 3, 3)
    center = (1, 1)
    assert r.center == center


def test_nw_corner():
    r = room.Room(0, 0, 3, 3)
    assert r.nw_corner == (0, 0)


def test_ne_corner():
    r = room.Room(0, 0, 3, 3)
    assert r.ne_corner == (2, 0)


def test_sw_corner():
    r = room.Room(0, 0, 3, 3)
    assert r.sw_corner == (0, 2)


def test_se_corner():
    r = room.Room(0, 0, 3, 3)
    assert r.se_corner == (2, 2)


def test_corners():
    r = room.Room(0, 0, 3, 3)
    assert r.corners() == {(0, 0), (0, 2), (2, 0), (2, 2)}


def test_inner_3x3_square_room():
    r = room.Room(0, 0, 3, 3)
    inner = r.inner
    assert len(inner) == 2  # We should get a Tuple length 2
    assert inner[0] == slice(1, 2, None)  # x slice
    assert inner[1] == slice(1, 2, None)  # y slice


def test_inner_4x4_square_room():
    r = room.Room(0, 0, 4, 4)
    inner = r.inner
    assert len(inner) == 2  # We should get a Tuple length 2
    assert inner[0] == slice(1, 3, None)  # x slice
    assert inner[1] == slice(1, 3, None)  # y slice


def test_inner_4x3_square_room():
    r = room.Room(0, 0, 4, 3)
    inner = r.inner
    assert inner[0] == slice(1, 3, None)  # x slice
    assert inner[1] == slice(1, 2, None)  # y slice


def test_intersects_no_intersect_returns_False():
    r1 = room.Room(0, 0, 3, 3)
    r2 = room.Room(10, 10, 3, 3)
    assert r1.intersects(r2) is False
    assert r2.intersects(r1) is False


def test_intersects_both_rooms_intersect_returns_True():
    r1 = room.Room(0, 0, 3, 3)
    r2 = room.Room(1, 1, 3, 3)
    assert r1.intersects(r2)
    assert r2.intersects(r1)


def test_perimeter_3x3_room():
    r = room.Room(0, 0, 3, 3)
    result = r.perimeter()
    assert result == {
        (0, 0), (1, 0), (2, 0),
        (0, 1), (2, 1),
        (0, 2), (1, 2), (2, 2),
    }


def test_perimeter_4x4_room():
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


def test_random_point_inside__3x3_room():
    r = room.Room(0, 0, 3, 3)
    result = r.random_point_inside()
    # Only one spot available!
    assert result == (1, 1)


def test_random_door_loc__3x3_room():
    r = room.Room(0, 0, 3, 3)
    result = r.random_door_loc()
    assert result in {(1, 0), (0, 1), (2, 1), (1, 2)}


def test_all_coords__3x3_room():
    r = room.Room(0, 0, 3, 3)
    result = r.all_coords()
    assert result == [
        (0, 0), (0, 1), (0, 2),
        (1, 0), (1, 1), (1, 2),
        (2, 0), (2, 1), (2, 2),
    ]


def test_valid_door_loc__corner_is_not_valid():
    r = room.Room(0, 0, 3, 3)
    assert not r.valid_door_loc(0, 0)


def test_valid_door_loc__inner_perimeter_is_valid():
    r = room.Room(0, 0, 3, 3)
    assert r.valid_door_loc(1, 0)


def test_direction_facing__N():
    r = room.Room(0, 0, 3, 3)
    assert r.direction_facing(1, 0) == 'N'


def test_direction_facing__S():
    r = room.Room(0, 0, 3, 3)
    assert r.direction_facing(1, 2) == 'S'


def test_direction_facing__E():
    r = room.Room(0, 0, 3, 3)
    assert r.direction_facing(2, 1) == 'E'


def test_direction_facing__W():
    r = room.Room(0, 0, 3, 3)
    assert r.direction_facing(0, 1) == 'W'


def test_direction_facing__inner_point_returns_None():
    r = room.Room(0, 0, 3, 3)
    assert r.direction_facing(1, 1) is None


def test_direction_facing__corner_returns_None():
    r = room.Room(0, 0, 3, 3)
    assert r.direction_facing(0, 0) is None


def test_wall_light_dict__3x3_room():
    r = room.Room(0, 0, 3, 3)
    assert r.wall_light_dict() == {
        (0, 0): (1, 1),
        (1, 0): (1, 1),
        (2, 0): (1, 1),
        (0, 1): (1, 1),
        (2, 1): (1, 1),
        (0, 2): (1, 1),
        (1, 2): (1, 1),
        (2, 2): (1, 1),
    }


def test_wall_light_dict__4x4_room():
    r = room.Room(0, 0, 4, 4)
    assert r.wall_light_dict() == {
        (0, 0): (1, 1),
        (1, 0): (1, 1),
        (2, 0): (2, 1),
        (3, 0): (2, 1),
        (0, 1): (1, 1),
        (3, 1): (2, 1),
        (0, 2): (1, 2),
        (3, 2): (2, 2),
        (0, 3): (1, 2),
        (1, 3): (1, 2),
        (2, 3): (2, 2),
        (3, 3): (2, 2)
    }


def test_floor_light_dict__3x3_room():
    r = room.Room(0, 0, 3, 3)
    assert r.floor_light_dict() == {
        (1, 1): {
            (0, 0), (1, 0), (2, 0),
            (0, 1), (2, 1),
            (0, 2), (1, 2), (2, 2)
        }
    }


def test_floor_light_dict__4x4_room():
    r = room.Room(0, 0, 4, 4)
    assert r.floor_light_dict() == {
        (1, 1): {(0, 0), (1, 0), (0, 1)},
        (2, 1): {(2, 0), (3, 0), (3, 1)},
        (1, 2): {(0, 2), (0, 3), (1, 3)},
        (2, 2): {(3, 2), (2, 3), (3, 3)}
    }
