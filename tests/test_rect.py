""" Tests for rectangle.py """

import pytest
import rectangle


def test_Rectangle_init():
    r = rectangle.Rectangle(0, 0, 3, 3)
    assert r


def test_Rectangle_init_x2():
    r = rectangle.Rectangle(0, 0, 5, 10)
    x2 = 5
    assert r.x2 == x2


def test_Rectangle_init_y2():
    r = rectangle.Rectangle(0, 0, 5, 10)
    y2 = 10
    assert r.y2 == y2


def test_Rectangle_init_negative_x_raises_ValueError():
    with pytest.raises(ValueError):
        rectangle.Rectangle(-2, 2, 2, 2)


def test_Rectangle_init_negative_y_raises_ValueError():
    with pytest.raises(ValueError):
        rectangle.Rectangle(2, -2, 2, 2)


def test_Rectangle_init_low_w_raises_ValueError():
    with pytest.raises(ValueError):
        rectangle.Rectangle(2, 2, 2, 3)


def test_Rectangle_init_low_h_raises_ValueError():
    with pytest.raises(ValueError):
        rectangle.Rectangle(2, 2, 3, 2)


def test_Rectangle_center():
    r = rectangle.Rectangle(0, 0, 3, 3)
    center = (1, 1)
    assert r.center == center


def test_Rectangle_inner_3x3_square_room():
    r = rectangle.Rectangle(0, 0, 3, 3)
    inner = r.inner
    assert len(inner) == 2  # We should get a Tuple length 2
    assert inner[0] == slice(1, 2, None)  # x slice
    assert inner[1] == slice(1, 2, None)  # y slice


def test_Rectangle_inner_4x4_square_room():
    r = rectangle.Rectangle(0, 0, 4, 4)
    inner = r.inner
    assert len(inner) == 2  # We should get a Tuple length 2
    assert inner[0] == slice(1, 3, None)  # x slice
    assert inner[1] == slice(1, 3, None)  # y slice


def test_Rectangle_inner_4x3_square_room():
    r = rectangle.Rectangle(0, 0, 4, 3)
    inner = r.inner
    assert inner[0] == slice(1, 3, None)  # x slice
    assert inner[1] == slice(1, 2, None)  # y slice


def test_Rectangle_intersects_no_intersect_returns_False():
    r1 = rectangle.Rectangle(0, 0, 3, 3)
    r2 = rectangle.Rectangle(10, 10, 3, 3)
    assert r1.intersects(r2) is False
    assert r2.intersects(r1) is False


def test_Rectangle_intersects_both_rects_intersect_returns_True():
    r1 = rectangle.Rectangle(0, 0, 3, 3)
    r2 = rectangle.Rectangle(1, 1, 3, 3)
    assert r1.intersects(r2)
    assert r2.intersects(r1)


# Not implemented yet.

# def test_Rectangle_within__valid_returns_True():
    # r1 = rectangle.Rectangle(0, 0, 3, 3)
    # x, y = 0, 0
    # assert r1.within(x, y)


# def test_Rectangle_within__invalid_returns_False():
    # r1 = rectangle.Rectangle(0, 0, 3, 3)
    # x, y = 3, 3
    # assert r1.within(x, y) is False
