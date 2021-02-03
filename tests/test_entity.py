""" Tests for entity.py """

import entity
import game_map
import pytest
import settings
import tile_types


@pytest.fixture
def open_map():
    m = game_map.GameMap(width=10, height=10)
    m.tiles[0:, 0:] = tile_types.floor
    return m


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


def test_Entity_str():
    e = entity.Entity()
    assert str(e) == "<Unnamed>"


def test_Entity_gamemap(open_map):
    # What if parent is not set?
    e = entity.Entity(parent=open_map)
    assert e.gamemap is open_map


def test_Entity_move():
    e = entity.Entity()
    e.move(1, 1)
    assert e.x == 1
    assert e.y == 1


def test_Entity_spawn__creates_clone(open_map):
    e = entity.Entity()
    result = e.spawn(open_map, 2, 3)
    # Should be a clone
    assert e.char == result.char
    assert e.color == result.color
    assert e.name == result.name
    assert e.blocks_movement == result.blocks_movement
    assert e.render_order == result.render_order

    # Not an exact clone thogh
    assert result != e
    assert result is not e


def test_Entity_spawn__in_gamemap_entities(open_map):
    e = entity.Entity()
    result = e.spawn(open_map, 2, 3)
    # Should be in the map at the coordinates
    assert result in open_map.entities
    assert result.x == 2
    assert result.y == 3


def test_Entity_place__no_gamemap():
    e = entity.Entity()
    e.place(2, 3)
    assert e.x == 2
    assert e.y == 3


def test_Entity_place__new_gamemap(open_map):
    e = entity.Entity()
    e.place(2, 3, open_map)
    assert e.x == 2
    assert e.y == 3
    assert e.gamemap == open_map
    assert e in open_map.entities


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
