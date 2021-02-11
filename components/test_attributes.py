""" Tests for attributes.py """
import copy
import pytest
from src import factory
from .attributes import Attributes


@pytest.fixture
def player():
    return copy.deepcopy(factory.player)


def test_Attributes_ac_property(player):
    f = Attributes(base_ac=15, base_strength=20)
    f.parent = player  # Needs parent to check it's equipment
    assert f.ac == 15  # No bonus


def test_Attributes_ac_bonus_property(player):
    f = Attributes(base_ac=15, base_strength=20)
    f.parent = player  # Needs parent to check it's ai
    # No bonus when player has no equipment
    assert f.ac_bonus == 0


def test_Attributes_strength_property(player):
    f = Attributes(base_ac=15, base_strength=20)
    f.parent = player  # Needs parent to check it's equipment
    assert f.strength == 20  # No bonus


def test_Attributes_strength_bonus_property(player):
    f = Attributes(base_ac=15, base_strength=20)
    f.parent = player  # Needs parent to check it's ai
    # No bonus when player has no equipment
    assert f.strength_bonus == 0


def test_Attributes_dexterity_property(player):
    f = Attributes(base_ac=15, base_strength=20)
    f.parent = player  # Needs parent to check it's equipment
    assert f.dexterity == 10  # Default dex, No bonus


def test_Attributes_dexterity_bonus_property(player):
    f = Attributes(base_ac=15, base_strength=20)
    f.parent = player  # Needs parent to check it's ai
    # No bonus when player has no equipment
    assert f.dexterity_bonus == 0

