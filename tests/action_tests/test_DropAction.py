from actions import actions
from actions.drop_action import DropAction
from actions.item_action import ItemAction
from src import factory
from tests import toolkit
import pytest


@pytest.fixture
def test_map():
    return toolkit.test_map()


@pytest.fixture
def vial():
    return factory.make("healing vial")


def test_is_Action(test_map, vial):
    player = test_map.player
    a = DropAction(entity=player, item=vial)
    assert isinstance(a, actions.Action)


def test_is_ItemAction(test_map, vial):
    player = test_map.player
    a = DropAction(entity=player, item=vial)
    assert isinstance(a, ItemAction)


def test_init(test_map, vial):
    player = test_map.player
    a = DropAction(entity=player, item=vial)
    assert a.entity == player
    assert a.item == vial


def test_perform__item_leaves_inventory(test_map):
    player = test_map.player
    item = player.inventory.item_dict.get('a')  # Need the actual item from inv
    assert item.name == "dagger"

    a = DropAction(entity=player, item=item)
    result = a.perform()
    assert item not in player.inventory.item_dict


def test_perform__item_appears_on_map(test_map):
    player = test_map.player
    item = player.inventory.item_dict.get('a')  # Need the actual item from inv
    assert item.name == "dagger"

    a = DropAction(entity=player, item=item)
    a.perform()
    result = test_map.filter(x=player.x, y=player.y, name="dagger").pop()
    assert result.x == player.x
    assert result.y == player.y
    assert result.name == "dagger"


def test_perform__msg(test_map):
    player = test_map.player
    item = player.inventory.item_dict.get('a')  # Need the actual item from inv
    assert item.name == "dagger"

    a = DropAction(entity=player, item=item)
    result = a.perform()
    assert a.msg == f"You dropped a {item.name}."


def test_perform__equipped_item(test_map):
    player = test_map.player
    item = player.inventory.item_dict.get('a')  # Need the actual item from inv
    assert item.name == "dagger"
    player.equipment.toggle_equip(item)
    assert player.equipment.is_equipped(item)

    a = DropAction(entity=player, item=item)
    result = a.perform()

    assert not player.equipment.is_equipped(item)
