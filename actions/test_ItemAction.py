from . import actions
from .item_action import ItemAction
from src import factory
from tests import toolkit
import pytest


@pytest.fixture
def test_map():
    return toolkit.test_map()


@pytest.fixture
def potion():
    return factory.make("health potion")


def test_init__is_Action(test_map, potion):
    player = test_map.player
    a = ItemAction(entity=player, item=potion)
    assert isinstance(a, actions.Action)


def test_init(test_map, potion):
    player = test_map.player
    a = ItemAction(entity=player, item=potion)
    assert a.item == potion
    assert a.entity == player


def test_init__default_targetxy_is_playersxy(test_map, potion):
    player = test_map.player
    a = ItemAction(entity=player, item=potion)
    assert a.target_xy == (player.x, player.y)


def test_init__with_target_xy(test_map, potion):
    player = test_map.player
    a = ItemAction(entity=player, item=potion, target_xy=(1, 1))
    assert a.target_xy == (1, 1)


def test_target_actor(test_map, potion):
    player = test_map.player
    # We'll target the grid bug
    a = ItemAction(entity=player, item=potion, target_xy=(2, 5))
    result = a.target_actor
    assert result.name == "Grid Bug"


# perform
# perform with a consumable item
# perform with a non-consumable item
# perform with a reuseable/chargeable item?


