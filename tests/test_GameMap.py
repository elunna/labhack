""" Tests for gamemap.py """
from components.item_comp import ItemComponent
from components.stackable import StackableComponent
from src import factory, gamemap, room, tiles
from src.entity import Entity
import pytest
import toolkit


@pytest.fixture
def std_map():
    return gamemap.GameMap(width=10, height=15)


@pytest.fixture
def test_map():
    return toolkit.test_map()


@pytest.fixture
def room_map():
    m = gamemap.GameMap(width=20, height=20)
    a = room.Room(0, 0, 3, 3)
    b = room.Room(4, 0, 3, 3)
    c = room.Room(0, 5, 3, 3)
    d = room.Room(4, 4, 3, 3)
    for i, r in enumerate([a, b, c, d]):
        r.label = i
        m.rooms.append(r)
    m.room_coords = m.room_coordinates()
    return m


@pytest.fixture
def player():
    p = toolkit.cp_player()
    p.parent = None  # Gotta set this...
    return p


@pytest.fixture
def testitem():
    e = Entity(
        x=0, y=0,
        name="fleepgork",
        item=ItemComponent(),
        stackable=StackableComponent(),
    )
    e.item.size = 10
    return e


def test_init__engine(std_map):
    assert std_map.engine is None


def test_init__width_height(std_map):
    assert std_map.width == 10
    assert std_map.height == 15


def test_init__rooms(std_map):
    assert std_map.rooms == []


def test_init__doors(std_map):
    assert std_map.doors == []


def test_init__stairs_locations(std_map):
    # This should default to 0,0
    assert std_map.downstairs_location == (-1, -1)
    assert std_map.upstairs_location == (-1, -1)


def test_init__room_coords(std_map):
    assert std_map.room_coords is None


def test_init__tiles(std_map):
    assert len(std_map.tiles) == 10


def test_init__visible_tiles(std_map):
    assert len(std_map.visible) == 10
    assert not std_map.visible.all()  # By default none should be visible


def test_init__explored_tiles(std_map):
    assert len(std_map.explored) == 10
    assert not std_map.explored.all()  # By default none should be explored


def test_gamemap_property(test_map):
    assert test_map.gamemap is test_map


def test_actors_property(std_map):
    assert list(std_map.actors) == []  # None by default
    f = factory.make("mouse")
    std_map.add_entity(f)
    assert f in std_map.actors


def test_items_property_none_by_default(std_map):
    # We get a generator, need to convert to list.
    assert list(std_map.items) == []  # None by default
    i = Entity(name="item", item=True)
    std_map.add_entity(i)
    assert i in std_map.items


def test_in_bounds__valid_loc(test_map):
    # test_map is a 6x6 map
    assert test_map.in_bounds(0, 0)
    assert test_map.in_bounds(5, 5)


def test_in_bounds__invalid_loc(test_map):
    # test_map is a 6x6 map
    assert not test_map.in_bounds(-1, -1)
    assert not test_map.in_bounds(10, 15)


def test_get_names_at__no_visible(test_map):
    result = test_map.get_names_at(0, 1)
    assert result == ""


def test_get_names_at__visible(test_map):
    # Set map tile to visible
    test_map.visible[5, 5] = True

    result = test_map.get_names_at(5, 5)
    assert result == "Player"


def test_get_names_at__multiple_visible(test_map):
    vial = factory.make("healing vial")
    assert test_map.place(vial, 5, 5)

    # Set map tile to visible
    test_map.visible[5, 5] = True

    result = test_map.get_names_at(5, 5)
    assert result == "Healing vial, Player"


def test_walkable__wall_tile(test_map):
    # test_map: 0, 0 is a wall
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
        (0, 0): r, (0, 1): r, (0, 2): r,
        (1, 0): r, (1, 1): r, (1, 2): r,
        (2, 0): r, (2, 1): r, (2, 2): r,
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


def test_get_nearest_unconnected_room__no_connections(room_map):
    a = room_map.rooms[0]
    b = room_map.rooms[1]
    c = room_map.rooms[2]
    d = room_map.rooms[3]
    assert room_map.get_nearest_unconnected_room(a) == b
    assert room_map.get_nearest_unconnected_room(c) == d

    # This should be b... must be a rounding issue
    assert room_map.get_nearest_unconnected_room(d) == c


# def test_get_nearest_unconnected_room__connections(room_map):


def test_on_edge_of_map__x_is_0__returns_True():
    m = gamemap.GameMap(width=20, height=20)
    assert m.on_edge_of_map(x=0, y=5)


def test_on_edge_of_map__y_is_0__returns_True():
    m = gamemap.GameMap(width=20, height=20)
    assert m.on_edge_of_map(x=5, y=0)


def test_on_edge_of_map__x_1off_from_width__returns_True():
    m = gamemap.GameMap(width=20, height=20)
    assert m.on_edge_of_map(x=19, y=5)


def test_on_edge_of_map__y_1off_from_height__returns_True():
    m = gamemap.GameMap(width=20, height=20)
    assert m.on_edge_of_map(x=5, y=19)


def test_on_edge_of_map__middle_of_map__returns_False():
    m = gamemap.GameMap(width=20, height=20)
    assert m.on_edge_of_map(x=10, y=10) is False


def test_get_random_unoccupied_tile__all_wall():
    m = gamemap.GameMap(width=3, height=3)
    result = m.get_random_unoccupied_tile()
    assert result is None


def test_get_random_unoccupied_tile__1_valid_tile():
    m = gamemap.GameMap(width=3, height=3)
    m.tiles[1][1] = tiles.floor
    result = m.get_random_unoccupied_tile()
    assert result == (1, 1)


def test_get_random_unoccupied_tile__1floor_1actor(player):
    m = gamemap.GameMap(width=3, height=3)
    m.tiles[0][0] = tiles.floor
    m.tiles[1][1] = tiles.floor
    m.place(player, 0, 0)

    result = m.get_random_unoccupied_tile()
    assert result == (1, 1)


def test_get_actor_at__DNE_returns_None(std_map):
    assert std_map.get_actor_at(0, 0) is None


def test_get_actor_at__valid_actor(std_map):
    e = factory.make("mouse")
    std_map.place(e, 1, 1)
    result = std_map.get_actor_at(1, 1)
    assert result == e


def test_get_trap_at__DNE_returns_None(std_map):
    assert std_map.get_trap_at(0, 0) is None


def test_get_trap_at__valid_actor(std_map):
    e = Entity(name="banana trap", x=1, y=1, trap=True)
    std_map.add_entity(e)
    assert std_map.get_trap_at(1, 1) == e


def test_place__success_returns_True(std_map):
    e = Entity(name="fleeb")
    assert std_map.place(e, 2, 3)
    assert e in std_map


def test_place__calls_add_entity(std_map, mocker):
    mocker.patch('src.entity_manager.EntityManager.add_entity')
    e = Entity(name="fleeb")
    std_map.place(e, 2, 3)
    std_map.add_entity.assert_called_once()


def test_place__updates_xy(std_map):
    e = Entity(name="fleeb")
    std_map.place(e, 2, 3)
    assert e.x == 2
    assert e.y == 3
