""" Tests for engine.py """
from src import engine
import pytest


def test_init():
    e = engine.Engine(player="Player")
    assert e.msglog.messages == []
    assert e.mouse_location == (0, 0)
    assert e.player == "Player"


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


