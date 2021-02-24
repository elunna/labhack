from src.door import Door
from src.room import Room
import pytest


def test_init__room():
    r = Room(0, 0, 3, 3)
    d = Door(r, 1, 0)
    assert d.room == r


def test_init__coords():
    r = Room(0, 0, 3, 3)
    d = Door(r, 1, 0)
    assert d.x == 1
    assert d.y == 0


def test_init__invalid_location__raises_exception():
    r = Room(0, 0, 3, 3)
    with pytest.raises(ValueError):
        Door(r, 0, 0)


def test_init__not_in_its_room_raises_exception():
    r = Room(0, 0, 3, 3)
    with pytest.raises(ValueError):
        Door(r, 100, 1000)


def test_facing_other__same_room():
    r = Room(0, 0, 3, 3)
    d1 = Door(r, 1, 0)
    d2 = Door(r, 2, 1)
    assert d1.facing_other(d2) is False


def test_facing_other__vertical():
    r1 = Room(0, 0, 3, 3)
    d1 = Door(r1, 1, 2)

    r2 = Room(0, 5, 4, 3)
    d2 = Door(r2, 1, 5)
    d3 = Door(r2, 2, 5)
    assert d1.facing_other(d2)  # Lined up vertically
    assert d2.facing_other(d1)  # Lined up vertically
    assert d1.facing_other(d3)  # Off by one
    assert d3.facing_other(d1)  # Off by one


def test_facing_other__horizontal():
    r1 = Room(0, 0, 3, 3)
    d1 = Door(r1, 2, 1)

    r2 = Room(5, 0, 3, 4)
    d2 = Door(r2, 5, 1)
    d3 = Door(r2, 5, 2)
    assert d1.facing_other(d2)  # Lined up horizontally
    assert d2.facing_other(d1)  # Lined up horizontally
    assert d1.facing_other(d3)  # Off by one
    assert d3.facing_other(d1)  # Off by one


def test_facing_other__facing_away_vertically():
    r1 = Room(0, 0, 3, 3)
    d1 = Door(r1, 1, 0)  # Facing N

    r2 = Room(0, 5, 4, 3)
    d2 = Door(r2, 1, 7)  # Facing S
    assert d1.facing_other(d2) is False  # Lined up vertically
    assert d2.facing_other(d1) is False  # Lined up vertically


def test_facing_other__facing_away_horizontally():
    r1 = Room(0, 0, 3, 3)
    d1 = Door(r1, 0, 1)  # Facing west

    r2 = Room(5, 0, 3, 4)
    d2 = Door(r2, 7, 1)  # Facing east
    assert d1.facing_other(d2) is False  # Lined up horizontally
    assert d2.facing_other(d1) is False  # Lined up horizontally


def test_facing_other__doors_lined_up_horizontally():
    # These doors do not share the same x-axis, there is 1 space between them,
    # but we need at least 2 spaces for them to be facing eachother.
    r1 = Room(0, 0, 3, 3)
    d1 = Door(r1, 2, 1)  # Facing east

    r2 = Room(3, 4, 3, 3)
    d2 = Door(r2, 3, 5)  # Facing west
    assert d1.facing_other(d2)
    assert d2.facing_other(d1)


def test_facing_other__doors_lined_up_vertically():
    # These doors do not share the same y-axis, there is 1 space between them,
    # but we need at least 2 spaces for them to be facing eachother.
    r1 = Room(0, 0, 3, 3)
    d1 = Door(r1, 1, 2)  # Facing south

    r2 = Room(4, 3, 3, 3)
    d2 = Door(r2, 5, 3)  # Facing north
    assert d1.facing_other(d2)
    assert d2.facing_other(d1)
