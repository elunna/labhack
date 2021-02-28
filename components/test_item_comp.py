import pytest
from .item_comp import ItemComponent
from .component import Component


@pytest.fixture
def test_item():
    return ItemComponent()


def test_init__is_Component(test_item):
    assert isinstance(test_item, Component)


def test_init__stackable__False_by_default(test_item):
    assert test_item.stackable is False


def test_init__stackable_arg():
    i = ItemComponent(stackable=True)
    assert i.stackable


def test_init__breakable__0_by_default(test_item):
    assert test_item.breakable == 0


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


def test_init__last_letter__None_by_default(test_item):
    assert test_item.last_letter is None


