from actions import actions
from actions.upstairs_action import UpStairsAction
from src import dungeon
from src import exceptions
from tests import toolkit
from types import SimpleNamespace
import pytest


@pytest.fixture
def test_dungeon():
    # Create a dungeon with 3 floors and adds the player to the floor 2 for easy testing situations.
    player = toolkit.cp_player()
    e = SimpleNamespace(game_map='testmap', player=player)
    d = dungeon.Dungeon(engine=e, test_map=toolkit.stair_map)
    d.generate_floor()  # Floor 2
    d.generate_floor()  # Floor 3

    d.place_entity(player, 2, 0, 0)  # Put the player on level 2
    d.current_map.player = player  # We'll set this manually
    assert d.dlevel == 2
    return d


def test_init__is_Action(test_dungeon):
    player = test_dungeon.current_map.player
    a = UpStairsAction(entity=player, dungeon=test_dungeon)
    assert isinstance(a, actions.Action)


def test_init(test_dungeon):
    player = test_dungeon.current_map.player
    a = UpStairsAction(entity=player, dungeon=test_dungeon)
    assert a.entity == player


def test_perform__not_on_upstairs__raises_Impossible(test_dungeon):
    player = test_dungeon.current_map.player
    a = UpStairsAction(entity=player, dungeon=test_dungeon)
    with pytest.raises(exceptions.Impossible):
        a.perform()


def test_perform__success_calls_dungeon_move_upstairs(mocker, test_dungeon):
    mocker.patch('src.dungeon.Dungeon.move_upstairs')

    player = test_dungeon.current_map.player
    player.x, player.y = test_dungeon.current_map.upstairs_location
    a = UpStairsAction(entity=player, dungeon=test_dungeon)
    a.perform()
    test_dungeon.move_upstairs.assert_called_once()


def test_perform__msg(test_dungeon):
    player = test_dungeon.current_map.player
    player.x, player.y = test_dungeon.current_map.upstairs_location

    a = UpStairsAction(entity=player, dungeon=test_dungeon)
    a.perform()
    assert a.msg == "You ascend the stairs."
