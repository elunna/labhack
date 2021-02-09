import src.item_data
from . import actions
from .drop import DropAction
from .useitem import ItemAction
from src import factory
from src import exceptions
from tests import toolkit
import pytest


@pytest.fixture
def test_map():
    return toolkit.test_map()


def test_DropItem_is_Action(test_map):
    player = test_map.get_player()
    potion = src.item_data.health_potion
    a = DropAction(entity=player, item=potion)
    assert isinstance(a, actions.Action)


def test_DropItem_is_ItemAction(test_map):
    player = test_map.get_player()
    potion = src.item_data.health_potion
    a = DropAction(entity=player, item=potion)
    assert isinstance(a, ItemAction)


def test_DropItem_init(test_map):
    player = test_map.get_player()
    potion = src.item_data.health_potion
    a = DropAction(entity=player, item=potion)
    assert a.entity == player
    assert a.item == potion


def test_DropItem_perform__item_leaves_inventory(test_map):
    player = test_map.get_player()
    item = player.inventory.items.get('a')  # Need the actual item from inv
    assert item.name == "Dagger"

    a = DropAction(entity=player, item=item)
    result = a.perform()
    assert item not in player.inventory.items


def test_DropItem_perform__item_appears_on_map(test_map):
    player = test_map.get_player()
    item = player.inventory.items.get('a')  # Need the actual item from inv
    assert item.name == "Dagger"

    a = DropAction(entity=player, item=item)
    result = a.perform()
    assert item in test_map.get_items_at(player.x, player.y)


def test_DropItem_perform__msg(test_map):
    player = test_map.get_player()
    item = player.inventory.items.get('a')  # Need the actual item from inv
    assert item.name == "Dagger"

    a = DropAction(entity=player, item=item)
    result = a.perform()
    assert a.msg == f"You dropped the {item.name}."


def test_DropItem_perform__invalid_item_raises_Impossible(test_map):
    player = test_map.get_player()
    a = DropAction(entity=player, item=src.item_data.sword)

    with pytest.raises(exceptions.Impossible):
        a.perform()


def test_DropItem_perform__equipped_item(test_map):
    player = test_map.get_player()
    item = player.inventory.items.get('a')  # Need the actual item from inv
    assert item.name == "Dagger"
    player.equipment.toggle_equip(item)
    assert player.equipment.item_is_equipped(item)

    a = DropAction(entity=player, item=item)
    result = a.perform()

    assert not player.equipment.item_is_equipped(item)