import pytest
from src.entity import Entity
from .component import Component
from src import exceptions
from .stackable import StackableComponent


@pytest.fixture
def stackcomp():
    return StackableComponent()


@pytest.fixture
def testitem():
    e = Entity(name="fleepgork", stackable=StackableComponent(10))
    e.stackable.size = 10
    return e


def test_init__is_Component(stackcomp):
    assert isinstance(stackcomp, Component)


def test_init__size_default_1():
    s = StackableComponent()
    assert s.size == 1


def test_init__size_arg():
    s = StackableComponent(size=5)
    assert s.size == 5


def test_merge_stack__success_returns_True(testitem):
    e = Entity(name="fleepgork", stackable=StackableComponent(1))
    assert testitem.stackable.merge_stack(e)


def test_merge_stack__default_full_stack(testitem):
    e = Entity(name="fleepgork", stackable=StackableComponent(5))
    testitem.stackable.merge_stack(e)
    assert testitem.stackable.size == 15
    assert e.stackable.size == 0


def test_merge_stack__default_full_stack__reversed(testitem):
    e = Entity(name="fleepgork", stackable=StackableComponent(5))
    e.stackable.merge_stack(testitem)
    assert testitem.stackable.size == 0
    assert e.stackable.size == 15


def test_merge_stack__qty_arg(testitem):
    e = Entity(name="fleepgork", stackable=StackableComponent(5))
    testitem.stackable.merge_stack(e, 3)
    assert testitem.stackable.size == 13
    assert e.stackable.size == 2


@pytest.mark.skip
def test_merge_stack__different_Item__returns_False(testitem):
    e = Entity(name="floob", stackable=StackableComponent(1))
    assert testitem.stackable.merge_stack(e) is False


def test_split_stack__0_qty__raises_ValueError(testitem):
    with pytest.raises(ValueError):
        testitem.stackable.split_stack(0)


def test_split_stack__partial__returns_copied_Item(testitem):
    assert testitem.stackable.size == 10
    result = testitem.stackable.split_stack(1)
    # Is the item the same type? Name?
    assert result.name == testitem.name


def test_split_stack__partial__stacksize_depleted(testitem):
    assert testitem.stackable.size == 10
    testitem.stackable.split_stack(1)
    assert testitem.stackable.size == 9


def test_split_stack__partial__copy_stacksize(testitem):
    assert testitem.stackable.size == 10
    result = testitem.stackable.split_stack(1)
    assert result.stackable.size == 1


def test_split_stack__full__stacksize_depleted(testitem):
    assert testitem.stackable.size == 10
    result = testitem.stackable.split_stack(10)
    assert result
    assert testitem.stackable.size == 0


def test_split_stack__more_than_stacksize__raises_ValueError(testitem):
    assert testitem.stackable.size == 10
    with pytest.raises(ValueError):
        testitem.stackable.split_stack(11)