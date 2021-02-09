from . import actions
from .dieaction import DieAction
from src.renderorder import RenderOrder
from tests import toolkit
import pytest


@pytest.fixture
def test_map():
    return toolkit.test_map()



def test_DieAction_is_Action(test_map):
    orc = test_map.get_actor_at(5, 4)
    player = test_map.get_player()

    a = DieAction(entity=player, cause=orc)
    assert isinstance(a, actions.Action)


def test_DieAction_init(test_map):
    orc = test_map.get_actor_at(5, 4)
    player = test_map.get_player()

    a = DieAction(entity=player, cause=orc)
    assert a.entity == player
    assert a.cause == orc


def test_DieAction_perform__player_kills_enemy(test_map):
    orc = test_map.get_actor_at(5, 4)
    player = test_map.get_player()
    a = DieAction(entity=orc, cause=player)
    a.perform()

    assert orc.char == "%"
    assert orc.color == (191, 0, 0)
    assert orc.blocks_movement is False
    assert orc.ai is None
    assert orc.name == "Orc corpse"
    assert orc.render_order == RenderOrder.CORPSE


def test_DieAction_perform__player_kills_enemy__xp(test_map):
    orc = test_map.get_actor_at(5, 4)
    player = test_map.get_player()
    a = DieAction(entity=orc, cause=player)
    a.perform()

    assert player.level.current_xp == orc.level.xp_given


def test_DieAction_perform__player_kills_enemy__msg(test_map):
    orc = test_map.get_actor_at(5, 4)
    player = test_map.get_player()
    a = DieAction(entity=orc, cause=player)
    a.perform()

    assert a.msg == "You kill the Orc!"


def test_DieAction_perform__enemy_kills_player(test_map):
    orc = test_map.get_actor_at(5, 4)
    player = test_map.get_player()
    a = DieAction(entity=player, cause=orc)
    a.perform()

    assert player.char == "%"
    assert player.color == (191, 0, 0)
    assert player.blocks_movement is False
    assert player.ai is None
    assert player.name == "Player corpse"
    assert player.render_order == RenderOrder.CORPSE


def test_DieAction_perform__enemy_kills_player__msg(test_map):
    orc = test_map.get_actor_at(5, 4)
    player = test_map.get_player()
    a = DieAction(entity=player, cause=orc)
    a.perform()

    assert a.msg == "You died!"


def test_DieAction_perform__enemy_kills_enemy__msg(test_map):
    orc = test_map.get_actor_at(5, 4)
    gridbug = test_map.get_actor_at(2, 5)
    a = DieAction(entity=gridbug, cause=orc)
    a.perform()

    assert a.msg == "The Orc kills the Grid Bug!"


def test_DieAction_perform__enemy_kills_enemy__xp(test_map):
    orc = test_map.get_actor_at(5, 4)
    gridbug = test_map.get_actor_at(2, 5)
    a = DieAction(entity=gridbug, cause=orc)
    a.perform()

    assert orc.level.current_xp == gridbug.level.xp_given
