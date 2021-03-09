from actions import actions
from actions.wait_action import WaitAction
from tests import toolkit
import pytest


@pytest.fixture
def player():
    return toolkit.cp_player()


def test_init__is_Action(player):
    a = WaitAction(entity=player)
    assert isinstance(a, actions.Action)


def test_init(player):
    a = WaitAction(entity=player)
    assert a.entity == player


def test_perform(player):
    a = WaitAction(entity=player)
    assert a.perform() is None
    assert a.msg == ''
