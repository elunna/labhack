""" Tests for attributes.py """
import pytest
from components.attributes import Attributes
from src import player


@pytest.fixture
def test_player():
    return player.Player()


def test_strength_property(test_player):
    f = Attributes(base_strength=20)
    f.parent = test_player  # Needs parent to check it's equipment
    assert f.strength == 20  # No bonus


def test_equipment_bonus__strength(test_player):
    f = Attributes(base_strength=20)
    f.parent = test_player  # Needs parent to check it's ai
    # No bonus when test_player has no equipment
    assert f.equipment_bonus('STRENGTH') == 0


def test_dexterity_property(test_player):
    f = Attributes(base_strength=20)
    f.parent = test_player  # Needs parent to check it's equipment
    assert f.dexterity == 10  # Default dex, No bonus


def test_equipment_bonus__dexterity(test_player):
    f = Attributes(base_strength=20)
    f.parent = test_player  # Needs parent to check it's ai
    # No bonus when test_player has no equipment
    assert f.equipment_bonus('DEXTERITY') == 0
