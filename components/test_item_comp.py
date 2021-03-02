import pytest

from src.entity import Entity
from .item_comp import ItemComponent
from .component import Component


@pytest.fixture
def itemcomp():
    return ItemComponent()


@pytest.fixture
def testitem():
    e = Entity(name="fleepgork", item=ItemComponent())
    e.item.stacksize = 10
    return e


def test_init__is_Component(itemcomp):
    assert isinstance(itemcomp, Component)


def test_init__breakable__0_by_default(itemcomp):
    assert itemcomp.breakable == 0


def test_init__breakable_arg():
    i = ItemComponent(breakable=25)
    assert i.breakable == 25


def test_init__last_letter__None_by_default(itemcomp):
    assert itemcomp.last_letter is None
