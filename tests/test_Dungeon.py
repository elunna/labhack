from src import dungeon, exceptions
from src.gamemap import GameMap
from tests import toolkit
from types import SimpleNamespace
import pytest


@pytest.fixture
def test_dungeon():
    # Create a dungeon with 3 floors and adds the player to the floor 2 for easy testing situations.
    player = toolkit.cp_player()
    e = SimpleNamespace(game_map='testmap')
    d = dungeon.Dungeon(e)
    d.generate_floor()  # Floor 2
    d.generate_floor()  # Floor 3

    d.place_entity(player, 2, 0, 0)  # Put the player on level 2
    d.current_map.player = player  # We'll set this manually
    assert d.dlevel == 2
    return d


def test_init__dlevel():
    d = dungeon.Dungeon()
    assert d.dlevel == 1


def test_init__map_list():
    d = dungeon.Dungeon()
    assert d.map_list == [d.current_map]


def test_current_map():
    d = dungeon.Dungeon()
    assert d.current_map == d.map_list[0]


def test_generate_map__added_to_map_list():
    d = dungeon.Dungeon()
    assert len(d.map_list) == 1
    d.generate_floor()
    assert len(d.map_list) == 2


def test_generate_map__returns_GameMap():
    d = dungeon.Dungeon()
    result = d.generate_floor()
    assert isinstance(result, GameMap)


@pytest.mark.skip(reason="Deal with populate")
def test_generate_map__calls_populate():
    pass


def test_move_downstairs__next_level_DNE__return_False(test_dungeon):
    player = test_dungeon.current_map.player
    test_dungeon.place_entity(entity=player, map_num=3, x=0, y=0)
    assert len(test_dungeon.map_list) == 3

    assert test_dungeon.move_downstairs(entity=player) is False


def test_move_downstairs__success_returns_True(test_dungeon):
    player = test_dungeon.current_map.player
    assert test_dungeon.move_downstairs(entity=player)


def test_move_downstairs__dlevel_increments(test_dungeon):
    player = test_dungeon.current_map.player
    assert test_dungeon.dlevel == 2

    test_dungeon.move_downstairs(entity=player)
    assert test_dungeon.dlevel == 3


def test_move_downstairs__entity_moved_to_next_upstair(test_dungeon):
    player = test_dungeon.current_map.player
    test_dungeon.move_downstairs(entity=player)
    x, y = test_dungeon.current_map.upstairs_location
    assert player.x == x and player.y == y


def test_move_downstairs__player_unset_on_old_map(test_dungeon):
    player = test_dungeon.current_map.player
    old_map = test_dungeon.current_map
    test_dungeon.move_downstairs(entity=player)
    assert old_map.player is None


def test_move_downstairs__player_set_on_new_map(test_dungeon):
    player = test_dungeon.current_map.player
    test_dungeon.move_downstairs(entity=player)
    assert test_dungeon.current_map.player == player


def test_move_upstairs__level_1__returns_False(test_dungeon):
    player = test_dungeon.current_map.player
    test_dungeon.place_entity(player, 1, 0, 0)  # Put the player on level 1

    assert test_dungeon.dlevel == 1
    assert test_dungeon.move_upstairs(entity=player) is False


def test_move_upstairs__success_returns_True(test_dungeon):
    player = test_dungeon.current_map.player
    assert test_dungeon.move_upstairs(entity=player)


def test_move_upstairs__dlevel_decrements(test_dungeon):
    player = test_dungeon.current_map.player
    assert test_dungeon.dlevel == 2

    test_dungeon.move_upstairs(entity=player)
    assert test_dungeon.dlevel == 1


def test_move_upstairs__entity_moves_to_previous_downstair(test_dungeon):
    player = test_dungeon.current_map.player

    test_dungeon.move_upstairs(entity=player)
    x, y = test_dungeon.current_map.downstairs_location
    assert player.x == x and player.y == y


def test_move_upstairs__player_unset_on_old_map(test_dungeon):
    player = test_dungeon.current_map.player

    old_map = test_dungeon.current_map
    test_dungeon.move_upstairs(entity=player)
    assert old_map.player is None


def test_move_upstairs__player_set_on_new_map(test_dungeon):
    player = test_dungeon.current_map.player

    test_dungeon.move_upstairs(entity=player)
    assert test_dungeon.current_map.player == player


def test_place_entity__to_new_map__dlevel_changes(test_dungeon):
    player = test_dungeon.current_map.player
    assert test_dungeon.dlevel == 2
    expected = 3
    test_dungeon.place_entity(entity=player, map_num=expected, x=0, y=0)
    assert test_dungeon.dlevel == expected


def test_place_entity__to_new_map__updates_entity_parent(test_dungeon):
    player = test_dungeon.current_map.player
    old_parent = player.parent
    test_dungeon.place_entity(entity=player, map_num=1, x=0, y=0)
    assert player.parent != old_parent


def test_place_entity__same_map(test_dungeon):
    player = test_dungeon.current_map.player
    old_map = player.parent
    expected = 2
    assert test_dungeon.dlevel == expected
    test_dungeon.place_entity(entity=player, map_num=expected, x=0, y=0)
    assert player.parent == old_map  # Map should not have changed.
    assert test_dungeon.dlevel == expected


def test_place_entity__updates_entity_coordinates(test_dungeon):
    player = test_dungeon.current_map.player
    test_dungeon.place_entity(entity=player, map_num=1, x=0, y=1)
    assert player.x == 0 and player.y == 1


def test_place_entity__removed_from_old_map(test_dungeon):
    player = test_dungeon.current_map.player
    old_map = test_dungeon.current_map
    test_dungeon.place_entity(entity=player, map_num=3, x=0, y=1)
    assert player not in old_map.entities


def test_place_entity__added_to_new_map(test_dungeon):
    player = test_dungeon.current_map.player
    test_dungeon.place_entity(entity=player, map_num=3, x=0, y=1)
    assert player in test_dungeon.current_map.entities


def test_place_entity__sets_engines_gamemap_ref(test_dungeon):
    player = test_dungeon.current_map.player
    test_dungeon.place_entity(entity=player, map_num=3, x=0, y=1)
    m = test_dungeon.current_map
    assert test_dungeon.engine.game_map == m


def test_place_entity__sets_new_maps_engine_ref(test_dungeon):
    player = test_dungeon.current_map.player
    test_dungeon.place_entity(entity=player, map_num=3, x=0, y=1)
    e = test_dungeon.engine
    assert test_dungeon.current_map.engine == e


def test_set_dlevel__empty_maplist__raise_exception():
    d = dungeon.Dungeon()
    with pytest.raises(ValueError):
        d.set_dlevel(0)


def test_set_dlevel__valid_level():
    d = dungeon.Dungeon()
    d.generate_floor()
    d.generate_floor()
    assert d.set_dlevel(2)
    assert d.dlevel == 2


def test_set_dlevel__invalid_level__raise_exception():
    d = dungeon.Dungeon()
    d.generate_floor()
    with pytest.raises(ValueError):
        d.set_dlevel(99)


# get_map(int)
# add_map
# max_depth_reached_property
