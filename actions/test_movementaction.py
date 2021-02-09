from . import actions
from . import toolkit
from .moveaction import MovementAction
from src import exceptions
import pytest


@pytest.fixture
def test_map():
    return toolkit.test_map()


def test_MovementAction_is_Action(test_map):
    player = test_map.get_player()
    a = MovementAction(entity=player, dx=1, dy=-1)
    assert isinstance(a, actions.Action)


def test_MovementAction_is_ActionWithDirection(test_map):
    player = test_map.get_player()
    a = MovementAction(entity=player, dx=1, dy=-1)
    assert isinstance(a, actions.ActionWithDirection)


def test_MovementAction_init(test_map):
    player = test_map.get_player()
    a = MovementAction(entity=player, dx=1, dy=-1)
    assert a.dx == 1
    assert a.dy == -1
    assert a.entity == player


def test_MovementAction_perform__success(test_map):
    player = test_map.get_player()
    a = MovementAction(entity=player, dx=-1, dy=0)
    a.perform()
    assert player.x == 4
    assert player.y == 5


def test_MovementAction_perform__out_of_bounds__raises_Impossible(test_map):
    player = test_map.get_player()
    # Try to move out of the map bounds (we're at 5, 5)
    a = MovementAction(entity=player, dx=1, dy=1)
    with pytest.raises(exceptions.Impossible):
        a.perform()


def test_MovementAction_perform__blocked_by_wall__raises_Impossible(test_map):
    player = test_map.get_player()
    # Try to move into wall
    a = MovementAction(entity=player, dx=-1, dy=-1)
    with pytest.raises(exceptions.Impossible):
        a.perform()


def test_MovementAction_perform__blocked_by_actor__raises_Impossible(test_map):
    player = test_map.get_player()
    # Try to move into orc
    a = MovementAction(entity=player, dx=0, dy=-1)
    with pytest.raises(exceptions.Impossible):
        a.perform()
