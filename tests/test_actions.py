""" Tests for actions.py """

from src import factory
from src import actions
import toolkit
import pytest


@pytest.fixture
def test_map():
    return toolkit.test_map()


@pytest.fixture
def player():
    return toolkit.cp_player()


def test_Action_init(player):
    a = actions.Action(player)
    assert a.entity == player
    assert a.msg == ''


def test_Action_engine(test_map):
    player = test_map.get_player()
    a = actions.Action(player)
    result = a.engine
    assert result is None


def test_Action_perform__not_implemented(player):
    a = actions.Action(player)
    with pytest.raises(NotImplementedError):
        a.perform()


def test_ActionWithDirection_init(test_map):
    player = test_map.get_player()
    a = actions.ActionWithDirection(entity=player, dx=1, dy=-1)
    assert isinstance(a, actions.Action)
    assert a.entity == player
    assert a.dx == 1
    assert a.dy == -1
    assert a.msg == ''


def test_ActionWithDirection_dest_xy(test_map):
    player = test_map.get_player()
    dx, dy = 1, -1
    a = actions.ActionWithDirection(entity=player, dx=dx, dy=dy)
    assert a.dest_xy == (player.x + dx, player.y + dy)


def test_ActionWithDirection_blocking_entity(player):
    testmap = toolkit.test_map()
    player.place(1, 2, testmap)
    # Blocked by a wall, not an entity
    a = actions.ActionWithDirection(entity=player, dx=0, dy=-1)
    assert a.blocking_entity is None


def test_ActionWithDirection__target_actor(player):
    testmap = toolkit.test_map()
    player.place(2, 4, testmap)
    a = actions.ActionWithDirection(entity=player, dx=0, dy=1)
    assert a.target_actor.name == "Grid Bug"


# perform

# BumpAction
# init, is action
# perform

# ItemAction
# init
# target_actor
# perform

# DropItem
# perform

# EquipAction
# init
# perform


# MeleeAction
# perform

# MovementAction
# perform

# PickupAction
# init
# perform

# TakeStairsAction
# perform

# WaitAction
# perform
