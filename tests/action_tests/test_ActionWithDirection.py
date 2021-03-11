from actions.actions import Action, ActionWithDirection
from src import player
from tests import toolkit
import pytest


@pytest.fixture
def test_map():
    return toolkit.test_map()


@pytest.fixture
def test_player():
    return player.Player()


def test_init_is_Action(test_map):
    plyr = test_map.player
    a = ActionWithDirection(entity=plyr, dx=1, dy=-1)
    assert isinstance(a, Action)


def test_init(test_map):
    plyr = test_map.player
    a = ActionWithDirection(entity=plyr, dx=1, dy=-1)
    assert a.entity == plyr
    assert a.dx == 1
    assert a.dy == -1
    assert a.msg == ''


def test_dest_xy(test_map):
    plyr = test_map.player
    dx, dy = 1, -1
    a = ActionWithDirection(entity=plyr, dx=dx, dy=dy)
    assert a.dest_xy == (plyr.x + dx, plyr.y + dy)


def test_blocking_entity(test_player):
    testmap = toolkit.test_map()
    testmap.place(test_player, 1, 2)
    # Blocked by a wall, not an entity
    a = ActionWithDirection(entity=test_player, dx=0, dy=-1)
    assert not a.blocking_entity


def test_target_actor(test_player):
    testmap = toolkit.test_map()
    testmap.place(test_player, 2, 4)
    a = ActionWithDirection(entity=test_player, dx=0, dy=1)
    assert a.target_actor.name == "grid bug"


def test_perform(test_player):
    test_player.x, test_player.y = 2, 4
    a = ActionWithDirection(entity=test_player, dx=0, dy=1)
    with pytest.raises(NotImplementedError):
        a.perform()
