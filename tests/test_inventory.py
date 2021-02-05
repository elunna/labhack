""" Tests for inventory.py """

from components.base_component import BaseComponent
from components.inventory import Inventory
import pytest


def test_Inventory_is_BaseComponent():
    i = Inventory(10)
    assert isinstance(i, BaseComponent)


def test_Inventory_init():
    i = Inventory(10)
    assert i.capacity == 10
    assert i.items == []


@pytest.mark.skip(reason='Needs item, etc.')
def test_Inventory_drop__invalid_item():
    i = Inventory(10)
    pass


@pytest.mark.skip(reason='Needs gamemap setup')
def test_Inventory_drop__valid_item():
    i = Inventory(10)
