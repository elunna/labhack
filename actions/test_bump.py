from . import actions
from tests import toolkit
from .bump import BumpAction
from .move import MovementAction
from .melee import MeleeAction
import pytest


@pytest.fixture
def test_map():
    return toolkit.test_map()


def test_BumpAction_is_Action(test_map):
    player = test_map.player
    a = BumpAction(entity=player, dx=1, dy=-1)
    assert isinstance(a, actions.Action)


def test_BumpAction_is_ActionWithDirection(test_map):
    player = test_map.player
    a = BumpAction(entity=player, dx=1, dy=-1)
    assert isinstance(a, actions.ActionWithDirection)


def test_BumpAction_init(test_map):
    player = test_map.player
    a = BumpAction(entity=player, dx=1, dy=-1)
    assert a.entity == player
    assert a.dx == 1
    assert a.dy == -1
    assert a.msg == ''


def test_BumpAction_perform__Move(test_map):
    player = test_map.player
    a = BumpAction(entity=player, dx=1, dy=1)
    result = a.perform()
    assert isinstance(result, MovementAction)


def test_BumpAction_perform__Melee(test_map):
    # We'll attack the Grid Bug at (2, 5)
    player = test_map.player
    player.place(2, 4, test_map)
    a = BumpAction(entity=player, dx=0, dy=1)
    result = a.perform()
    assert isinstance(result, MeleeAction)
