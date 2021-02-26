import pytest
from .item_comp import ItemComponent
from .component import Component


@pytest.fixture
def test_item():
    return ItemComponent(appearance='blue', weight=10, material='plastic')


def test_init__is_Component(test_item):
    assert isinstance(test_item, Component)


def test_init__appearance(test_item):
    assert test_item.appearance == 'blue'


def test_init__weight(test_item):
    assert test_item.weight == 10


def test_init__material(test_item):
    assert test_item.material == 'plastic'


def test_init__stackable__False_by_default(test_item):
    assert test_item.stackable is False


def test_init__stackable_arg():
    i = ItemComponent('blue', 10, 'plastic', stackable=True)
    assert i.stackable


def test_init__breakable__0_by_default(test_item):
    assert test_item.breakable == 0


def test_init__breakable_arg():
    i = ItemComponent('blue', 10, 'plastic', breakable=25)
    assert i.breakable == 25


def test_init__last_letter__None_by_default(test_item):
    assert test_item.last_letter is None
