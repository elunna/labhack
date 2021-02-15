""" Tests for rect.py """

import pytest
from src import rect


def test_Rect_init():
    r = rect.Rect(0, 0, 3, 3)
    assert r


def test_Rect_init_x2():
    r = rect.Rect(0, 0, 5, 10)
    assert r.x2 == 4


def test_Rect_init_y2():
    r = rect.Rect(0, 0, 5, 10)
    assert r.y2 == 9


def test_Rect_init_negative_x_raises_ValueError():
    with pytest.raises(ValueError):
        rect.Rect(-2, 2, 2, 2)


def test_Rect_init_negative_y_raises_ValueError():
    with pytest.raises(ValueError):
        rect.Rect(2, -2, 2, 2)


def test_Rect_init_low_w_raises_ValueError():
    with pytest.raises(ValueError):
        rect.Rect(2, 2, 2, 3)


def test_Rect_init_low_h_raises_ValueError():
    with pytest.raises(ValueError):
        rect.Rect(2, 2, 3, 2)


def test_Rect_center():
    r = rect.Rect(0, 0, 3, 3)
    center = (1, 1)
    assert r.center == center


def test_Rect_nw_corner():
    r = rect.Rect(0, 0, 3, 3)
    assert r.nw_corner == (0, 0)


def test_Rect_ne_corner():
    r = rect.Rect(0, 0, 3, 3)
    assert r.ne_corner == (2, 0)


def test_Rect_sw_corner():
    r = rect.Rect(0, 0, 3, 3)
    assert r.sw_corner == (0, 2)


def test_Rect_se_corner():
    r = rect.Rect(0, 0, 3, 3)
    assert r.se_corner == (2, 2)


def test_Rect_inner_3x3_square_room():
    r = rect.Rect(0, 0, 3, 3)
    inner = r.inner
    assert len(inner) == 2  # We should get a Tuple length 2
    assert inner[0] == slice(1, 2, None)  # x slice
    assert inner[1] == slice(1, 2, None)  # y slice


def test_Rect_inner_4x4_square_room():
    r = rect.Rect(0, 0, 4, 4)
    inner = r.inner
    assert len(inner) == 2  # We should get a Tuple length 2
    assert inner[0] == slice(1, 3, None)  # x slice
    assert inner[1] == slice(1, 3, None)  # y slice


def test_Rect_inner_4x3_square_room():
    r = rect.Rect(0, 0, 4, 3)
    inner = r.inner
    assert inner[0] == slice(1, 3, None)  # x slice
    assert inner[1] == slice(1, 2, None)  # y slice


def test_Rect_intersects_no_intersect_returns_False():
    r1 = rect.Rect(0, 0, 3, 3)
    r2 = rect.Rect(10, 10, 3, 3)
    assert r1.intersects(r2) is False
    assert r2.intersects(r1) is False


def test_Rect_intersects_both_rects_intersect_returns_True():
    r1 = rect.Rect(0, 0, 3, 3)
    r2 = rect.Rect(1, 1, 3, 3)
    assert r1.intersects(r2)
    assert r2.intersects(r1)


def test_Rect_perimeter_3x3_room():
    r = rect.Rect(0, 0, 3, 3)
    result = r.perimeter()
    assert result == {
        (0, 0), (1, 0), (2, 0),
        (0, 1), (2, 1),
        (0, 2), (1, 2), (2, 2),
    }


def test_Rect_perimeter_4x4_room():
    r = rect.Rect(0, 0, 4, 4)
    result = r.perimeter()
    assert result == {
        (0, 0), (1, 0), (2, 0), (3, 0),
        (0, 1), (3, 1),
        (0, 2), (3, 2),
        (0, 3), (1, 3), (2, 3), (3, 3)
    }


def test_horz_walls_3x3_room():
    r = rect.Rect(0, 0, 3, 3)
    result = r.horz_walls()
    assert result == [(1, 0), (1, 2)]


def test_horz_walls_4x4_room():
    r = rect.Rect(0, 0, 4, 4)
    result = r.horz_walls()
    assert result == [(1, 0), (2, 0), (1, 3), (2, 3)]


def test_vert_walls_3x3_room():
    r = rect.Rect(0, 0, 3, 3)
    result = r.vert_walls()
    assert result == [(0, 1), (2, 1)]


def test_vert_walls_4x4_room():
    r = rect.Rect(0, 0, 4, 4)
    result = r.vert_walls()
    assert result == [(0, 1), (0, 2), (3, 1), (3, 2)]


def test_Rect_random_point_inside__3x3_rect():
    r = rect.Rect(0, 0, 3, 3)
    result = r.random_point_inside()
    # Only one spot available!
    assert result == (1, 1)