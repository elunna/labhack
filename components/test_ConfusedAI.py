import pytest

from actions.bump_action import BumpAction
from components import ai
from components.component import Component


def test_init_is_Component():
    confused_ai = ai.ConfusedAI(
        previous_ai=ai.HostileAI,
        turns_remaining=4
    )
    assert isinstance(confused_ai, Component)


@pytest.mark.skip(reason='Engine reference issues')
def test_init(player):
    confused_ai = ai.ConfusedAI(
        previous_ai=ai.HostileAI,
        turns_remaining=4
    )
    assert confused_ai.previous_ai == ai.HostileAI
    assert confused_ai.turns_remaining == 4


@pytest.mark.skip(reason='Engine reference issues')
def test_perform(player):
    confused_ai = ai.ConfusedAI(
        previous_ai=ai.HostileAI,
        turns_remaining=4
    )
    result = confused_ai.yield_action()
    assert isinstance(result, BumpAction)
    assert confused_ai.turns_remaining == 3


@pytest.mark.skip(reason='Engine reference issues')
def test_perform__no_turns_remaining(player):
    confused_ai = ai.ConfusedAI(
        previous_ai=ai.HostileAI,
        turns_remaining=4
    )
    confused_ai.yield_action()  # 3 remaining
    confused_ai.yield_action()  # 2 remaining
    confused_ai.yield_action()  # 1 remaining
    confused_ai.yield_action()  # 0 remaining

    assert isinstance(player.ai, ai.HostileAI)