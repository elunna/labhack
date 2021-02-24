from .action_with_direction import ActionWithDirection
from .actions import Action
from tests import toolkit
import pytest


@pytest.fixture
def test_map():
    return toolkit.test_map()


@pytest.fixture
def player():
    return toolkit.cp_player()


def test_init_is_Action(test_map):
    player = test_map.player
    a = ActionWithDirection(entity=player, dx=1, dy=-1)
    assert isinstance(a, Action)


def test_init(test_map):
    player = test_map.player
    a = ActionWithDirection(entity=player, dx=1, dy=-1)
    assert a.entity == player
    assert a.dx == 1
    assert a.dy == -1
    assert a.msg == ''


def test_dest_xy(test_map):
    player = test_map.player
    dx, dy = 1, -1
    a = ActionWithDirection(entity=player, dx=dx, dy=dy)
    assert a.dest_xy == (player.x + dx, player.y + dy)


def test_blocking_entity(player):
    testmap = toolkit.test_map()
    player.place(1, 2, testmap)
    # Blocked by a wall, not an entity
    a = ActionWithDirection(entity=player, dx=0, dy=-1)
    assert a.blocking_entity is None


def test_target_actor(player):
    testmap = toolkit.test_map()
    player.place(2, 4, testmap)
    a = ActionWithDirection(entity=player, dx=0, dy=1)
    assert a.target_actor.name == "Grid Bug"


def test_perform(player):
    testmap = toolkit.test_map()
    player.place(2, 4, testmap)
    a = ActionWithDirection(entity=player, dx=0, dy=1)
    with pytest.raises(NotImplementedError):
        a.perform()
