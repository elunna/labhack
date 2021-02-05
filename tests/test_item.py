""" Tests for items.py """
from src.renderorder import RenderOrder
from src import entity
from src import item


def test_Item_subclass_of_Entity():
    i = item.Item()
    assert isinstance(i, entity.Entity)


def test_Item_init_defaults():
    i = item.Item()
    assert i.x == 0
    assert i.y == 0
    assert i.char == '?'
    assert i.color == (255, 255, 255)
    assert i.name == "<Unnamed>"
    assert i.consumable is None
    assert i.equippable is None
    assert i.blocks_movement is False
    assert i.render_order == RenderOrder.ITEM
