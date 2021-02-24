from . import actions
from .downstairs_action import DownStairsAction
from src import exceptions
from tests import toolkit
import pytest


@pytest.fixture
def test_map():
    return toolkit.test_map()


def test_init__is_Action(test_map):
    player = test_map.player
    a = DownStairsAction(entity=player)
    assert isinstance(a, actions.Action)


def test_init(test_map):
    player = test_map.player
    a = DownStairsAction(entity=player)
    assert a.entity == player


@pytest.mark.skip(reason='Engine/GameWorld need updating')
def test_perform__player_removed_from_old_map(testengine):
    player = testengine.game_map.player()
    a = DownStairsAction(entity=player)
    a.perform


@pytest.mark.skip(reason='Engine/GameWorld need updating')
def test_perform__level_changed(test_map):
    pass


@pytest.mark.skip(reason='Engine/GameWorld need updating')
def test_perform__player_added_to_new_map(test_map):
    pass


@pytest.mark.skip(reason='Engine/GameWorld need updating')
def test_perform__player_on_upstair(test_map):
    pass


@pytest.mark.skip(reason='Engine/GameWorld need updating')
def test_perform__msg(test_map):
    player = test_map.player()
    a = DownStairsAction(entity=player)
    assert a.msg == "You descend the stairs"


@pytest.mark.skip(reason='Engine/GameWorld need updating')
def test_perform__no_stairs__raises_Impossible(test_map):
    player = test_map.player()
    a = DownStairsAction(entity=player)
    with pytest.raises(exceptions.Impossible):
        a.perform()



