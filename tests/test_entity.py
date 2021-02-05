""" Tests for entity.py """
from components.fighter import Fighter
from src.entity import Entity
from src.renderorder import RenderOrder
import test_tools
import pytest


@pytest.fixture
def test_map():
    return test_tools.test_map()


def test_Entity_init__defaults():
    e = Entity()
    # assert e.parent is None
    assert e.x == 0
    assert e.y == 0
    assert e.char == '?'
    assert e.color == (255, 255, 255)
    assert e.name == '<Unnamed>'
    assert e.blocks_movement is False
    assert e.render_order == RenderOrder.CORPSE


def test_Entity_init__xy():
    e = Entity(x=1, y=2)
    assert e.x == 1
    assert e.y == 2


def test_Entity_init__char_and_color():
    e = Entity(char='@', color='white')
    assert e.char == '@'
    assert e.color == 'white'


def test_Entity_init__name():
    e = Entity(name='Player')
    assert e.name == 'Player'


def test_Entity_init__gamemap(test_map):
    e = Entity(parent=test_map)
    assert e.parent == test_map


def test_Entity_init__blocks_movement():
    e = Entity()
    assert e.blocks_movement is False


def test_Entity_init__renderorder():
    e = Entity()
    assert e.render_order == RenderOrder.CORPSE


def test_Entity_str__has_name():
    e = Entity(name='Player')
    assert str(e) == 'Player'


def test_Entity_str__unnamed():
    e = Entity()
    assert str(e) == '<Unnamed>'


def test_Entity_move():
    e = Entity(x=0, y=0)
    e.move(1, 1)
    assert e.x == 1
    assert e.y == 1


def test_Entity_spawn__creates_clone(test_map):
    e = Entity(name='cloner')
    result = e.spawn(test_map, 2, 3)
    # Should be a clone
    assert e.name == result.name

    # Not an exact clone thogh
    assert result != e
    assert result is not e


def test_Entity_spawn__not_exact_clone(test_map):
    e = Entity(name='cloner')
    result = e.spawn(test_map, 2, 3)
    assert result != e
    assert result is not e


def test_Entity_spawn__in_gamemap_entities(test_map):
    e = Entity()
    result = e.spawn(test_map, 2, 3)
    assert result in test_map.entities


def test_Entity_spawn__xy(test_map):
    e = Entity()
    result = e.spawn(test_map, 2, 3)
    assert result.x == 2
    assert result.y == 3


def test_Entity_place__no_gamemap():
    e = Entity()
    e.place(2, 3)
    assert e.x == 2
    assert e.y == 3


def test_Entity_place__gamemap__xy(test_map):
    e = Entity(x=0, y=0)
    e.place(2, 3, test_map)
    assert e.x == 2
    assert e.y == 3


def test_Entity_place__gamemap__in_entities(test_map):
    e = Entity(x=0, y=0)
    e.place(2, 3, test_map)
    assert e in test_map.entities


def test_Entity_place__gamemap(test_map):
    e = Entity(x=0, y=0)
    e.place(2, 3, test_map)
    assert e.gamemap == test_map


def test_Entity_distance__same_point():
    e = Entity(x=0, y=0)
    assert e.x == 0
    assert e.y == 0
    assert e.distance(0, 0) == 0


def test_Entity_distance__1_tile_away():
    e = Entity(x=0, y=0)
    assert e.distance(1, 0) == 1


def test_Entity_distance__1_diagonal_tile_away():
    e = Entity(x=0, y=0)
    result = e.distance(1, 1)
    result = round(result, 2)  # Round to 2 decimal places
    assert result == 1.41
