""" Tests for inventory.py """

from .component import Component
from .inventory import Inventory
from src import factory
import pytest


@pytest.fixture
def sword():
    return factory.make('sword')


@pytest.fixture
def dagger():
    return factory.make('dagger')


def test_init__is_BaseComponent():
    i = Inventory(10)
    assert isinstance(i, Component)


def test_init():
    i = Inventory(10)
    assert i.capacity == 10
    assert i.items == {}


def test_init__first_inv_letter_is_a():
    i = Inventory(10)
    assert i.current_letter == 'a'


def test_add_item__success_returns_True(sword):
    i = Inventory(10)
    assert i.add_item(sword)


def test_add_item__sets_parent_on_item(sword):
    i = Inventory(10)
    i.add_item(sword)
    assert sword.parent == i


def test_add_item__letter1_is_a(sword):
    i = Inventory(10)
    i.add_item(sword)
    assert i.items['a'] == sword


def test_add_item__letter2_is_a(sword, dagger):
    i = Inventory(10)
    i.add_item(sword)
    i.add_item(dagger)
    assert i.items['b'] == dagger


def test_add_item__over_capacity_returns_False(sword, dagger):
    i = Inventory(1)
    i.add_item(sword)
    assert i.add_item(dagger) is False
    assert 'b' not in i.items


def test_rm_item__success_returns_True(sword):
    i = Inventory(10)
    i.add_item(sword)
    assert i.rm_item(sword)


def test_rm_item__item_removed(sword):
    i = Inventory(10)
    i.add_item(sword)
    i.rm_item(sword)
    assert sword not in i.items.values()


def test_rm_item__resets_item_parent(sword):
    i = Inventory(10)
    i.add_item(sword)
    i.rm_item(sword)
    assert sword.parent is None


def test_rm_item__failure_returns_False(sword):
    i = Inventory(10)
    i.add_item(sword)
    assert i.rm_item('dagger') is False


def test_rm_letter__success_returns_True(sword):
    i = Inventory(10)
    i.add_item(sword)
    assert i.rm_letter('a')


def test_rm_letter__item_removed(sword):
    i = Inventory(10)
    i.add_item(sword)
    i.rm_letter('a')
    assert 'a' not in i.items


def test_rm_letter__resets_item_parent(sword):
    i = Inventory(10)
    i.add_item(sword)
    i.rm_letter('a')
    assert sword.parent is None


def test_rm_letter__failure_returns_false(sword):
    i = Inventory(10)
    i.add_item(sword)
    assert i.rm_letter('b') is False


def test_sorted_dict__one_item(dagger):
    i = Inventory(10)
    i.add_item(dagger)
    result = i.sorted_dict()
    assert result == {'/': ['a']}


def test_sorted_dict__multiple_items():
    i = Inventory(10)
    i.add_item(factory.dagger)
    i.add_item(factory.leather_vest)
    i.add_item(factory.bulletproof_vest)
    i.add_item(factory.health_potion)
    result = i.sorted_dict()
    assert result == {
        '/': ['a'],
        '[': ['b', 'c'],
        '!': ['d'],
    }
