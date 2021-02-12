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
    return ef.leather_armor


def test_Equipment_is_BaseComponent():
    e = Equipment()
    assert isinstance(e, Component)


def test_Equipment_init():
    e = Equipment()
    assert e.slots['WEAPON'] is None
    assert e.slots['ARMOR'] is None

# TODO: Make sure init uses the equip function - we can't equip armor to weapon
# slot, etc...


def test_Equipment_init__weapon(dagger):
    e = Equipment(dagger)
    assert e.slots['WEAPON'] == dagger
    assert e.slots['ARMOR'] is None


def test_Equipment_init__weapon__calls_equip(dagger, mocker):
    mocker.patch('components.equipment.Equipment.toggle_equip')
    e = Equipment(dagger)
    e.toggle_equip.assert_called_once()


def test_Equipment_init__armor__calls_equip(leather_armor, mocker):
    mocker.patch('components.equipment.Equipment.toggle_equip')
    e = Equipment(leather_armor)
    e.toggle_equip.assert_called_once()


def test_Equipment_init__with_armor(leather_armor):
    e = Equipment(leather_armor)
    assert e.slots['WEAPON'] is None
    assert e.slots['ARMOR'] is leather_armor


def test_Equipment_defense_bonus__default_is_0():
    e = Equipment()
    assert e.ac_bonus == 0


def test_Equipment_defense_bonus__with_armor(leather_armor):
    e = Equipment(leather_armor)
    assert e.ac_bonus == leather_armor.equippable.modifiers['AC']


def test_Equipment_power_bonus__default_is_0():
    e = Equipment()
    assert e.strength_bonus == 0


def test_Equipment_power_bonus__with_weapon(dagger):
    e = Equipment(dagger)
    assert e.strength_bonus == dagger.equippable.modifiers['STRENGTH']


def test_Equipment_item_is_equipped__none_equipped():
    e = Equipment()
    assert e.item_is_equipped('giant jockstrap') is False


def test_Equipment_item_is_equipped__weapon_equipped(dagger):
    e = Equipment(dagger)
    assert e.item_is_equipped(dagger)


def test_Equipment_item_is_equipped__armor_equipped(leather_armor):
    e = Equipment(leather_armor)
    assert e.item_is_equipped(leather_armor)


def test_Equipment_unequip_message(leather_armor):
    e = Equipment(leather_armor)
    result = e.unequip_message(leather_armor.name)
    assert result == "You remove the Leather Armor. "


def test_Equipment_equip_message(dagger):
    e = Equipment()
    result = e.equip_message(dagger.name)
    assert result == "You equip the Dagger. "


def test_Equipment_equip_to_slot__weapon_to_weaponslot(dagger):
    e = Equipment()
    e.equip_to_slot(slot="WEAPON", item=dagger)
    assert e.slots['WEAPON'] == dagger


def test_Equipment_equip_to_slot__msg(dagger):
    e = Equipment()
    result = e.equip_to_slot(slot="WEAPON", item=dagger)
    assert result == 'You equip the Dagger. '


def test_Equipment_equip_to_slot__armor_to_armorslot(leather_armor):
    e = Equipment()
    e.equip_to_slot(slot="ARMOR", item=leather_armor)
    assert e.slots['ARMOR'] == leather_armor


def test_Equipment_equip_to_slot__weapon2armorslot__raises_Impossible(dagger):
    # We should not be able to put weapon in an armor slot.
    e = Equipment()
    with pytest.raises(exceptions.Impossible):
        e.equip_to_slot(slot="ARMOR", item=dagger)


def test_Equipment_equip_to_slot__armor2weaponslot__raises_Impossible(leather_armor):
    # We should not be able to put armor in an weapon slot.
    e = Equipment()
    with pytest.raises(exceptions.Impossible):
        e.equip_to_slot(slot="WEAPON", item=leather_armor)


def test_Equipment_equip_to_slot__non_equippable():
    potion = ef.health_potion
    e = Equipment()
    with pytest.raises(exceptions.Impossible):
        e.equip_to_slot(slot="WEAPON", item=potion)


def test_Equipment_unequip_from_slot__weapon(dagger):
    e = Equipment(dagger)
    e.unequip_from_slot(slot="WEAPON")
    assert e.slots['WEAPON'] is None


def test_Equipment_unequip_from_slot__armor(leather_armor):
    e = Equipment(leather_armor)
    e.unequip_from_slot(slot="ARMOR")
    assert e.slots['ARMOR'] is None


def test_Equipment_unequip_from_slot__msg(dagger):
    e = Equipment(dagger)
    result = e.unequip_from_slot(slot="WEAPON")
    assert result == 'You remove the Dagger. '


def test_Equipment_unequip_from_slot__fail_returns_False():
    e = Equipment()
    result = e.unequip_from_slot(slot="ARMOR")
    assert result == "The ARMOR slot is not equipped with anything!"


def test_Equipment_toggle_equip__none2weapon(dagger):
    e = Equipment()
    e.toggle_equip(item=dagger)
    assert e.slots['WEAPON'] == dagger


def test_Equipment_toggle_equip__none2weapon__msg(dagger):
    e = Equipment()
    result = e.toggle_equip(item=dagger)
    assert result == "You equip the Dagger. "


def test_Equipment_toggle_equip__none2armor(leather_armor):
    e = Equipment()
    e.toggle_equip(item=leather_armor)
    assert e.slots['ARMOR'] == leather_armor


def test_Equipment_toggle_equip__none2armor__msg(leather_armor):
    e = Equipment()
    result = e.toggle_equip(item=leather_armor)
    assert result == "You equip the Leather Armor. "


def test_Equipment_toggle_equip__weapon2none(dagger):
    e = Equipment(dagger)
    e.toggle_equip(item=dagger)
    assert e.slots['WEAPON'] is None


def test_Equipment_toggle_equip__weapon2none__msg(dagger):
    e = Equipment(dagger)
    result = e.toggle_equip(item=dagger)
    assert result == "You remove the Dagger. "


def test_Equipment_toggle_equip__armor2none(leather_armor):
    e = Equipment(leather_armor)
    e.toggle_equip(item=leather_armor)
    assert e.slots['ARMOR'] is None


def test_Equipment_toggle_equip__armor2none__msg(leather_armor):
    e = Equipment(leather_armor)
    result = e.toggle_equip(item=leather_armor)
    assert result == "You remove the Leather Armor. "


def test_Equipment_toggle_equip__weapon2weapon(dagger):
    e = Equipment(dagger)
    sword = ef.sword
    e.toggle_equip(item=sword)
    assert e.slots['WEAPON'] == sword


def test_Equipment_toggle_equip__weapon2weapon__msg(dagger):
    e = Equipment(dagger)
    sword = ef.sword
    result = e.toggle_equip(item=sword)
    assert result == "You remove the Dagger. You equip the Sword. "


def test_Equipment_toggle_equip__armor2armor(leather_armor):
    e = Equipment(leather_armor)
    chainmail = ef.chain_mail
    e.toggle_equip(item=chainmail)
    assert e.slots['ARMOR'] == chainmail


def test_Equipment_toggle_equip__armor2armor__msg(leather_armor):
    e = Equipment(leather_armor)
    chainmail = ef.chain_mail
    result = e.toggle_equip(item=chainmail)
    assert result == "You remove the Leather Armor. You equip the Chain Mail. "


def test_Equipment_toggle_equip__non_equippable__raisesImpossible():
    e = Equipment()
    potion = ef.health_potion
    with pytest.raises(exceptions.Impossible):
        e.toggle_equip(item=potion)
