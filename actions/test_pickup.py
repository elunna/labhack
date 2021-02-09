import src.item_data
from . import actions
from .pickup import PickupAction
from src import exceptions
from src import factory
from tests import toolkit
import pytest


@pytest.fixture
def test_map():
    return toolkit.test_map()


def test_PickupAction_is_Action(test_map):
    player = test_map.get_player()
    a = PickupAction(entity=player)
    assert isinstance(a, actions.Action)


def test_PickupAction_init(test_map):
    player = test_map.get_player()
    a = PickupAction(entity=player)
    assert a.entity == player


def test_PickupAction_perform__no_items__raises_Impossible(test_map):
    player = test_map.get_player()
    a = PickupAction(entity=player)
    with pytest.raises(exceptions.Impossible):
        a.perform()


def test_PickupAction_perform__single_item(test_map):
    player = test_map.get_player()
    # Put a scroll at player location
    src.item_data.lightning_scroll.spawn(test_map, player.x, player.y)
    a = PickupAction(entity=player)
    a.perform()
    assert a.msg == "You picked up the Lightning Scroll. "


@pytest.mark.skip(reason='Pickup for piles of items not yet supported')
def test_PickupAction_perform__multiple_items(test_map):
    player = test_map.get_player()
    # Put 2 scrolls at player location
    src.item_data.lightning_scroll.spawn(test_map, player.x, player.y)
    src.item_data.fireball_scroll.spawn(test_map, player.x, player.y)

    a = PickupAction(entity=player)
    a.perform()

    # How do we know which item to pickup?
    assert a.msg == "You picked up the Lightning Scroll. "