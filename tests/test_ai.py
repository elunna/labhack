""" Tests for ai.py """

from components.component import Component
from components import ai
from src import actions
from src import engine
from src import factory
from src import gamemap
from src import tiles
import copy
import pytest
import test_tools

@pytest.fixture
def player():
    new_map = test_tools.test_map()
    return new_map.get_player()

@pytest.fixture
def empty_map():
    new_map = gamemap.GameMap(
        width=10,
        height=10,
        fill_tile=tiles.floor
    )

# All of these should be BaseComponents

def test_BaseAI_init(player):
    base_ai = ai.BaseAI(player)
    assert base_ai.entity is player


@pytest.mark.skip(reason='Convert to BaseComponent later')
def test_BaseAI_is_BaseComponent(player):
    base_ai = ai.BaseAI(player)
    assert isinstance(base_ai, Component)


@pytest.mark.skip(reason='Should we handle entity not having a gamemap/engine?')
def test_BaseAI_engine(player):
    base_ai = ai.BaseAI(player)
    result = base_ai.engine
    assert isinstance(result, Engine)


def test_BaseAI_perform(player):
    # This is not implemented in the base BaseComponent class.
    base_ai = ai.BaseAI(player)
    with pytest.raises(NotImplementedError):
        base_ai.perform()


@pytest.mark.skip(reason='REQUIRES the entity to have a gamemap reference')
def test_BaseAI_get_path_to(player):
    base_ai = ai.BaseAI(player)
    result = base_ai.engine
    assert isinstance(result, Engine)


@pytest.mark.skip(reason='Convert to BaseComponent later')
def test_HostileEnemy_is_BaseComponent(player):
    approach_ai = ai.HostileAI(player)
    assert isinstance(approach_ai, Component)


def test_HostileEnemy_init(player):
    approach_ai = ai.HostileAI(player)
    assert approach_ai.path == []


@pytest.mark.skip(reason='REQUIRES the entity to have a gamemap and enginereference')
def test_HostileEnemy_perform(player):
    approach_ai = ai.HostileAI(player)
    assert approach_ai.path == []

    # TODO: Target can be anything in addition to the player
    # TODO: Target is not visible
    # TODO: Target is more than 1 square away
    # TODO: Target is 1 square away - cardinal
    # TODO: Target is 1 square away - diagonal


@pytest.mark.skip(reason='Convert to BaseComponent later')
def test_ConfusedEnemy_is_BaseComponent(player):
    confused_ai = ai.ConfusedAI(
        entity=player,
        previous_ai=ai.HostileAI,
        turns_remaining=4
    )
    assert isinstance(confused_ai, Component)


@pytest.mark.skip(reason='Engine reference issues')
def test_ConfusedEnemy_init(player):
    confused_ai = ai.ConfusedAI(
        entity=player,
        previous_ai=ai.HostileAI,
        turns_remaining=4
    )
    assert confused_ai.previous_ai == ai.HostileAI
    assert confused_ai.turns_remaining == 4


@pytest.mark.skip(reason='Engine reference issues')
def test_ConfusedEnemy_perform(player):
    confused_ai = ai.ConfusedAI(
        entity=player,
        previous_ai=ai.HostileAI,
        turns_remaining=4
    )
    result = confused_ai.perform()
    assert isinstance(result, BumpAction)
    assert confused_ai.turns_remaining == 3


@pytest.mark.skip(reason='Engine reference issues')
def test_ConfusedEnemy_perform__no_turns_remaining(player):
    confused_ai = ai.ConfusedAI(
        entity=player,
        previous_ai=ai.HostileAI,
        turns_remaining=4
    )
    confused_ai.perform()  # 3 remaining
    confused_ai.perform()  # 2 remaining
    confused_ai.perform()  # 1 remaining
    confused_ai.perform()  # 0 remaining

    assert isinstance(player.ai, ai.HostileAI)
