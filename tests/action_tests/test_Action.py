""" Tests for actions.py """
from actions.actions import Action
from src import player
from tests import toolkit
import pytest


@pytest.fixture
def test_map():
    return toolkit.test_map()


@pytest.fixture
def test_player():
    return player.Player()


def test_init(test_player):
    a = Action(test_player)
    assert a.entity == test_player
    assert a.msg == ''


def test_engine(test_map):
    test_player = test_map.player
    a = Action(test_player)
    result = a.engine
    assert result is None


def test_perform__not_implemented(test_player):
    a = Action(test_player)
    with pytest.raises(NotImplementedError):
        a.perform()
