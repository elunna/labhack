""" Tests for actions.py """
from .actions import Action
from tests import toolkit
import pytest


@pytest.fixture
def test_map():
    return toolkit.test_map()


@pytest.fixture
def player():
    return toolkit.cp_player()


def test_init(player):
    a = Action(player)
    assert a.entity == player
    assert a.msg == ''


def test_engine(test_map):
    player = test_map.player
    a = Action(player)
    result = a.engine
    assert result is None


def test_perform__not_implemented(player):
    a = Action(player)
    with pytest.raises(NotImplementedError):
        a.perform()
