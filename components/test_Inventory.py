""" Tests for inventory.py """
from .component import Component
from .inventory import Inventory
from src import factory
import pytest


@pytest.fixture
def plunger():
    return factory.make('plunger')


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


def test_add_item__success_returns_True(plunger):
    i = Inventory(10)
    assert i.add_item(plunger)


def test_add_item__sets_parent_on_item(plunger):
    i = Inventory(10)
    i.add_item(plunger)
    assert plunger.parent == i


def test_add_item__letter1_is_a(plunger):
    i = Inventory(10)
    i.add_item(plunger)
    assert i.items['a'] == plunger


def test_add_item__letter2_is_a(plunger, dagger):
    i = Inventory(10)
    i.add_item(plunger)
    i.add_item(dagger)
    assert i.items['b'] == dagger


def test_add_item__over_capacity_returns_False(plunger, dagger):
    i = Inventory(1)
    i.add_item(plunger)
    assert i.add_item(dagger) is False
    assert 'b' not in i.items


def test_rm_item__success_returns_True(plunger):
    i = Inventory(10)
    i.add_item(plunger)
    assert i.rm_item(plunger)


def test_rm_item__item_removed(plunger):
    i = Inventory(10)
    i.add_item(plunger)
    i.rm_item(plunger)
    assert plunger not in i.items.values()


def test_rm_item__resets_item_parent(plunger):
    i = Inventory(10)
    i.add_item(plunger)
    i.rm_item(plunger)
    assert plunger.parent is None


def test_rm_item__failure_returns_False(plunger):
    i = Inventory(10)
    i.add_item(plunger)
    assert i.rm_item('dagger') is False


def test_rm_letter__success_returns_True(plunger):
    i = Inventory(10)
    i.add_item(plunger)
    assert i.rm_letter('a')


def test_rm_letter__item_removed(plunger):
    i = Inventory(10)
    i.add_item(plunger)
    i.rm_letter('a')
    assert 'a' not in i.items


def test_rm_letter__resets_item_parent(plunger):
    i = Inventory(10)
    i.add_item(plunger)
    i.rm_letter('a')
    assert plunger.parent is None


def test_rm_letter__failure_returns_false(plunger):
    i = Inventory(10)
    i.add_item(plunger)
    assert i.rm_letter('b') is False


def test_sorted_dict__one_item(dagger):
    i = Inventory(10)
    i.add_item(dagger)
    result = i.sorted_dict()
    assert result == {'/': ['a']}


def test_sorted_dict__multiple_items():
    i = Inventory(10)
    i.add_item(factory.make("dagger"))
    i.add_item(factory.make("leather vest"))
    i.add_item(factory.make("bulletproof vest"))
    i.add_item(factory.make("vial of healing"))
    result = i.sorted_dict()
    assert result == {
        '/': ['a'],
        '[': ['b', 'c'],
        '!': ['d'],
    }
