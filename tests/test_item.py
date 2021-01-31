""" Tests for items.py """

import pytest
import items
import entity
from settings import RenderOrder


def test_Item_subclass_of_Entity():
    i = items.Item()
    assert isinstance (i, entity.Entity)


def test_Item_init_defaults():
    i = items.Item()
    assert i.x == 0
    assert i.y == 0
    assert i.char == '?'
    assert i.color == (255, 255, 255)
    assert i.name == "<Unnamed>"
    assert i.consumable is None
    assert i.equippable is None
    assert i.blocks_movement is False
    assert i.render_order == RenderOrder.ITEM
