from . import actions
from .equipaction import EquipAction
from src import factory
from tests import toolkit
import pytest


@pytest.fixture
def test_map():
    return toolkit.test_map()


def test_EquipAction_is_Action(test_map):
    player = test_map.get_player()
    armor = factory.leather_armor
    a = EquipAction(entity=player, item=armor)
    assert isinstance(a, actions.Action)


def test_EquipAction_init(test_map):
    player = test_map.get_player()
    armor = factory.leather_armor
    a = EquipAction(entity=player, item=armor)
    assert a.entity == player
    assert a.item == armor


def test_EquipAction_perform(test_map):
    player = test_map.get_player()
    armor = factory.leather_armor
    assert not player.equipment.item_is_equipped(armor)

    a = EquipAction(entity=player, item=armor)
    a.perform()
    assert player.equipment.item_is_equipped(armor)



