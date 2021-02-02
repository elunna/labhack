""" Tests for ai.py """

from actions import WaitAction, BumpAction
from components.component import Component
from engine import Engine
import components.ai
import copy
import factories
import pytest


@pytest.fixture
def empty_map():
    new_map = game_map.GameMap(
        width=10,
        height=10,
        fill_tile=tile_types.floor
    )

# All of these should be Components

# Tests for BaseAI
def test_BaseAI_init():
    player = copy.deepcopy(factories.player)
    ai = components.ai.BaseAI(player)
    assert ai.entity is player


@pytest.mark.skip(reason='Convert to Component later')
def test_BaseAI_is_Component():
    player = copy.deepcopy(factories.player)
    ai = components.ai.BaseAI(player)
    assert isinstance(ai, Component)


@pytest.mark.skip(reason='Should we handle entity not having a gamemap/engine?')
def test_BaseAI_engine():
    player = copy.deepcopy(factories.player)
    ai = components.ai.BaseAI(player)
    result = ai.engine
    assert isinstance(result, Engine)


def test_BaseAI_yield_action():
    # This is not implemented in the base Component class.
    player = copy.deepcopy(factories.player)
    ai = components.ai.BaseAI(player)
    with pytest.raises(NotImplementedError):
        ai.yield_action()


@pytest.mark.skip(reason='REQUIRES the entity to have a gamemap reference')
def test_BaseAI_get_path_to():
    player = copy.deepcopy(factories.player)
    ai = components.ai.BaseAI(player)
    result = ai.engine
    assert isinstance(result, Engine)


@pytest.mark.skip(reason='Convert to Component later')
def test_HeroControllerAI_is_Component():
    player = copy.deepcopy(factories.player)
    ai = components.ai.HeroControllerAI(player)
    assert isinstance(ai, Component)


def test_HeroControllerAI_yield_action__is_None():
    player = copy.deepcopy(factories.player)
    ai = components.ai.HeroControllerAI(player)
    result = ai.yield_action()
    assert result is None


@pytest.mark.skip(reason='Convert to Component later')
def test_StationaryAI_is_Component():
    player = copy.deepcopy(factories.player)
    ai = components.ai.StationaryAI(player)
    assert isinstance(ai, Component)


def test_StationaryAI_yield_action():
    player = copy.deepcopy(factories.player)
    ai = components.ai.StationaryAI(player)
    result = ai.yield_action()
    # Always returns a WaitAction
    assert isinstance(result, WaitAction)


@pytest.mark.skip(reason='Convert to Component later')
def test_ApproachAI_is_Component():
    player = copy.deepcopy(factories.player)
    ai = components.ai.ApproachAI(player)
    assert isinstance(ai, Component)


def test_ApproachAI_init():
    player = copy.deepcopy(factories.player)
    ai = components.ai.ApproachAI(player)
    assert ai.path == []


@pytest.mark.skip(reason='REQUIRES the entity to have a gamemap and enginereference')
def test_ApproachAI_yield_action():
    player = copy.deepcopy(factories.player)
    ai = components.ai.ApproachAI(player)
    assert ai.path == []

    # TODO: Target can be anything in addition to the player
    # TODO: Target is not visible
    # TODO: Target is more than 1 square away
    # TODO: Target is 1 square away - cardinal
    # TODO: Target is 1 square away - diagonal


@pytest.mark.skip(reason='Convert to Component later')
def test_GridMoveAI_is_Component():
    player = copy.deepcopy(factories.player)
    ai = components.ai.GridMoveAI(player)
    assert isinstance(ai, Component)


def test_GridMoveAI_init():
    player = copy.deepcopy(factories.player)
    ai = components.ai.GridMoveAI(player)
    assert ai.path == []


@pytest.mark.skip(reason='REQUIRES the entity to have a gamemap and enginereference')
def test_GridMoveAI_yield_action():
    player = copy.deepcopy(factories.player)
    ai = components.ai.GridMoveAI(player)
    assert ai.path == []

    # TODO: Target can be anything in addition to the player
    # TODO: Target is not visible
    # TODO: Target is more than 1 square away
    # TODO: Target is 1 square away - cardinal
    # TODO: Target is 1 square away - diagonal


@pytest.mark.skip(reason='Convert to Component later')
def test_ConfusedAI_is_Component():
    player = copy.deepcopy(factories.player)
    ai = components.ai.ConfusedAI(
        entity=player,
        previous_ai=components.ai.HeroControllerAI,
        turns_remaining=4
    )
    assert isinstance(ai, Component)


def test_ConfusedAI_init():
    player = copy.deepcopy(factories.player)
    ai = components.ai.ConfusedAI(
        entity=player,
        previous_ai=components.ai.HeroControllerAI,
        turns_remaining=4
    )
    assert ai.previous_ai == components.ai.HeroControllerAI
    assert ai.turns_remaining == 4


def test_ConfusedAI_yield_action():
    player = copy.deepcopy(factories.player)
    ai = components.ai.ConfusedAI(
        entity=player,
        previous_ai=components.ai.HeroControllerAI,
        turns_remaining=4
    )
    result = ai.yield_action()
    assert isinstance(result, BumpAction)
    assert ai.turns_remaining == 3


def test_ConfusedAI_yield_action__no_turns_remaining():
    player = copy.deepcopy(factories.player)
    ai = components.ai.ConfusedAI(
        entity=player,
        previous_ai=components.ai.HeroControllerAI,
        turns_remaining=4
    )
    ai.yield_action() # 3 remaining
    ai.yield_action() # 2 remaining
    ai.yield_action() # 1 remaining
    ai.yield_action() # 0 remaining

    assert isinstance(player.ai, components.ai.HeroControllerAI)


@pytest.mark.skip(reason='Convert to Component later')
def test_ParalyzedAI_is_Component():
    player = copy.deepcopy(factories.player)
    ai = components.ai.ParalyzedAI(
        entity=player,
        previous_ai=components.ai.HeroControllerAI,
        turns_remaining=4
    )
    assert isinstance(ai, Component)

def test_ParalyzedAI_init():
    player = copy.deepcopy(factories.player)
    ai = components.ai.ParalyzedAI(
        entity=player,
        previous_ai=components.ai.HeroControllerAI,
        turns_remaining=4
    )

    assert ai.previous_ai == components.ai.HeroControllerAI
    assert ai.turns_remaining == 4


@pytest.mark.skip(reason='Requires engine reference')
def test_ParalyzedAI_yield_action():
    player = copy.deepcopy(factories.player)
    ai = components.ai.ParalyzedAI(
        entity=player,
        previous_ai=components.ai.HeroControllerAI,
        turns_remaining=4
    )

    assert ai.previous_ai == components.ai.HeroControllerAI
    assert ai.turns_remaining == 4

    result = ai.yield_action()
    assert isinstance(result, WaitAction)
    assert at.turns_remaining == 3


@pytest.mark.skip(reason='Requires engine reference')
def test_ParalyzedAI_yield_action__no_turns_remaining():
    player = copy.deepcopy(factories.player)
    ai = components.ai.ParalyzedAI(
        entity=player,
        previous_ai=components.ai.HeroControllerAI,
        turns_remaining=4
    )
    ai.yield_action() # 3 remaining
    ai.yield_action() # 2 remaining
    ai.yield_action() # 1 remaining
    ai.yield_action() # 0 remaining

    assert isinstance(player.ai, components.ai.HeroControllerAI)
