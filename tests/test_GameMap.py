""" Tests for gamemap.py """

from src import factory, gamemap, room, tiles
import pytest
import toolkit


@pytest.fixture
def test_map():
    return toolkit.test_map()


@pytest.fixture
def player():
    p = toolkit.cp_player()
    p.parent = None  # Gotta set this...
    return p


def test_init():
    m = gamemap.GameMap(width=10, height=15)
    assert m.width == 10
    assert m.height == 15
    assert m.entities == set()

    assert len(m.tiles) == 10

    # g.visible
    assert len(m.visible) == 10
    assert not m.visible.all()  # By default none should be visible

    # self.explored
    assert len(m.explored) == 10
    assert not m.explored.all()  # By default none should be explored

    # This should default to 0,0
    assert m.downstairs_location == (-1, -1)
    assert m.upstairs_location == (-1, -1)


def test_contains__entity_not_in_returns_False(player):
    m = gamemap.GameMap(width=10, height=15)
    assert player not in m


def test_contains__entity_inside_returns_True(player):
    m = gamemap.GameMap(width=10, height=15)
    m.add_entity(player, 0, 0)
    assert player in m


def test_gamemap(test_map):
    assert test_map.gamemap is test_map


def test_actors(test_map):
    # We get a generator, need to convert to list.
    # assert list(test_map.actors) == []
    # There are 2 actors in the test_map: Player and gridbug
    assert len(list(test_map.actors)) == 3


def test_items__none_by_default(test_map):
    # We get a generator, need to convert to list.
    assert list(test_map.items) == []


def test_add_entity__success_returns_True(player):
    g = gamemap.GameMap(width=10, height=15)
    assert g.add_entity(player, 0, 0)


def test_add_entity__not_an_Entity_returns_False(player):
    g = gamemap.GameMap(width=10, height=15)
    assert g.add_entity('x', 0, 0) is False


def test_add_entity__already_in_map_returns_False(test_map):
    player = test_map.player
    assert test_map.add_entity(player, 0, 0) is False


def test_add_entity__out_of_bounds_returns_False(player):
    g = gamemap.GameMap(width=10, height=15)
    assert g.add_entity(player, -5, -5) is False


def test_add_entity__updates_entity_coordinates(player):
    g = gamemap.GameMap(width=10, height=15)
    assert player.x == 0 and player.y == 0
    g.add_entity(player, 3, 2)
    assert player.x == 3 and player.y == 2


def test_add_entity__updates_entity_parent(player):
    g = gamemap.GameMap(width=10, height=15)
    assert player.parent is None
    g.add_entity(player, 0, 0)
    assert player.parent == g


def test_add_entity__added_to_map_entities(player):
    g = gamemap.GameMap(width=10, height=15)
    g.add_entity(player, 0, 0)
    assert player in g


def test_add_entity__removed_from_previous_parent(test_map):
    player = test_map.player
    assert player.parent == test_map

    g = gamemap.GameMap(width=10, height=15)
    g.add_entity(player, 0, 0)
    assert player not in test_map


def test_rm_entity__success_returns_True(test_map):
    player = test_map.player
    assert test_map.rm_entity(player)


def test_rm_entity__not_in_map_returns_False(test_map):
    assert test_map.rm_entity('x') is False


def test_rm_entity__removed_from_map_entities(test_map):
    player = test_map.player
    test_map.rm_entity(player)
    assert player not in test_map


def test_rm_entity__updates_entity_parent_to_None(test_map):
    player = test_map.player
    assert player.parent == test_map
    test_map.rm_entity(player)
    assert player.parent is None


def test_rm_entity__updates_entity_coords(test_map):
    player = test_map.player
    test_map.rm_entity(player)
    assert player.x == -1 and player.y == -1


def test_get_blocking_entity_at_location__walls(test_map):
    assert test_map.blocking_entity_at(0, 0) is None


def test_get_blocking_entity_at_location__floors(test_map):
    assert test_map.blocking_entity_at(0, 0) is None


def test_get_blocking_entity_at_location__valid_blocker(test_map):
    # test_map has player at (5, 5)
    result = test_map.blocking_entity_at(5, 5)
    assert result.name == "Player"


def test_get_actor_at_location__empty_tile(test_map):
    result = test_map.get_actor_at(0, 0)
    assert result is None


def test_get_actor_at_location__valid_actor(test_map):
    result = test_map.get_actor_at(5, 5)
    assert result.name == "Player"


def test_in_bounds__valid_loc(test_map):
    # test_map is a 6x6 map
    assert test_map.in_bounds(0, 0)
    assert test_map.in_bounds(5, 5)


def test_in_bounds__invalid_loc(test_map):
    # test_map is a 6x6 map
    assert not test_map.in_bounds(-1, -1)
    assert not test_map.in_bounds(10, 15)


@pytest.mark.skip(reason='Need to create walkable')
def test_walkable__wall_tile(test_map):
    # test_map: 0, 0 is a wall
    assert not test_map.walkable(0, 0)


@pytest.mark.skip(reason='Need to create walkable')
def test_walkable__floor_tile(test_map):
    # test_map: 5, 5 is a floor
    assert test_map.walkable(5, 5)


@pytest.mark.skip(reason='Need to import from rendering_functions')
def test_get_names_at__no_visible(test_map):
    result = test_map.get_names_at(0, 1)
    assert result == ""


@pytest.mark.skip(reason='Need to import from rendering_functions')
def test_get_names_at__visible(test_map):
    # Set map tile to visible
    test_map.visible[5, 5] = True

    result = test_map.get_names_at(5, 5)
    assert result == "Player"


@pytest.mark.skip(reason='Need to import from rendering_functions')
def test_get_names_at__multiple_visible(test_map):
    potion = factory.health_potion
    test_map.add_entity(potion, 5, 5)

    # Set map tile to visible
    test_map.visible[5, 5] = True

    result = test_map.get_names_at(5, 5)
    assert result == "Health potion, Player"


def test_walkable__all_walls(test_map):
    assert not test_map.walkable(0, 0)


def test_walkable__all_floor(test_map):
    # Open floor at 5, 4
    assert test_map.walkable(5, 4)
    # Player is on the floor at 5, 5
    assert test_map.walkable(5, 5)


def test_room_coordinates():
    m = gamemap.GameMap(width=20, height=20)
    r = room.Room(0, 0, 3, 3)
    m.rooms.append(r)

    result = m.room_coordinates()
    assert result == {
        (0, 0): r,
        (0, 1): r,
        (0, 2): r,
        (1, 0): r,
        (1, 1): r,
        (1, 2): r,
        (2, 0): r,
        (2, 1): r,
        (2, 2): r,
    }


def test_tiles_around__radius_of_0__raises_ValueError():
    with pytest.raises(ValueError):
        gamemap.GameMap.tiles_around(x=3, y=3, radius=0)


def test_tiles_around__radius_of_1():
    result = gamemap.GameMap.tiles_around(x=3, y=3, radius=1)
    assert result == {
        (2, 2), (3, 2), (4, 2),
        (2, 3), (4, 3),
        (2, 4), (3, 4), (4, 4),
    }


def test_valid_door_neighbors__facing_north():
    m = gamemap.GameMap(width=10, height=10)
    r = room.Room(1, 1, 3, 3)
    m.rooms.append(r)
    # Need to set the tiles for the flanking check!
    m.tiles[1][1] = tiles.room_nw_corner
    m.tiles[3][1] = tiles.room_ne_corner
    assert m.valid_door_neighbors(r, 2, 1)


def test_valid_door_neighbors__facing_south():
    m = gamemap.GameMap(width=10, height=10)
    r = room.Room(1, 1, 3, 3)
    m.rooms.append(r)
    # Need to set the tiles for the flanking check!
    m.tiles[1][3] = tiles.room_sw_corner
    m.tiles[3][3] = tiles.room_se_corner
    assert m.valid_door_neighbors(r, 2, 3)


def test_valid_door_neighbors__facing_east():
    m = gamemap.GameMap(width=10, height=10)
    r = room.Room(1, 1, 3, 3)
    m.rooms.append(r)
    # Need to set the tiles for the flanking check!
    m.tiles[3][1] = tiles.room_ne_corner
    m.tiles[3][3] = tiles.room_se_corner
    assert m.valid_door_neighbors(r, 3, 2)


def test_valid_door_neighbors__facing_west():
    m = gamemap.GameMap(width=10, height=10)
    r = room.Room(1, 1, 3, 3)
    m.rooms.append(r)
    m.rooms.append(r)
    # Need to set the tiles for the flanking check!
    m.tiles[1][1] = tiles.room_nw_corner
    m.tiles[1][3] = tiles.room_sw_corner
    assert m.valid_door_neighbors(r, 1, 2)


def test_valid_door_neighbors__corner_returns_false():
    m = gamemap.GameMap(width=20, height=20)
    r = room.Room(0, 0, 3, 3)
    m.rooms.append(r)
    assert not m.valid_door_neighbors(r, 0, 0)


def test_valid_door_neighbors__no_closet_space_west():
    m = gamemap.GameMap(width=20, height=20)
    r = room.Room(0, 0, 3, 3)
    m.rooms.append(r)
    assert not m.valid_door_neighbors(r, 0, 1)


def test_valid_door_neighbors__no_closet_space_north():
    m = gamemap.GameMap(width=20, height=20)
    r = room.Room(0, 0, 10, 3)
    m.rooms.append(r)
    assert not m.valid_door_neighbors(r, 1, 0)


def test_valid_door_neighbors_walls__next_to_floor__facing_south():
    m = gamemap.GameMap(width=20, height=20)
    r = room.Room(0, 0, 10, 3)
    m.rooms.append(r)
    m.tiles[0][2] = tiles.floor
    assert not m.valid_door_neighbors(r, 1, 2)


def test_valid_door_neighbors__next_to_floors__facing_south():
    m = gamemap.GameMap(width=20, height=20)
    r = room.Room(0, 0, 10, 3)
    m.rooms.append(r)
    m.tiles[3][2] = tiles.floor
    m.tiles[5][2] = tiles.floor
    assert not m.valid_door_neighbors(r, 4, 2)


def test_valid_door_neighbors__next_to_floor__facing_east():
    m = gamemap.GameMap(width=20, height=20)
    r = room.Room(0, 0, 10, 3)
    m.rooms.append(r)
    m.tiles[9][0] = tiles.floor
    assert not m.valid_door_neighbors(r, 9, 1)
