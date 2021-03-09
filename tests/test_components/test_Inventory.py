""" Tests for inventory.py """
from src.entity_manager import EntityManager
from components.component import Component
from components.inventory import Inventory


def test_init__is_Component():
    i = Inventory(10)
    assert isinstance(i, Component)


def test_init__is_EntityManager():
    i = Inventory(10)
    assert isinstance(i, EntityManager)


def test_init__requires_item_components():
    i = Inventory(capacity=10)
    assert i.required_comp == "item"


def test_init__capacity():
    i = Inventory(capacity=10)
    assert i.capacity == 10
