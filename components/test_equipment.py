""" Tests for equipment.py """

from .component import Component
from .equipment import Equipment
from src import exceptions
from src import factory as ef
import pytest


@pytest.fixture
def dagger():
    return ef.dagger


@pytest.fixture
def leather_armor():
    return ef.leather_vest


def test_is_BaseComponent():
    e = Equipment()
    assert isinstance(e, Component)


def test_init():
    e = Equipment()
    assert e.slots['WEAPON'] is None
    assert e.slots['ARMOR'] is None


def test_init__weapon(dagger):
    e = Equipment(dagger)
    assert e.slots['WEAPON'] == dagger
    assert e.slots['ARMOR'] is None


def test_init__weapon__calls_equip(dagger, mocker):
    mocker.patch('components.equipment.Equipment.toggle_equip')
    e = Equipment(dagger)
    e.toggle_equip.assert_called_once()


def test_init__armor__calls_equip(leather_armor, mocker):
    mocker.patch('components.equipment.Equipment.toggle_equip')
    e = Equipment(leather_armor)
    e.toggle_equip.assert_called_once()


def test_init__with_armor(leather_armor):
    e = Equipment(leather_armor)
    assert e.slots['WEAPON'] is None
    assert e.slots['ARMOR'] is leather_armor


def test_attribute_bonus__ac_default_is_0():
    e = Equipment()
    assert e.attribute_bonus('AC') == 0


def test_attribute_bonus__ac_with_armor(leather_armor):
    e = Equipment(leather_armor)
    assert e.attribute_bonus('AC') == leather_armor.equippable.modifiers['AC']


def test_attribute_bonus__strength_default_is_0():
    e = Equipment()
    assert e.attribute_bonus('STRENGTH') == 0


def test_attribute_bonus__strength_with_weapon(dagger):
    e = Equipment(dagger)
    assert e.attribute_bonus('STRENGTH') == dagger.equippable.modifiers['STRENGTH']


def test_item_is_equipped__none_equipped():
    e = Equipment()
    assert e.is_equipped('giant jockstrap') is False


def test_item_is_equipped__weapon_equipped(dagger):
    e = Equipment(dagger)
    assert e.is_equipped(dagger)


def test_item_is_equipped__armor_equipped(leather_armor):
    e = Equipment(leather_armor)
    assert e.is_equipped(leather_armor)


def test_unequip_message(leather_armor):
    e = Equipment(leather_armor)
    result = e.unequip_message(leather_armor.name)
    assert result == "You remove the Leather Vest. "


def test_equip_message(dagger):
    e = Equipment()
    result = e.equip_message(dagger.name)
    assert result == "You equip the Dagger. "


def test_equip_to_slot__weapon_to_weaponslot(dagger):
    e = Equipment()
    e.equip_to_slot(slot="WEAPON", item=dagger)
    assert e.slots['WEAPON'] == dagger


def test_equip_to_slot__msg(dagger):
    e = Equipment()
    result = e.equip_to_slot(slot="WEAPON", item=dagger)
    assert result == 'You equip the Dagger. '


def test_equip_to_slot__armor_to_armorslot(leather_armor):
    e = Equipment()
    e.equip_to_slot(slot="ARMOR", item=leather_armor)
    assert e.slots['ARMOR'] == leather_armor


def test_equip_to_slot__weapon2armorslot__raises_Impossible(dagger):
    # We should not be able to put weapon in an armor slot.
    e = Equipment()
    with pytest.raises(exceptions.Impossible):
        e.equip_to_slot(slot="ARMOR", item=dagger)


def test_equip_to_slot__armor2weaponslot__raises_Impossible(leather_armor):
    # We should not be able to put armor in an weapon slot.
    e = Equipment()
    with pytest.raises(exceptions.Impossible):
        e.equip_to_slot(slot="WEAPON", item=leather_armor)


def test_equip_to_slot__non_equippable():
    potion = ef.health_potion
    e = Equipment()
    with pytest.raises(exceptions.Impossible):
        e.equip_to_slot(slot="WEAPON", item=potion)


def test_unequip_from_slot__weapon(dagger):
    e = Equipment(dagger)
    e.unequip_from_slot(slot="WEAPON")
    assert e.slots['WEAPON'] is None


def test_unequip_from_slot__armor(leather_armor):
    e = Equipment(leather_armor)
    e.unequip_from_slot(slot="ARMOR")
    assert e.slots['ARMOR'] is None


def test_unequip_from_slot__msg(dagger):
    e = Equipment(dagger)
    result = e.unequip_from_slot(slot="WEAPON")
    assert result == 'You remove the Dagger. '


def test_unequip_from_slot__fail_returns_False():
    e = Equipment()
    result = e.unequip_from_slot(slot="ARMOR")
    assert result == "The ARMOR slot is not equipped with anything!"


def test_toggle_equip__none2weapon(dagger):
    e = Equipment()
    e.toggle_equip(item=dagger)
    assert e.slots['WEAPON'] == dagger


def test_toggle_equip__none2weapon__msg(dagger):
    e = Equipment()
    result = e.toggle_equip(item=dagger)
    assert result == "You equip the Dagger. "


def test_toggle_equip__none2armor(leather_armor):
    e = Equipment()
    e.toggle_equip(item=leather_armor)
    assert e.slots['ARMOR'] == leather_armor


def test_toggle_equip__none2armor__msg(leather_armor):
    e = Equipment()
    result = e.toggle_equip(item=leather_armor)
    assert result == "You equip the Leather Vest. "


def test_toggle_equip__weapon2none(dagger):
    e = Equipment(dagger)
    e.toggle_equip(item=dagger)
    assert e.slots['WEAPON'] is None


def test_toggle_equip__weapon2none__msg(dagger):
    e = Equipment(dagger)
    result = e.toggle_equip(item=dagger)
    assert result == "You remove the Dagger. "


def test_toggle_equip__armor2none(leather_armor):
    e = Equipment(leather_armor)
    e.toggle_equip(item=leather_armor)
    assert e.slots['ARMOR'] is None


def test_toggle_equip__armor2none__msg(leather_armor):
    e = Equipment(leather_armor)
    result = e.toggle_equip(item=leather_armor)
    assert result == "You remove the Leather Vest. "


def test_toggle_equip__weapon2weapon(dagger):
    e = Equipment(dagger)
    baton = ef.riot_baton
    e.toggle_equip(item=baton)
    assert e.slots['WEAPON'] == baton


def test_toggle_equip__weapon2weapon__msg(dagger):
    e = Equipment(dagger)
    baton = ef.riot_baton
    result = e.toggle_equip(item=baton)
    assert result == "You remove the Dagger. You equip the Riot Baton. "


def test_toggle_equip__armor2armor(leather_armor):
    e = Equipment(leather_armor)
    bp_vest = ef.bulletproof_vest
    e.toggle_equip(item=bp_vest)
    assert e.slots['ARMOR'] == bp_vest


def test_toggle_equip__armor2armor__msg(leather_armor):
    e = Equipment(leather_armor)
    bp_vest = ef.bulletproof_vest
    result = e.toggle_equip(item=bp_vest)
    assert result == "You remove the Leather Vest. You equip the Bulletproof Vest. "


def test_toggle_equip__non_equippable__raisesImpossible():
    e = Equipment()
    potion = ef.health_potion
    with pytest.raises(exceptions.Impossible):
        e.toggle_equip(item=potion)
