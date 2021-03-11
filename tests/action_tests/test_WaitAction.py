from actions import actions
from actions.wait_action import WaitAction
import pytest
from src import player


@pytest.fixture
def test_player():
    return player.Player()


def test_init__is_Action(test_player):
    a = WaitAction(entity=test_player)
    assert isinstance(a, actions.Action)


def test_init(test_player):
    a = WaitAction(entity=test_player)
    assert a.entity == test_player


def test_perform(test_player):
    a = WaitAction(entity=test_player)
    assert a.perform() is None
    assert a.msg == ''
