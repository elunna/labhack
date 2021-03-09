from actions import actions
from actions.die_action import DieAction
from src.renderorder import RenderOrder
from tests import toolkit
import pytest


@pytest.fixture
def test_map():
    return toolkit.test_map()


def test_is_Action(test_map):
    henchman = test_map.get_actor_at(5, 4)
    player = test_map.player

    a = DieAction(entity=player, cause=henchman)
    assert isinstance(a, actions.Action)


def test_init(test_map):
    henchman = test_map.get_actor_at(5, 4)
    player = test_map.player

    a = DieAction(entity=player, cause=henchman)
    assert a.entity == player
    assert a.cause == henchman


def test_perform__player_kills_enemy(test_map):
    henchman = test_map.get_actor_at(5, 4)
    player = test_map.player
    a = DieAction(entity=henchman, cause=player)
    a.perform()

    assert henchman.char == "%"
    assert henchman.color == (191, 0, 0)
    assert henchman.blocks_movement is False
    assert henchman.ai is None
    assert henchman.name == "henchman corpse"
    assert henchman.render_order == RenderOrder.CORPSE


def test_perform__player_kills_enemy__xp(test_map):
    henchman = test_map.get_actor_at(5, 4)
    player = test_map.player
    a = DieAction(entity=henchman, cause=player)
    a.perform()

    assert player.level.current_xp == henchman.level.xp_given


def test_perform__player_kills_enemy__msg(test_map):
    orc = test_map.get_actor_at(5, 4)
    player = test_map.player
    a = DieAction(entity=orc, cause=player)
    a.perform()

    assert a.msg == "You kill the henchman!"


def test_perform__enemy_kills_player(test_map):
    henchman = test_map.get_actor_at(5, 4)
    player = test_map.player
    a = DieAction(entity=player, cause=henchman)
    a.perform()

    assert player.char == "%"
    assert player.color == (191, 0, 0)
    assert player.blocks_movement is False
    assert player.ai is None
    assert player.name == "player corpse"
    assert player.render_order == RenderOrder.CORPSE


def test_perform__enemy_kills_player__msg(test_map):
    henchman = test_map.get_actor_at(5, 4)
    player = test_map.player
    a = DieAction(entity=player, cause=henchman)
    a.perform()
    assert a.msg == "You died!"


def test_perform__enemy_kills_enemy__msg(test_map):
    henchman = test_map.get_actor_at(5, 4)
    gridbug = test_map.get_actor_at(2, 5)
    a = DieAction(entity=gridbug, cause=henchman)
    a.perform()
    assert a.msg == "The henchman kills the grid bug!"


def test_perform__enemy_kills_enemy__xp(test_map):
    henchman = test_map.get_actor_at(5, 4)
    gridbug = test_map.get_actor_at(2, 5)
    a = DieAction(entity=gridbug, cause=henchman)
    a.perform()

    assert henchman.level.current_xp == gridbug.level.xp_given
