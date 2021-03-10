""" Tests for item.py """
from components.item_comp import ItemComponent
from src.renderorder import RenderOrder
from src import entity
from src import item


def test_init__is_Entity():
    i = item.Item()
    assert isinstance(i, entity.Entity)


def test_init_default_components():
    i = item.Item()
    assert i.x == -1
    assert i.y == -1


def test_init_color():
    i = item.Item()
    assert i.color == (255, 255, 255)


def test_init_blocks_movement():
    i = item.Item()
    assert i.blocks_movement is False


def test_init_renderorder():
    i = item.Item()
    assert i.render_order == RenderOrder.ITEM


def test_init_itemcomp():
    i = item.Item()
    assert isinstance(i.item, ItemComponent)
