from . import actions
from .wait import WaitAction
from tests import toolkit
import pytest

@pytest.fixture
def player():
    return toolkit.cp_player()


def test_WaitAction_is_Action(player):
    a = WaitAction(entity=player)
    assert isinstance(a, actions.Action)


def test_WaitAction_init(player):
    a = WaitAction(entity=player)
    assert a.entity == player


def test_WaitAction_perform(player):
    a = WaitAction(entity=player)
    assert a.perform() is None
    assert a.msg == ''
