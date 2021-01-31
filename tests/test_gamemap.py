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


@pytest.mark.skip(reason='Do later')
def test_GameMap_gamemap():
    pass


@pytest.mark.skip(reason='Do later')
def test_GameMap_actors():
    pass


@pytest.mark.skip(reason='Do later')
def test_GameMap_items():
    pass


@pytest.mark.skip(reason='Do later')
def test_GameMap_get_blocking_entity_at_location():
    pass


@pytest.mark.skip(reason='Do later')
def test_GameMap_get_actor_at_location():
    pass


@pytest.mark.skip(reason='Do later')
def test_GameMap_in_bounds():
    pass

