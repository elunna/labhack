from . import actions
from .downstairs_action import DownStairsAction
from pytest_mock import mocker
from types import SimpleNamespace
from src import dungeon
from src import exceptions
from tests import toolkit
import pytest


@pytest.fixture
def test_dungeon():
    # Create a dungeon with 1 floor and add the Player to it.
    player = toolkit.cp_player()
    e = SimpleNamespace(game_map='testmap', player=player)
    d = dungeon.Dungeon(engine=e, test_map=toolkit.stair_map)
    d.generate_floor()
    d.current_map.add_entity(player, 0, 0)
    d.current_map.player = player
    return d


def test_init__is_Action(test_dungeon):
    player = test_dungeon.current_map.player
    a = DownStairsAction(entity=player, dungeon=None)
    assert isinstance(a, actions.Action)


def test_init(test_dungeon):
    player = test_dungeon.current_map.player
    a = DownStairsAction(entity=player, dungeon=None)
    assert a.entity == player


def test_perform__no_stairs__raises_Impossible(test_dungeon):
    player = test_dungeon.current_map.player
    a = DownStairsAction(entity=player, dungeon=test_dungeon)
    with pytest.raises(exceptions.Impossible):
        a.perform()


def test_perform__success_calls_dungeon_move_downstairs(mocker, test_dungeon):
    mocker.patch('src.dungeon.Dungeon.move_downstairs')

    player = test_dungeon.current_map.player
    player.x, player.y = test_dungeon.current_map.downstairs_location
    a = DownStairsAction(entity=player, dungeon=test_dungeon)
    a.perform()
    test_dungeon.move_downstairs.assert_called_once()


def test_perform__msg(test_dungeon):
    player = test_dungeon.current_map.player
    player.x, player.y = test_dungeon.current_map.downstairs_location

    a = DownStairsAction(entity=player, dungeon=test_dungeon)
    a.perform()
    assert a.msg == "You descend the stairs."
