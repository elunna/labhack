""" Tests for actors.py """

import pytest
import factories
import copy
import actors
import entity

def test_Actor_subclass_of_Entity():
    player = copy.deepcopy(factories.player)
    assert isinstance(player, actors.Actor)
    assert isinstance(player, entity.Entity)


def test_Actor_init_defaults():
    player = copy.deepcopy(factories.player)
    # Just test that Actor has standard components included
    assert player.inventory
    assert player.fighter
    assert player.equipment
    assert player.level
    assert player.energymeter


def test_Actor_is_alive():
    player = copy.deepcopy(factories.player)
    assert player.is_alive
