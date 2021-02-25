""" Tests for attributes.py """
import pytest
from src import factory
from .attributes import Attributes


@pytest.fixture
def player():
    return factory.make("player")


def test_ac_property(player):
    f = Attributes(base_ac=15, base_strength=20)
    f.parent = player  # Needs parent to check it's equipment
    assert f.ac == 15  # No bonus


def test_equipment_bonus__ac(player):
    f = Attributes(base_ac=15, base_strength=20)
    f.parent = player  # Needs parent to check it's ai
    # No bonus when player has no equipment
    assert f.equipment_bonus('AC') == 0


def test_strength_property(player):
    f = Attributes(base_ac=15, base_strength=20)
    f.parent = player  # Needs parent to check it's equipment
    assert f.strength == 20  # No bonus


def test_equipment_bonus__strength(player):
    f = Attributes(base_ac=15, base_strength=20)
    f.parent = player  # Needs parent to check it's ai
    # No bonus when player has no equipment
    assert f.equipment_bonus('STRENGTH') == 0


def test_dexterity_property(player):
    f = Attributes(base_ac=15, base_strength=20)
    f.parent = player  # Needs parent to check it's equipment
    assert f.dexterity == 10  # Default dex, No bonus


def test_equipment_bonus__dexterity(player):
    f = Attributes(base_ac=15, base_strength=20)
    f.parent = player  # Needs parent to check it's ai
    # No bonus when player has no equipment
    assert f.equipment_bonus('DEXTERITY') == 0

