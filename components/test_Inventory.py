""" Tests for inventory.py """
from src.entity import Entity
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


def test_add_item__only_accept_Items():
    i = Inventory(10)
    assert i.add_item('x') is False


def test_add_item__must_have_ItemComponent():
    i = Inventory(10)
    assert i.add_item(Entity(name="test entity")) is False


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


def test_add_item__sets_letter_on_item_component(plunger):
    i = Inventory(1)
    i.add_item(plunger)
    assert i.items['a'] == plunger
    assert plunger.item.last_letter == 'a'


def test_add_item__uses_last_letter_from_item_component(plunger):
    i = Inventory(1)
    plunger.item.last_letter = 'z'
    i.add_item(plunger)
    assert i.items['z'] == plunger


def test_add_item__last_letter_not_available(plunger, dagger):
    i = Inventory(2)
    dagger.item.last_letter = 'a'
    i.add_item(plunger)
    i.add_item(dagger)
    assert i.items['b'] == dagger
    assert dagger.item.last_letter == 'b'  # Resets the last letter


def test_add_item__one_stackable__adds_to_stack(dagger):
    i = Inventory(2)
    i.add_item(dagger)
    i.add_item(dagger)
    assert dagger.item.stacksize == 2  # Same ref work?
    assert i.items['a'].item.stacksize == 2  # Which check is more accurate?


def test_add_item__one_stackable__capacity_unchanged(dagger):
    i = Inventory(2)
    i.add_item(dagger)
    expected = len(i.items)
    i.add_item(dagger)
    assert len(i.items) == expected


def test_add_item__stackable__full_capacity(dagger):
    i = Inventory(1)
    i.add_item(dagger)
    assert i.add_item(dagger)
    assert dagger.item.stacksize == 2  # Same ref work?
    assert i.items['a'].item.stacksize == 2  # Which check is more accurate?


def test_rm_item__stackable__sets_last_letter(dagger):
    i = Inventory(10)
    dagger.item.stacksize = 10
    i.add_item(dagger)
    assert dagger.item.last_letter == 'a'


def test_rm_item__success_returns_the_item(plunger):
    i = Inventory(10)
    i.add_item(plunger)
    result = i.rm_item(plunger)
    assert result == plunger


def test_rm_item__item_removed(plunger):
    i = Inventory(10)
    i.add_item(plunger)
    i.rm_item(plunger)
    assert plunger not in i.items.values()


def test_rm_item__resets_item_parent(plunger):
    i = Inventory(10)
    i.add_item(plunger)
    result = i.rm_item(plunger)
    assert result.parent is None


def test_rm_item__failure_returns_False(plunger):
    i = Inventory(10)
    i.add_item(plunger)
    assert i.rm_item('dagger') is None


def test_rm_item__stackable__single(dagger):
    i = Inventory(10)
    dagger.item.stacksize = 10
    i.add_item(dagger)
    assert dagger.item.stacksize == 10
    i.rm_item(dagger)
    assert dagger.item.stacksize == 9


def test_rm_item__stackable__multiple__adjusts_stacksize(dagger):
    i = Inventory(10)
    dagger.item.stacksize = 10
    i.add_item(dagger)
    assert dagger.item.stacksize == 10
    i.rm_item(dagger, 2)
    assert dagger.item.stacksize == 8


def test_rm_item__stackable__multiple__returns_stackable(dagger):
    i = Inventory(10)
    dagger.item.stacksize = 10
    i.add_item(dagger)
    assert dagger.item.stacksize == 10
    result = i.rm_item(dagger, 2)
    assert result.item.stacksize == 2


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
    i.add_item(factory.make("healing vial"))
    result = i.sorted_dict()
    assert result == {
        '/': ['a'],
        '[': ['b', 'c'],
        '!': ['d'],
    }

# This should probably have rigorous testing - items could differ by non-significant details:
# x, y should not matter, but all the other components should match.


def test_get_matching_item__has_match(dagger, plunger):
    i = Inventory(10)
    i.add_item(dagger)
    i.add_item(plunger)

    p = factory.make('plunger')
    assert i.get_matching_item(p) == plunger
    # assert i.get_matching_item(p) == p


def test_get_matching_item__no_match(dagger, plunger):
    i = Inventory(10)
    i.add_item(dagger)
    assert i.get_matching_item(plunger) is None
