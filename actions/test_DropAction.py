from . import actions
from .drop_action import DropAction
from .item_action import ItemAction
from src import factory
from src import exceptions
from tests import toolkit
import pytest


@pytest.fixture
def test_map():
    return toolkit.test_map()


@pytest.fixture
def potion():
    return factory.make("health potion")


def test_is_Action(test_map, potion):
    player = test_map.player
    a = DropAction(entity=player, item=potion)
    assert isinstance(a, actions.Action)


def test_is_ItemAction(test_map, potion):
    player = test_map.player
    a = DropAction(entity=player, item=potion)
    assert isinstance(a, ItemAction)


def test_init(test_map, potion):
    player = test_map.player
    a = DropAction(entity=player, item=potion)
    assert a.entity == player
    assert a.item == potion


def test_perform__item_leaves_inventory(test_map):
    player = test_map.player
    item = player.inventory.items.get('a')  # Need the actual item from inv
    assert item.name == "dagger"

    a = DropAction(entity=player, item=item)
    result = a.perform()
    assert item not in player.inventory.items


def test_perform__item_appears_on_map(test_map):
    player = test_map.player
    item = player.inventory.items.get('a')  # Need the actual item from inv
    assert item.name == "dagger"

    a = DropAction(entity=player, item=item)
    result = a.perform()
    assert item in test_map.get_items_at(player.x, player.y)


def test_perform__msg(test_map):
    player = test_map.player
    item = player.inventory.items.get('a')  # Need the actual item from inv
    assert item.name == "dagger"

    a = DropAction(entity=player, item=item)
    result = a.perform()
    assert a.msg == f"You dropped the {item.name}."


def test_perform__invalid_item_raises_Impossible(test_map):
    player = test_map.player
    a = DropAction(entity=player, item=factory.make("riot baton"))

    with pytest.raises(exceptions.Impossible):
        a.perform()


def test_perform__equipped_item(test_map):
    player = test_map.player
    item = player.inventory.items.get('a')  # Need the actual item from inv
    assert item.name == "dagger"
    player.equipment.toggle_equip(item)
    assert player.equipment.is_equipped(item)

    a = DropAction(entity=player, item=item)
    result = a.perform()

    assert not player.equipment.is_equipped(item)
