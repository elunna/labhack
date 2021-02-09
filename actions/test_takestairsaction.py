from . import actions
from .stairactions import TakeStairsAction
from src import exceptions
from tests import toolkit
import pytest


@pytest.fixture
def test_map():
    return toolkit.test_map()


def test_TakeStairsAction_is_Action(test_map):
    player = test_map.get_player()
    a = TakeStairsAction(entity=player)
    assert isinstance(a, actions.Action)


def test_TakeStairsAction_init(test_map):
    player = test_map.get_player()
    a = TakeStairsAction(entity=player)
    assert a.entity == player


@pytest.mark.skip(reason='Engine/GameWorld need updating')
def test_TakeStairsAction_perform__player_removed_from_old_map(testengine):
    player = testengine.game_map.get_player()
    a = TakeStairsAction(entity=player)
    a.perform


@pytest.mark.skip(reason='Engine/GameWorld need updating')
def test_TakeStairsAction_perform__level_changed(test_map):
    pass


@pytest.mark.skip(reason='Engine/GameWorld need updating')
def test_TakeStairsAction_perform__player_added_to_new_map(test_map):
    pass


@pytest.mark.skip(reason='Engine/GameWorld need updating')
def test_TakeStairsAction_perform__player_on_upstair(test_map):
    pass


@pytest.mark.skip(reason='Engine/GameWorld need updating')
def test_TakeStairsAction_perform__msg(test_map):
    player = test_map.get_player()
    a = TakeStairsAction(entity=player)
    assert a.msg == "You descend the stairs"


@pytest.mark.skip(reason='Engine/GameWorld need updating')
def test_TakeStairsAction_perform__no_stairs__raises_Impossible(test_map):
    player = test_map.get_player()
    a = TakeStairsAction(entity=player)
    with pytest.raises(exceptions.Impossible):
        a.perform()



