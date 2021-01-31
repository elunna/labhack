""" Tests for game_world.py """

import pytest
# Causes circular import
# import game_world


@pytest.mark.skip(reason='Circular import error... ')
def test_GameWorld_init():
    gw = game_world.GameWorld(
        engine=None,
        map_width=10,
        map_height=15,
        max_rooms=5,
        room_min_size=6,
        room_max_size=7,
    )

    assert self.engine is None
    assert self.map_width == 10
    assert self.map_height == 15
    assert self.max_rooms == 5
    assert self.room_min_size == 5
    assert self.room_max_size == 5

