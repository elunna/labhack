""" Tests for gamemap.py """

import pytest
import game_map

def test_GameMap_init():
    g = game_map.GameMap(engine=None, width=10, height=15)
    assert g.engine is None
    assert g.width == 10
    assert g.height == 15
    assert g.entities == set()

    # g.tiles
    # TODO: Test that all the starting tiles are walls.
    assert len(g.tiles) == 10

    # g.visible
    assert len(g.visible) == 10
    assert not g.visible.all()  # By default none should be visible

    # self.explored
    assert len(g.explored) == 10
    assert not g.explored.all()  # By default none should be explored

    # This should default to 0,0
    assert g.downstairs_location == (0, 0)


def test_GameMap_gamemap():
    g = game_map.GameMap(engine=None, width=10, height=15)
    assert g.gamemap is g


def test_GameMap_actors__none_by_default():
    g = game_map.GameMap(engine=None, width=10, height=15)
    # We get a generator, need to convert to list.
    assert list(g.actors) == []


def test_GameMap_items__none_by_default():
    g = game_map.GameMap(engine=None, width=10, height=15)
    # We get a generator, need to convert to list.
    assert list(g.items) == []


# TODO: Test with walkable tile
# TODO: Test with blocking entity
def test_GameMap_get_blocking_entity_at_location():
    g = game_map.GameMap(engine=None, width=10, height=15)
    assert g.get_blocking_entity_at_location(0, 0) is None


# TODO: Test with walkable tile
# TODO: Test with blocking entity
def test_GameMap_get_actor_at_location():
    g = game_map.GameMap(engine=None, width=10, height=15)
    assert g.get_actor_at_location(0, 0) is None


def test_GameMap_in_bounds__valid_loc():
    g = game_map.GameMap(engine=None, width=10, height=15)
    assert g.in_bounds(0, 0)
    assert g.in_bounds(9, 14)


def test_GameMap_in_bounds__invalid_loc():
    g = game_map.GameMap(engine=None, width=10, height=15)
    assert not g.in_bounds(-1, -1)
    assert not g.in_bounds(10, 15)
