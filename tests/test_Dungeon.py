import pytest

from src import dungeon, factory
from types import SimpleNamespace
from pytest_mock import mocker


@pytest.fixture
def mockengine():
    return SimpleNamespace(game_map='dungeon')


def test_init__current_level():
    d = dungeon.Dungeon(engine=None)
    assert d.current_floor == 0


def test_init__map_list():
    d = dungeon.Dungeon(engine=None)
    assert d.map_list == []


def test_init__current_map():
    d = dungeon.Dungeon(engine=None)
    assert d.current_map is None


def test_init__engine():
    d = dungeon.Dungeon(engine=None)
    assert d.engine is None


@pytest.mark.skip(reason="Deal with populate")
def test_generate_map__increments_current_floor(mockengine):
    pass

@pytest.mark.skip(reason="Deal with populate")
def test_generate_map__calls_populate(mockengine):
    pass


# set_current_map(level)
# get_map(int)
# add_map
# max_depth_reached_property