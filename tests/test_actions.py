""" Tests for actions.py """

import factories
import actions
import pytest

@pytest.fixture
def player():
    return factories.cp_player()


def test_Action_init(player):
    a = actions.Action(player)
    assert a.entity == player
    assert a.msg == ''


def test_Action_engine(player):
    testmap = factories.test_map()
    player.place(0, 0, testmap)

    a = actions.Action(player)
    result = a.engine
    assert result is None


def test_Action_perform__not_implemented(player):
    a = actions.Action(player)
    with pytest.raises(NotImplementedError):
        a.perform()

# ActionWithDirection
# init, is Action
# dest_xy
# blocking_entity
# target_actor
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
