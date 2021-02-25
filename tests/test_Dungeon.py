import pytest
from src import dungeon
from src.gamemap import GameMap


def test_init__dlevel():
    d = dungeon.Dungeon()
    assert d.dlevel == 0


def test_init__map_list():
    d = dungeon.Dungeon()
    assert d.map_list == []


def test_current_map__none_created_yet():
    d = dungeon.Dungeon()
    assert d.current_map is None


def test_generate_map__added_to_map_list():
    d = dungeon.Dungeon()
    assert len(d.map_list) == 0
    d.generate_floor()
    assert len(d.map_list) == 1


def test_generate_map__returns_GameMap():
    d = dungeon.Dungeon()
    result = d.generate_floor()
    assert isinstance(result, GameMap)


@pytest.mark.skip(reason="Deal with populate")
def test_generate_map__calls_populate():
    pass

# move_downstairs
# move_upstairs
# place_entity


# get_map(int)
# add_map
# max_depth_reached_property