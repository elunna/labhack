""" Tests for ai.py """
from components import ai
from components.component import Component
from src import gamemap
from src import tiles
from src.engine import Engine
from tests import toolkit
import pytest


@pytest.fixture
def player():
    new_map = toolkit.test_map()
    return new_map.player


@pytest.fixture
def empty_map():
    return gamemap.GameMap(
        width=10,
        height=10,
        fill_tile=tiles.floor
    )


def test_init__is_Component():
    base_ai = ai.BaseAI()
    assert isinstance(base_ai, Component)


@pytest.mark.skip(reason='Should we handle entity not having a gamemap/engine?')
def test_engine(player):
    base_ai = ai.BaseAI(player)
    result = base_ai.engine
    assert isinstance(result, Engine)


def test_perform():
    # This is not implemented in the Component class.
    base_ai = ai.BaseAI()
    with pytest.raises(NotImplementedError):
        base_ai.yield_action()


@pytest.mark.skip(reason='REQUIRES the entity to have a gamemap reference')
def test_get_path_to():
    base_ai = ai.BaseAI()
    result = base_ai.engine
    assert isinstance(result, Engine)
