""" Tests for engine.py """
from src import engine
import pytest


def test_Engine_init():
    e = engine.Engine(player="Player")
    assert e.msglog.messages == []
    assert e.mouse_location == (0, 0)
    assert e.player == "Player"

    assert e.msg_panel
    assert e.map_panel
    assert e.stat_panel


@pytest.mark.skip(reason="Skeleton")
def test_Engine_handle_enemy_turns():
    pass


@pytest.mark.skip(reason="Skeleton")
def test_Engine_update_fov():
    pass


@pytest.mark.skip(reason="Skeleton")
def test_Engine_render():
    pass


@pytest.mark.skip(reason="Skeleton")
def test_Engine_save_as():
    pass


