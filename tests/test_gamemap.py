""" Tests for gamemap.py """

import pytest
import game_map

@pytest.fixture
def test_map():
    return game_map.GameMap(width=10, height=15)

def test_GameMap_init(test_map):
    assert test_map.width == 10
    assert test_map.height == 15
    assert test_map.entities == set()

    # g.tiles
    # TODO: Test that all the starting tiles are walls.
    assert len(test_map.tiles) == 10

    # g.visible
    assert len(test_map.visible) == 10
    assert not test_map.visible.all()  # By default none should be visible

    # self.explored
    assert len(test_map.explored) == 10
    assert not test_map.explored.all()  # By default none should be explored

    # This should default to 0,0
    assert test_map.downstairs_location == (0, 0)


def test_GameMap_gamemap(test_map):
    assert test_map.gamemap is test_map


def test_GameMap_actors__none_by_default(test_map):
    # We get a generator, need to convert to list.
    assert list(test_map.actors) == []


def test_GameMap_items__none_by_default(test_map):
    # We get a generator, need to convert to list.
    assert list(test_map.items) == []


# TODO: Test with walkable tile
# TODO: Test with blocking entity
def test_GameMap_get_blocking_entity_at_location(test_map):
    assert test_map.get_blocking_entity_at_location(0, 0) is None


# TODO: Test with walkable tile
# TODO: Test with blocking entity
def test_GameMap_get_actor_at_location(test_map):
    assert test_map.get_actor_at_location(0, 0) is None


def test_GameMap_in_bounds__valid_loc(test_map):
    assert test_map.in_bounds(0, 0)
    assert test_map.in_bounds(9, 14)


def test_GameMap_in_bounds__invalid_loc(test_map):
    assert not test_map.in_bounds(-1, -1)
    assert not test_map.in_bounds(10, 15)
