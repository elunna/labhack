import pytest
from new_entity import Entity


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


def test_Entity_move__to_a_negative_x():
    e = Entity(x=0, y=0, char='@', color=None, name='Player')
    with pytest.raises(ValueError):
        e.move(-1, 2)


def test_Entity_move__to_a_negative_y():
    e = Entity(x=0, y=0, char='@', color=None, name='Player')
    with pytest.raises(ValueError):
        e.move(1, -2)


def test_Entity_move__positive_values():
    e = Entity(x=0, y=0, char='@', color=None, name='Player')
    e.move(1, 2)
    assert e.x == 1
    assert e.y == 2


def test_Entity_move__negative_values():
    e = Entity(x=10, y=10, char='@', color=None, name='Player')
    e.move(-1, 2)
    assert e.x == 9
    assert e.y == 12
