from . import actions
from .equip_action import EquipAction
from src import factory
from tests import toolkit
import pytest


@pytest.fixture
def test_map():
    return toolkit.test_map()


def test_init__is_Action(test_map):
    player = test_map.player
    armor = factory.make("leather_vest")
    a = EquipAction(entity=player, item=armor)
    assert isinstance(a, actions.Action)


def test_init(test_map):
    player = test_map.player
    armor = factory.make("leather_vest")
    a = EquipAction(entity=player, item=armor)
    assert a.entity == player
    assert a.item == armor


def test_perform(test_map):
    player = test_map.player
    armor = factory.make("leather_vest")
    assert not player.equipment.is_equipped(armor)

    a = EquipAction(entity=player, item=armor)
    a.perform()
    assert player.equipment.is_equipped(armor)
