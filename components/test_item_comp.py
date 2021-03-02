import pytest

from src.entity import Entity
from .item_comp import ItemComponent
from .component import Component
from src import exceptions


@pytest.fixture
def itemcomp():
    return ItemComponent()


@pytest.fixture
def testitem():
    e = Entity(name="fleepgork", item=ItemComponent(stackable=True))
    e.item.stacksize = 10
    return e


def test_init__is_Component(itemcomp):
    assert isinstance(itemcomp, Component)


def test_init__stackable__False_by_default(itemcomp):
    assert itemcomp.stackable is False


def test_init__stackable_arg():
    i = ItemComponent(stackable=True)
    assert i.stackable


def test_init__breakable__0_by_default(itemcomp):
    assert itemcomp.breakable == 0


def test_init__breakable_arg():
    i = ItemComponent(breakable=25)
    assert i.breakable == 25


def test_init__stacksize_always_starts_as_1():
    i = ItemComponent()
    assert i.stacksize == 1


@pytest.mark.skip
def test_init__set_stacksize_when_stackable():
    i = ItemComponent(stackable=True)
    i.stacksize = 10
    assert i.stacksize == 10


@pytest.mark.skip
def test_init__set_stacksize_when_not_stackable():
    i = ItemComponent(stackable=False)
    with pytest.raises(ValueError):
        i.stacksize = 3


def test_init__last_letter__None_by_default(itemcomp):
    assert itemcomp.last_letter is None


def test_merge_stack__not_stackable__raises_Impossible():
    i = ItemComponent(stackable=False)
    with pytest.raises(exceptions.Impossible):
        i.merge_stack('fake stack')

# def test_merge_stack__identical_Item__returns_True():
# def test_merge_stack__identical_Item__adds_to_stack():
# def test_merge_stack__identical_Item__destroy_other_stack():
# def test_merge_stack__different_Item__returns_False():


def test_split_stack__not_stackable__raises_Impossible():
    i = ItemComponent(stackable=False)
    with pytest.raises(exceptions.Impossible):
        i.split_stack(1)


def test_split_stack__0_qty__raises_ValueError(testitem):
    with pytest.raises(ValueError):
        testitem.item.split_stack(0)


def test_split_stack__partial__returns_copied_Item(testitem):
    assert testitem.item.stacksize == 10
    result = testitem.item.split_stack(1)
    # Is the item the same type? Name?
    assert result.name == testitem.name


def test_split_stack__partial__stacksize_depleted(testitem):
    assert testitem.item.stacksize == 10
    testitem.item.split_stack(1)
    assert testitem.item.stacksize == 9


def test_split_stack__partial__copy_stacksize(testitem):
    assert testitem.item.stacksize == 10
    result = testitem.item.split_stack(1)
    assert result.item.stacksize == 1


def test_split_stack__full__stacksize_depleted(testitem):
    assert testitem.item.stacksize == 10
    result = testitem.item.split_stack(10)
    assert result
    assert testitem.item.stacksize == 0


def test_split_stack__more_than_stacksize__raises_ValueError(testitem):
    assert testitem.item.stacksize == 10
    with pytest.raises(ValueError):
        testitem.item.split_stack(11)


def test_deplete_stack__not_stackable__raises_Impossible():
    i = ItemComponent(stackable=False)
    with pytest.raises(exceptions.Impossible):
        i.deplete_stack(1)


def test_deplete_stack__0_qty__raises_ValueError():
    i = ItemComponent(stackable=True)
    with pytest.raises(ValueError):
        i.deplete_stack(0)


def test_deplete_stack__partial():
    i = ItemComponent(stackable=True)
    i.stacksize = 2
    i.deplete_stack(1)
    assert i.stacksize == 1


def test_deplete_stack__success_returns_True():
    i = ItemComponent(stackable=True)
    i.stacksize = 2
    assert i.deplete_stack(1)


def test_deplete_stack__more_than_stacksize__raises_ValueError():
    i = ItemComponent(stackable=True)
    assert i.stacksize == 1
    with pytest.raises(ValueError):
        i.deplete_stack(2)


# def test_deplete_stack__full__destroys_item():