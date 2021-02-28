import pytest

from actions.actions import Action
from actions.search_action import SearchAction
from tests import toolkit


@pytest.fixture
def test_map():
    return toolkit.hidden_map()


def test_init__is_Action():
    s = SearchAction(None)
    assert isinstance(s, Action)


def test_init__entity():
    s = SearchAction(None)
    assert s.entity is None


def test_perform__finds_bear_trap__msg(test_map):
    player = test_map.player
    trap = test_map.get_trap_at(2, 3)
    assert trap.name == "bear trap"
    assert trap.hidden is True
    s = SearchAction(player)
    s.perform()
    assert s.msg == "You find a bear trap! "


def test_perform__finds_bear_trap__unhides_trap(test_map):
    player = test_map.player
    trap = test_map.get_trap_at(2, 3)
    assert trap.name == "bear trap"
    assert trap.hidden is True
    s = SearchAction(player)
    s.perform()
    assert "hidden" not in trap


def test_get_hidden_entities__none_around(test_map):
    player = test_map.player
    s = SearchAction(player)
    result = s.get_hidden_entities(4, 0)
    assert result == []


def test_get_hidden_entities__bear_trap(test_map):
    player = test_map.player
    s = SearchAction(player)
    trap = test_map.get_trap_at(2, 3)
    result = s.get_hidden_entities(2, 2)
    assert result == [trap]
