from . import actions
from .pickup import PickupAction
from src import exceptions
from src import factory
from tests import toolkit
import pytest


@pytest.fixture
def test_map():
    return toolkit.test_map()


def test_init__is_Action(test_map):
    player = test_map.player
    a = PickupAction(entity=player)
    assert isinstance(a, actions.Action)


def test_init(test_map):
    player = test_map.player
    a = PickupAction(entity=player)
    assert a.entity == player


def test_perform__no_items__raises_Impossible(test_map):
    player = test_map.player
    a = PickupAction(entity=player)
    with pytest.raises(exceptions.Impossible):
        a.perform()


def test_perform__single_item(test_map):
    player = test_map.player
    # Put a scroll at player location
    factory.lightning_scroll.spawn(test_map, player.x, player.y)
    a = PickupAction(entity=player)
    a.perform()
    assert a.msg == "You picked up the Lightning Scroll. "


@pytest.mark.skip(reason='Pickup for piles of items not yet supported')
def test_perform__multiple_items(test_map):
    player = test_map.player
    # Put 2 scrolls at player location
    factory.lightning_scroll.spawn(test_map, player.x, player.y)
    factory.fireball_scroll.spawn(test_map, player.x, player.y)

    a = PickupAction(entity=player)
    a.perform()

    # How do we know which item to pickup?
    assert a.msg == "You picked up the Lightning Scroll. "
