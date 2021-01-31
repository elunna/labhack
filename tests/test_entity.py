""" Tests for entity.py """

import entity
import pytest
import settings


def test_Entity_init_defaults():
    e = entity.Entity()
    # assert e.parent is None  # Not set
    assert e.x == 0
    assert e.y == 0
    assert e.char == '?'
    assert e.color == (255, 255, 255)
    assert e.name == '<Unnamed>'
    assert e.blocks_movement is False
    assert e.render_order == settings.RenderOrder.CORPSE


@pytest.mark.skip(reason='need map fixture')
def test_Entity_gamemap():
    # What if parent is not set?
    e = entity.Entity()
    assert e.gamemap is None


def test_Entity_move():
    e = entity.Entity()
    e.move(1, 1)
    assert e.x == 1
    assert e.y == 1


@pytest.mark.skip(reason='need map fixture')
def test_Entity_spawn():
    pass


@pytest.mark.skip(reason='need map fixture')
def test_Entity_place():
    pass


def test_Entity_distance__same_point():
    e = entity.Entity()
    assert e.x == 0
    assert e.y == 0
    assert e.distance(0, 0) == 0


def test_Entity_distance__1_tile_away():
    e = entity.Entity()
    assert e.distance(1, 0) == 1


def test_Entity_distance__1_diagonal_tile_away():
    e = entity.Entity()
    result = e.distance(1, 1)
    result = round(result, 2)  # Round to 2 decimal places
    assert result == 1.41
