import game_map
import pytest
import tile_types
from new_entity import Entity
from components.fighter import Fighter


@pytest.fixture
def open_map():
    m = game_map.GameMap(width=10, height=10)
    m.tiles[0:, 0:] = tile_types.floor
    return m

def test_Entity_init__defaults():
    e = Entity(x=0, y=0, char='@', color=None, name='Player')
    assert e.x == 0
    assert e.y == 0
    assert e.char == '@'
    assert e.color is None
    assert e.name == 'Player'


def test_Entity_init__components_dict():
    e = Entity(x=0, y=0)
    assert e.components == {'x': 0, 'y': 0}


@pytest.mark.skip(reason='implement after ecs is mostly done.')
def test_Entity_init__kwargs_become_components():
    pass


def test_Entity_str__has_name():
    e = Entity(x=0, y=0, char='@', color=None, name='Player')
    assert str(e) == 'Player'


def test_Entity_str__unnamed():
    e = Entity(x=0, y=0, char='@', color=None)
    assert str(e) == 'Unnamed'


def test_Entity_init__add_comp__1_kwarg():
    e = Entity(x=0, y=0, char='@', color=None, name='Player')
    e.add_comp(a=1)
    assert e.components['a'] == 1


def test_Entity_init__add_comp__2_kwargs():
    e = Entity(x=0, y=0, char='@', color=None, name='Player')
    e.add_comp(a=1, b=2)
    assert e.components['a'] == 1
    assert e.components['b'] == 2


def test_Entity_init__add_comp__already_exists_and_replaces():
    e = Entity(x=0, y=0, char='@', color=None, name='Player')
    e.add_comp(a=1)
    e.add_comp(a=2)
    assert e.components['a'] == 2


def test_Entity_init__has_comp():
    e = Entity(x=0, y=0)
    assert e.has_comp('x')
    assert e.has_comp('y')


def test_Entity_init__rm_comp__success_removes_component():
    e = Entity(x=0, y=0, char='@', color=None, name='Player')
    e.add_comp(a=1)
    e.rm_comp('a')
    assert 'a' not in e.components


def test_Entity_init__rm_comp__success_returns_True():
    e = Entity(x=0, y=0, char='@', color=None, name='Player')
    e.add_comp(a=1)
    result = e.rm_comp('a')
    assert result


def test_Entity_init__rm_comp__fail_returns_False():
    e = Entity(x=0, y=0, char='@', color=None, name='Player')
    e.rm_comp('z')
    # Raise exception?


def test_Entity_init__getattr__returns_component_value():
    e = Entity(x=0, y=0, char='@', color=None, name='Player')
    e.add_comp(a=1)
    assert e.a == 1


def test_Entity_init__getattr__DNE_returns_None():
    e = Entity(x=0, y=0, char='@', color=None, name='Player')
    with pytest.raises(AttributeError):
        result = e.a


def test_Entity_init__blocks_component():
    e = Entity(x=0, y=0, char='@', color=None, name='Player', blocks=True)

    assert e.blocks
    assert 'blocks' in e.components


def test_Entity__with_Fighter():
    e = Entity(
        name='Player',
        fighter=Fighter(hp=1, base_defense=2, base_power=3)
    )

    # Try all the different things with the Fighter components
    assert e.fighter.hp == 1
    assert e.fighter.base_defense == 2
    assert e.fighter.base_power == 3
    # assert "fighter" in e
    assert e.has_comp("fighter")
    e.rm_comp("fighter")
    assert not e.has_comp("fighter")



def test_Entity_gamemap(open_map):
    # What if parent is not set?
    e = Entity(parent=open_map)
    assert e.gamemap is open_map


def test_Entity_move():
    e = Entity(x=0, y=0)
    e.move(1, 1)
    assert e.x == 1
    assert e.y == 1


def test_Entity_spawn__creates_clone(open_map):
    e = Entity(name='cloner')
    result = e.spawn(open_map, 2, 3)
    # Should be a clone
    assert e.name == result.name

    # Not an exact clone thogh
    assert result != e
    assert result is not e


def test_Entity_spawn__in_gamemap_entities(open_map):
    e = Entity()
    result = e.spawn(open_map, 2, 3)
    # Should be in the map at the coordinates
    assert result in open_map.entities
    assert result.x == 2
    assert result.y == 3


def test_Entity_place__no_gamemap():
    e = Entity()
    e.place(2, 3)
    assert e.x == 2
    assert e.y == 3


def test_Entity_place__new_gamemap(open_map):
    e = Entity(x=0, y=0)
    e.place(2, 3, open_map)
    assert e.x == 2
    assert e.y == 3
    assert e.gamemap == open_map
    assert e in open_map.entities


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
