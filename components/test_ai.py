""" Tests for ai.py """

from . import ai
from .component import Component
from src import gamemap
from src import tiles
from tests import toolkit
import pytest


@pytest.fixture
def player():
    new_map = toolkit.test_map()
    return new_map.get_player()


@pytest.fixture
def empty_map():
    new_map = gamemap.GameMap(
        width=10,
        height=10,
        fill_tile=tiles.floor
    )


def test_BaseAI_init(player):
    base_ai = ai.BaseAI(player)
    assert base_ai.parent is player


def test_BaseAI_is_Component(player):
    base_ai = ai.BaseAI(player)
    assert isinstance(base_ai, Component)


@pytest.mark.skip(reason='Should we handle entity not having a gamemap/engine?')
def test_BaseAI_engine(player):
    base_ai = ai.BaseAI(player)
    result = base_ai.engine
    assert isinstance(result, Engine)


def test_BaseAI_perform(player):
    # This is not implemented in the Component class.
    base_ai = ai.BaseAI(player)
    with pytest.raises(NotImplementedError):
        base_ai.perform()


@pytest.mark.skip(reason='REQUIRES the entity to have a gamemap reference')
def test_BaseAI_get_path_to(player):
    base_ai = ai.BaseAI(player)
    result = base_ai.engine
    assert isinstance(result, Engine)


def test_HostileAI_is_Component(player):
    approach_ai = ai.HostileAI(player)
    assert isinstance(approach_ai, Component)


def test_HostileAI_init(player):
    approach_ai = ai.HostileAI(player)
    assert approach_ai.path == []


@pytest.mark.skip(reason='REQUIRES the entity to have a gamemap and enginereference')
def test_HostileAI_perform(player):
    approach_ai = ai.HostileAI(player)
    assert approach_ai.path == []

    # TODO: Target can be anything in addition to the player
    # TODO: Target is not visible
    # TODO: Target is more than 1 square away
    # TODO: Target is 1 square away - cardinal
    # TODO: Target is 1 square away - diagonal


def test_ConfusedAI_is_Component(player):
    confused_ai = ai.ConfusedAI(
        parent=player,
        previous_ai=ai.HostileAI,
        turns_remaining=4
    )
    assert isinstance(confused_ai, Component)


@pytest.mark.skip(reason='Engine reference issues')
def test_ConfusedAI_init(player):
    confused_ai = ai.ConfusedAI(
        entity=player,
        previous_ai=ai.HostileAI,
        turns_remaining=4
    )
    assert confused_ai.previous_ai == ai.HostileAI
    assert confused_ai.turns_remaining == 4


@pytest.mark.skip(reason='Engine reference issues')
def test_ConfusedAI_perform(player):
    confused_ai = ai.ConfusedAI(
        entity=player,
        previous_ai=ai.HostileAI,
        turns_remaining=4
    )
    result = confused_ai.perform()
    assert isinstance(result, BumpAction)
    assert confused_ai.turns_remaining == 3


@pytest.mark.skip(reason='Engine reference issues')
def test_ConfusedAI_perform__no_turns_remaining(player):
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
