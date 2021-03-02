import pytest

from components.stackable import StackableComponent
from src.entity import Entity
import toolkit


@pytest.fixture
def test_map():
    return toolkit.test_map()


def test_init__defaults__always_has_parent_component():
    e = Entity()
    assert e.parent is None


def test_init__components_dict():
    e = Entity(x=0, y=0)
    assert e.components == {'parent': None, 'x': 0, 'y': 0}


def test_str__has_name():
    e = Entity(name='Player')
    assert str(e) == 'Player'


def test_str__unnamed():
    e = Entity(x=0, y=0)
    assert str(e) == 'Unnamed'


def test_equals__same_entity__True():
    e = Entity(x=0, y=0)
    assert e == e
    assert e is e


def test_is_similar__same_components__True():
    e = Entity(name="dart", x=0, y=0)
    f = Entity(name="dart", x=0, y=0)
    assert e.is_similar(f)


def test_is_similar__same_components_diff_values__False():
    e = Entity(name="dart", x=0, y=1)
    f = Entity(name="dart", x=0, y=0)
    assert not e.is_similar(f)


def test_is_similar__different_stacksizes__True():
    e = Entity(name="dart", x=0, y=0, stackable=StackableComponent(5))
    f = Entity(name="dart", x=0, y=0, stackable=StackableComponent(1))
    assert e.is_similar(f)


def test_add_comp__1_kwarg():
    e = Entity(x=0)
    e.add_comp(y=1)
    assert e.components['y'] == 1


def test_add_comp__2_kwargs():
    e = Entity(x=0, y=1)
    e.add_comp(a=1, b=2)
    assert e.components['a'] == 1
    assert e.components['b'] == 2


def test_add_comp__already_exists_and_replaces():
    e = Entity(x=0, y=1)
    e.add_comp(x=1)
    e.add_comp(x=2)
    assert e.components['x'] == 2


def test_contains__init_args():
    e = Entity(x=0, y=1)
    assert 'x' in e
    assert 'y' in e


def test_rm_comp__success_removes_component():
    e = Entity(x=0, y=1)
    e.rm_comp('x')
    assert 'x' not in e.components


def test_rm_comp__success_returns_True():
    e = Entity(x=0, y=1)
    result = e.rm_comp('x')
    assert result


def test_rm_comp__fail_returns_False():
    e = Entity(x=0, y=1)
    assert e.rm_comp('z') is False
    # Raise exception?


def test_has_comp():
    e = Entity(x=0, y=1)
    assert e.has_comp('x')
    assert e.has_comp('y')


def test_has_compval__single_kwarg():
    e = Entity(x=0, y=1)
    assert e.has_compval(x=0)
    assert e.has_compval(y=1)


def test_has_compval__multiple_kwargs():
    e = Entity(x=0, y=1)
    assert e.has_compval(x=0, y=1)


def test_has_compval__invalid_component():
    e = Entity(x=0, y=1)
    assert e.has_compval(z=3) is False


def test_getattr__returns_component_value():
    e = Entity(x=0, y=1)
    assert e.x == 0


def test_getattr__DNE_returns_None():
    e = Entity(x=0, y=0)
    with pytest.raises(AttributeError):
        result = e.z


def test_move():
    e = Entity(x=0, y=0)
    e.move(1, 1)
    assert e.x == 1
    assert e.y == 1


def test_distance__same_point():
    e = Entity(x=0, y=0)
    assert e.x == 0
    assert e.y == 0
    assert e.distance(0, 0) == 0


def test_distance__1_tile_away():
    e = Entity(x=0, y=0)
    assert e.distance(1, 0) == 1


def test_distance__1_diagonal_tile_away():
    e = Entity(x=0, y=0)
    result = e.distance(1, 1)
    result = round(result, 2)  # Round to 2 decimal places
    assert result == 1.41
