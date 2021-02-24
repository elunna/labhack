from components import ai
from components.component import Component
import pytest


def test_init_is_Component():
    approach_ai = ai.HostileAI()
    assert isinstance(approach_ai, Component)


def test_init():
    approach_ai = ai.HostileAI()
    assert approach_ai.path == []


@pytest.mark.skip(reason='REQUIRES the entity to have a gamemap and enginereference')
def test_perform():
    approach_ai = ai.HostileAI()
    assert approach_ai.path == []

    # TODO: Target can be anything in addition to the player
    # TODO: Target is not visible
    # TODO: Target is more than 1 square away
    # TODO: Target is 1 square away - cardinal
    # TODO: Target is 1 square away - diagonal