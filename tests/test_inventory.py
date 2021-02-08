""" Tests for inventory.py """

from components.component import Component
from components.inventory import Inventory
import pytest


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

# add item
# first letter is a
# seconds letter is b
# cannot add more than capacity

# rm_letter
# letter in items
# letter not in items

@pytest.mark.skip(reason='Needs item, etc.')
def test_Inventory_drop__invalid_item():
    i = Inventory(10)
    pass


@pytest.mark.skip(reason='Needs gamemap setup')
def test_Inventory_drop__valid_item():
    i = Inventory(10)

# sorted_dict
# Make sure it sorts a diverse inventory by group


# def test_LetterRoll__init():
# self.letters = 'abcdefghijklmnopqrstuvwxyz'
# index = -1
# first letter is a
# next letter is b
# build a roll from a-z then a
