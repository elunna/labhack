""" Tests for engine.py """
from src import engine, messages, dungeon
import pytest


def test_init__msglog():
    e = engine.Engine(player="Player")
    assert e.msglog.messages == []


def test_init__mouse_location():
    e = engine.Engine(player="Player")
    assert e.mouse_location == (0, 0)


def test_init__player():
    e = engine.Engine(player="Player")
    assert e.player == "Player"


def test_init__helplog():
    e = engine.Engine(player="Player")
    assert e.helplog  # Make sure it exists


def test_init__renderer():
    e = engine.Engine(player="Player")
    assert e.renderer is None


def test_init__turns():
    e = engine.Engine(player="Player")
    assert e.turns == 0


def test_init__dungeon():
    e = engine.Engine(player="Player")
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


