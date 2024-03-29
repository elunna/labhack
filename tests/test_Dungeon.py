from src import dungeon, player
from src.gamemap import GameMap
from tests import toolkit
from types import SimpleNamespace
import pytest


@pytest.fixture
def test_dungeon():
    # Create a dungeon with 3 floors and adds the player to the floor 2 for easy testing situations.
    plyr = player.Player()
    e = SimpleNamespace(game_map='testmap', player=plyr)
    d = dungeon.Dungeon(engine=e, test_map=toolkit.stair_map)
    d.generate_floor()  # Floor 2
    d.generate_floor()  # Floor 3

    d.place_entity(plyr, 2, 0, 0)  # Put the player on level 2
    d.current_map.player = plyr  # We'll set this manually
    assert d.dlevel == 2
    return d


@pytest.fixture
def quik_d():
    plyr = player.Player()
    e = SimpleNamespace(game_map='testmap', player=plyr)
    return dungeon.Dungeon(engine=e, test_map=toolkit.stair_map)


def test_init__dlevel(quik_d):
    assert quik_d.dlevel == 1


def test_init__map_list(quik_d):
    assert quik_d.map_list == [quik_d.current_map]


def test_current_map(quik_d):
    assert quik_d.current_map == quik_d.map_list[0]


def test_generate_map__added_to_map_list(quik_d):
    assert len(quik_d.map_list) == 1
    quik_d.generate_floor()
    assert len(quik_d.map_list) == 2


def test_generate_map__returns_GameMap(quik_d):
    result = quik_d.generate_floor()
    assert isinstance(result, GameMap)


def test_generate_map__sets_new_maps_engine_ref():
    e = SimpleNamespace(game_map='testmap', player=player.Player())
    d = dungeon.Dungeon(engine=e, test_map=toolkit.stair_map)
    result = d.generate_floor()
    assert result.engine == e


@pytest.mark.skip(reason="Deal with populate")
def test_generate_map__calls_populate():
    pass


def test_move_downstairs__next_level_DNE__return_False(test_dungeon):
    plyr = test_dungeon.current_map.player
    test_dungeon.place_entity(entity=plyr, map_num=3, x=0, y=0)
    assert len(test_dungeon.map_list) == 3

    assert test_dungeon.move_downstairs(entity=plyr) is False


def test_move_downstairs__success_returns_True(test_dungeon):
    plyr = test_dungeon.current_map.player
    assert test_dungeon.move_downstairs(entity=plyr)


def test_move_downstairs__dlevel_increments(test_dungeon):
    plyr = test_dungeon.current_map.player
    assert test_dungeon.dlevel == 2

    test_dungeon.move_downstairs(entity=plyr)
    assert test_dungeon.dlevel == 3


def test_move_downstairs__entity_moved_to_next_upstair(test_dungeon):
    plyr = test_dungeon.current_map.player
    test_dungeon.move_downstairs(entity=plyr)
    x, y = test_dungeon.current_map.upstairs_location
    assert plyr.x == x and plyr.y == y


def test_move_downstairs__player_unset_on_old_map(test_dungeon):
    plyr = test_dungeon.current_map.player
    old_map = test_dungeon.current_map
    test_dungeon.move_downstairs(entity=plyr)
    assert old_map.player is None


def test_move_downstairs__player_set_on_new_map(test_dungeon):
    plyr = test_dungeon.current_map.player
    test_dungeon.move_downstairs(entity=plyr)
    assert test_dungeon.current_map.player == plyr


def test_move_downstairs__sets_engines_gamemap_ref(test_dungeon):
    plyr = test_dungeon.current_map.player
    test_dungeon.move_downstairs(entity=plyr)
    m = test_dungeon.current_map
    assert test_dungeon.engine.game_map == m


def test_move_upstairs__level_1__returns_False(test_dungeon):
    plyr = test_dungeon.current_map.player
    test_dungeon.place_entity(plyr, 1, 0, 0)  # Put the player on level 1
    assert test_dungeon.dlevel == 1
    assert test_dungeon.move_upstairs(entity=plyr) is False


def test_move_upstairs__success_returns_True(test_dungeon):
    plyr = test_dungeon.current_map.player
    assert test_dungeon.move_upstairs(entity=plyr)


def test_move_upstairs__dlevel_decrements(test_dungeon):
    plyr = test_dungeon.current_map.player
    assert test_dungeon.dlevel == 2
    test_dungeon.move_upstairs(entity=plyr)
    assert test_dungeon.dlevel == 1


def test_move_upstairs__entity_moves_to_previous_downstair(test_dungeon):
    plyr = test_dungeon.current_map.player
    test_dungeon.move_upstairs(entity=plyr)
    x, y = test_dungeon.current_map.downstairs_location
    assert plyr.x == x and plyr.y == y


def test_move_upstairs__player_unset_on_old_map(test_dungeon):
    plyr = test_dungeon.current_map.player
    old_map = test_dungeon.current_map
    test_dungeon.move_upstairs(entity=plyr)
    assert old_map.player is None


def test_move_upstairs__player_set_on_new_map(test_dungeon):
    plyr = test_dungeon.current_map.player
    test_dungeon.move_upstairs(entity=plyr)
    assert test_dungeon.current_map.player == plyr


def test_move_upstairs__sets_engines_gamemap_ref(test_dungeon):
    plyr = test_dungeon.current_map.player
    test_dungeon.move_upstairs(entity=plyr)
    m = test_dungeon.current_map
    assert test_dungeon.engine.game_map == m


def test_place_entity__to_new_map__dlevel_changes(test_dungeon):
    plyr = test_dungeon.current_map.player
    assert test_dungeon.dlevel == 2
    expected = 3
    test_dungeon.place_entity(entity=plyr, map_num=expected, x=0, y=0)
    assert test_dungeon.dlevel == expected


def test_place_entity__to_new_map__updates_entity_parent(test_dungeon):
    plyr = test_dungeon.current_map.player
    old_parent = plyr.parent
    test_dungeon.place_entity(entity=plyr, map_num=1, x=0, y=0)
    assert plyr.parent != old_parent


def test_place_entity__same_map(test_dungeon):
    plyr = test_dungeon.current_map.player
    old_map = plyr.parent
    expected = 2
    assert test_dungeon.dlevel == expected
    test_dungeon.place_entity(entity=plyr, map_num=expected, x=0, y=0)
    assert plyr.parent == old_map  # Map should not have changed.
    assert test_dungeon.dlevel == expected


def test_place_entity__updates_entity_coordinates(test_dungeon):
    plyr = test_dungeon.current_map.player
    test_dungeon.place_entity(entity=plyr, map_num=1, x=0, y=1)
    assert plyr.x == 0 and plyr.y == 1


def test_place_entity__removed_from_old_map(test_dungeon):
    plyr = test_dungeon.current_map.player
    old_map = test_dungeon.current_map
    test_dungeon.place_entity(entity=plyr, map_num=3, x=0, y=1)
    assert plyr not in old_map


def test_place_entity__added_to_new_map(test_dungeon):
    plyr = test_dungeon.current_map.player
    test_dungeon.place_entity(entity=plyr, map_num=3, x=0, y=1)
    assert plyr in test_dungeon.current_map


def test_set_dlevel__empty_maplist__raise_exception(quik_d):
    with pytest.raises(ValueError):
        quik_d.set_dlevel(0)


def test_set_dlevel__valid_level(quik_d):
    quik_d.generate_floor()
    quik_d.generate_floor()
    assert quik_d.set_dlevel(2)
    assert quik_d.dlevel == 2


def test_set_dlevel__invalid_level__raise_exception(quik_d):
    with pytest.raises(ValueError):
        quik_d.set_dlevel(99)


# get_map(int)
# add_map
# max_depth_reached_property
