""" Tests for engine.py """
from src import engine, messages, dungeon
import pytest

from tests import toolkit


@pytest.fixture
def player():
    return toolkit.cp_player()


def test_init__msglog(player):
    e = engine.Engine(player=player)
    assert e.msglog.messages == []


def test_init__mouse_location(player):
    e = engine.Engine(player=player)
    assert e.mouse_location == (0, 0)


def test_init__player(player):
    e = engine.Engine(player=player)
    assert e.player == player


def test_init__helplog(player):
    e = engine.Engine(player=player)
    assert e.helplog  # Make sure it exists


def test_init__renderer(player):
    e = engine.Engine(player=player)
    assert e.renderer is None


def test_init__turns(player):
    e = engine.Engine(player=player)
    assert e.turns == 0


def test_init__dungeon(player):
    e = engine.Engine(player=player)
    assert isinstance(e.dungeon, dungeon.Dungeon)


@pytest.mark.skip(reason="Skeleton")
def test_handle_enemy_turns():
    pass


@pytest.mark.skip(reason="Skeleton")
def test_update_fov():
    pass


@pytest.mark.skip(reason="Skeleton")
def test_render():
    pass


@pytest.mark.skip(reason="Skeleton")
def test_save_as():
    pass


