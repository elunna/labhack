""" Tests for actors.py """

from src import factory
import copy
from src import actor
from src import entity


def test_Actor_subclass_of_Entity():
    player = copy.deepcopy(factory.player)
    assert isinstance(player, actor.Actor)
    assert isinstance(player, entity.Entity)


def test_Actor_init_defaults():
    player = copy.deepcopy(factory.player)
    # Just test that Actor has standard components included
    assert player.inventory
    assert player.fighter
    assert player.equipment
    assert player.level
    # assert player.energymeter


def test_Actor_is_alive():
    player = copy.deepcopy(factory.player)
    assert player.is_alive
