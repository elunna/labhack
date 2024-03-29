""" Tests for equippable.py """

from components.equippable import Equippable
from components.component import Component
import pytest


def test_is_BaseComponent():
    e = Equippable("armor")
    assert isinstance(e, Component)


def test_init__defaults():
    e = Equippable("armor")
    assert e.equipment_type == "armor"


@pytest.mark.skip(reason='Reenable after we get a list of equipment types')
def test_init__invalid_type():
    with pytest.raises(ValueError):
        e = Equippable("phaser")


def test_init__power_bonus():
    e = Equippable("weapon", strength_bonus=1)
    assert e.modifiers['STRENGTH'] == 1


def test_init__defense_bonus():
    e = Equippable("armor", ac_bonus=1)
    assert e.modifiers['AC'] == 1


def test_init__power_bonus_negative():
    e = Equippable("weapon", strength_bonus=-1)
    assert e.modifiers['STRENGTH'] == -1


def test_init__defense_bonus_negative():
    e = Equippable("armor", ac_bonus=-1)
    assert e.modifiers['AC'] == -1


# No tests for Dagger/Sword/Leather Armor/ChainMail
# These are basically derivatives, can probably be made data driven.
