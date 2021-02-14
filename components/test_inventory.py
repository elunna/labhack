""" Tests for inventory.py """

from .component import Component
from .inventory import Inventory
from .inventory import LetterRoll
from src import factory
import pytest

@pytest.fixture
def sword():
    return factory.make('sword')


@pytest.fixture
def dagger():
    return factory.make('dagger')


def test_Inventory_is_BaseComponent():
    i = Inventory(10)
    assert isinstance(i, Component)


def test_Inventory_init():
    i = Inventory(10)
    assert i.capacity == 10
    assert i.items == {}


def test_Inventory_init__first_inv_letter_is_a():
    i = Inventory(10)
    assert i.current_letter == 'a'


def test_Inventory_add_item__success_returns_True(sword):
    i = Inventory(10)
    assert i.add_item(sword)


def test_Inventory_add_item__sets_parent_on_item(sword):
    i = Inventory(10)
    i.add_item(sword)
    assert sword.parent == i


def test_Inventory_add_item__letter1_is_a(sword):
    i = Inventory(10)
    i.add_item(sword)
    assert i.items['a'] == sword


def test_Inventory_add_item__letter2_is_a(sword, dagger):
    i = Inventory(10)
    i.add_item(sword)
    i.add_item(dagger)
    assert i.items['b'] == dagger


def test_Inventory_add_item__over_capacity_returns_False(sword, dagger):
    i = Inventory(1)
    i.add_item(sword)
    assert i.add_item(dagger) is False
    assert 'b' not in i.items


def test_Inventory_rm_item__success_returns_True(sword):
    i = Inventory(10)
    i.add_item(sword)
    assert i.rm_item(sword)


def test_Inventory_rm_item__item_removed(sword):
    i = Inventory(10)
    i.add_item(sword)
    i.rm_item(sword)
    assert sword not in i.items.values()


def test_Inventory_rm_item__resets_item_parent(sword):
    i = Inventory(10)
    i.add_item(sword)
    i.rm_item(sword)
    assert sword.parent is None


def test_Inventory_rm_item__failure_returns_False(sword):
    i = Inventory(10)
    i.add_item(sword)
    assert i.rm_item('dagger') is False


def test_Inventory_rm_letter__success_returns_True(sword):
    i = Inventory(10)
    i.add_item(sword)
    assert i.rm_letter('a')


def test_Inventory_rm_letter__item_removed(sword):
    i = Inventory(10)
    i.add_item(sword)
    i.rm_letter('a')
    assert 'a' not in i.items


def test_Inventory_rm_letter__resets_item_parent(sword):
    i = Inventory(10)
    i.add_item(sword)
    i.rm_letter('a')
    assert sword.parent is None


def test_Inventory_rm_letter__failure_returns_false(sword):
    i = Inventory(10)
    i.add_item(sword)
    assert i.rm_letter('b') is False


def test_Inventory_sorted_dict__one_item(dagger):
    i = Inventory(10)
    i.add_item(dagger)
    result = i.sorted_dict()
    assert result == {'/': ['a']}


def test_Inventory_sorted_dict__multiple_items():
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


def test_LetterRoll__init():
    lr = LetterRoll()
    assert lr.letters == 'abcdefghijklmnopqrstuvwxyz'


def test_LetterRoll__init_index():
    lr = LetterRoll()
    assert lr.index == -1


def test_LetterRoll__size():
    lr = LetterRoll()
    assert len(lr) == 26


def test_LetterRoll__next_letter__1_is_a():
    lr = LetterRoll()
    assert lr.next_letter() == 'a'


def test_LetterRoll__next_letter__2_is_a():
    lr = LetterRoll()
    lr.next_letter()
    assert lr.next_letter() == 'b'


def test_LetterRoll__next_letter__roll_repeats():
    lr = LetterRoll()
    roll = ''.join([lr.next_letter() for x in range(27)])
    assert roll[-4:] == 'xyza'

