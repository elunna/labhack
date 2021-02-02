""" Tests for gamemap.py """

import copy
import factories
import game_map
import pytest
import tile_types

@pytest.fixture
def test_map():
    return game_map.GameMap(width=10, height=15)

@pytest.fixture
def empty_map():
    return game_map.GameMap(width=10, height=10, fill_tile=tile_types.floor)


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


def test_GameMap_get_blocker_at__walls(test_map):
    assert test_map.get_blocker_at(0, 0) is None


def test_GameMap_get_blocker_at__floors(empty_map):
    assert empty_map.get_blocker_at(0, 0) is None


def test_GameMap_get_blocker_at__valid_blocker(empty_map):
    player = copy.deepcopy(factories.player)
    player.place(0, 0, empty_map)
    assert empty_map.get_blocker_at(0, 0) is player


def test_GameMap_get_actor_at(test_map):
    assert test_map.get_actor_at(0, 0) is None


def test_GameMap_get_actor_at__valid_actor(empty_map):
    player = copy.deepcopy(factories.player)
    player.place(0, 0, empty_map)
    assert empty_map.get_actor_at(0, 0) is player


def test_GameMap_in_bounds__valid_loc(test_map):
    assert test_map.in_bounds(0, 0)
    assert test_map.in_bounds(9, 14)


def test_GameMap_in_bounds__invalid_loc(test_map):
    assert not test_map.in_bounds(-1, -1)
    assert not test_map.in_bounds(10, 15)


def test_GameMap_walkable__all_walls(test_map):
    assert not test_map.walkable(0, 0)


def test_GameMap_walkable__all_floor(test_map):
    test_map.tiles[0:, 0:] = tile_types.floor
    assert test_map.walkable(0, 0)
    assert test_map.walkable(9, 14)


def test_GameMap_get_names_at__no_visible(empty_map):
    player = copy.deepcopy(factories.player)
    player.place(0, 0, empty_map)
    result = empty_map.get_names_at(0, 1)
    assert result == ""


def test_GameMap_get_names_at__visible(empty_map):
    player = copy.deepcopy(factories.player)
    player.place(0, 0, empty_map)

    # Set map tile to visible
    empty_map.visible[0, 0] = True

    result = empty_map.get_names_at(0, 0)
    assert result == "Player"


def test_GameMap_get_names_at__multiple_visible(empty_map):
    player = copy.deepcopy(factories.player)
    player.place(0, 0, empty_map)
    potion = factories.mk_item("health potion")
    potion.place(0, 0, empty_map)

    # Set map tile to visible
    empty_map.visible[0, 0] = True

    result = empty_map.get_names_at(0, 0)
    assert result == "Health potion, Player"
