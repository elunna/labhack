""" Tests for tiles.py """
from src import tiles
import numpy
import pytest

"""
>>> pprint(floor)
array(
    (True, True,
        (32, [255, 255, 255], [ 50,  50, 150]),
        (32, [255, 255, 255], [200, 180,  50])
    ),
    dtype=[
        ('walkable', '?'),
        ('transparent', '?'),
        ('dark',
            [
                ('ch', '<i4'), ('fg', 'u1', (3,)), ('bg', 'u1', (3,))
            ]
        ),
        ('light',
            [('ch', '<i4'), ('fg', 'u1', (3,)), ('bg', 'u1', (3,))])
        ])
"""


def test_graphic_dt():
    gdt = tiles.graphic_dt
    assert isinstance(gdt, numpy.dtype)


def test_tile_dt():
    tdt = tiles.tile_dt
    assert isinstance(tdt, numpy.dtype)


""" Test new_tile using the already constructed dtiles"""


def test_SHROUD():
    shroud = tiles.SHROUD
    assert isinstance(shroud, numpy.ndarray)
    assert shroud.size == 1
    assert shroud.itemsize == 10
    assert shroud.shape == ()

# Can't do this
# def test_SHROUD__walkable():
    # shroud = tile_types.SHROUD
    # assert shroud['walkable']


# Can't do this
# def test_SHROUD__transparent():
    # shroud = tile_types.SHROUD
    # assert not shroud['transparent']


def test_new_tile__floor():
    floor = tiles.floor
    assert isinstance(floor, numpy.ndarray)
    assert floor.size == 1
    assert floor.itemsize == 22
    assert floor.shape == ()


def test_new_tile__floor__walkable():
    floor = tiles.floor
    assert floor['walkable']


def test_new_tile__floor__transparent():
    floor = tiles.floor
    assert floor['transparent']


def test_new_tile__wall():
    wall = tiles.wall
    assert isinstance(wall, numpy.ndarray)
    assert wall.size == 1
    assert wall.itemsize == 22
    assert wall.shape == ()


def test_new_tile__wall__not_walkable():
    wall = tiles.wall
    assert not wall['transparent']


def test_new_tile__wall__not_transparent():
    wall = tiles.wall
    assert not wall['walkable']


def test_new_tile__stairs():
    stairs = tiles.down_stairs
    assert isinstance(stairs, numpy.ndarray)
    assert stairs.size == 1
    assert stairs.itemsize == 22
    assert stairs.shape == ()


def test_new_tile__stairs__walkable():
    stairs = tiles.down_stairs
    assert stairs['walkable']


def test_new_tile__stairs__transparent():
    stairs = tiles.down_stairs
    assert stairs['transparent']
