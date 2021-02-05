""" Tests for equipment.py """

from components.base_component import BaseComponent
from components.equipment import Equipment
from src import entity_factories as ef
import pytest


@pytest.fixture
def dagger():
    return ef.dagger


@pytest.fixture
def leather_armor():
    return ef.leather_armor


def test_Equipment_is_BaseComponent():
    e = Equipment()
    assert isinstance(e, BaseComponent)


def test_Equipment_init():
    e = Equipment()
    assert e.weapon is None
    assert e.armor is None

# TODO: Make sure init uses the equip function - we can't equip armor to weapon
# slot, etc...


def test_Equipment_init__with_weapon(dagger):
    e = Equipment(weapon=dagger)
    assert e.weapon == dagger
    assert e.armor is None


def test_Equipment_init__with_armor(leather_armor):
    e = Equipment(armor=leather_armor)
    assert e.weapon is None
    assert e.armor is leather_armor


def test_Equipment_defense_bonus__default_is_0():
    e = Equipment()
    assert e.defense_bonus == 0


def test_Equipment_defense_bonus__with_armor(leather_armor):
    e = Equipment(armor=leather_armor)
    assert e.defense_bonus == leather_armor.equippable.defense_bonus


def test_Equipment_power_bonus__default_is_0():
    e = Equipment()
    assert e.power_bonus == 0


def test_Equipment_power_bonus__with_weapon(dagger):
    e = Equipment(weapon=dagger)
    assert e.power_bonus == dagger.equippable.power_bonus


def test_Equipment_item_is_equipped__none_equipped():
    e = Equipment()
    assert e.item_is_equipped('giant jockstrap') is False


def test_Equipment_item_is_equipped__weapon_equipped(dagger):
    e = Equipment(weapon=dagger)
    assert e.item_is_equipped(dagger)


def test_Equipment_item_is_equipped__armor_equipped(leather_armor):
    e = Equipment(armor=leather_armor)
    assert e.item_is_equipped(leather_armor)


@pytest.mark.skip(reason='Refers to self.parent.gamemap.engine')
def test_Equipment_unequip_message():
    e = Equipment(armor=leather_armor)
    result = e.unequip_message('leather armor')


@pytest.mark.skip(reason='Refers to self.parent.gamemap.engine')
def test_Equipment_equip_message(dagger):
    e = Equipment()
    result = e.equip_message('dagger')


def test_Equipment_equip_to_slot__weapon_to_weaponslot(dagger):
    e = Equipment()
    result = e.equip_to_slot(slot="weapon", item=dagger, add_message=False)
    assert e.weapon == dagger
    # assert result


def test_Equipment_equip_to_slot__armor_to_armorslot(leather_armor):
    e = Equipment()
    result = e.equip_to_slot(slot="armor", item=leather_armor, add_message=False)
    assert e.armor == leather_armor
    # assert result


@pytest.mark.skip(reason='Needs to check the equipment')
def test_Equipment_equip_to_slot__weapon_to_armorslot(dagger):
    # We should not be able to put weapon in an armor slot.
    e = Equipment()
    result = e.equip_to_slot(slot="armor", item=dagger, add_message=False)
    assert e.armor is None
    assert result is False


@pytest.mark.skip(reason='Needs to check the equipment')
def test_Equipment_equip_to_slot__armor_to_weaponslot(leather_armor):
    # We should not be able to put armor in an weapon slot.
    e = Equipment()
    result = e.equip_to_slot(slot="weapon", item=leather_armor, add_message=False)
    assert e.weapon is None
    assert result is False


@pytest.mark.skip(reason='Tries to refer to item.equippable when it does not have it')
def test_Equipment_equip_to_slot__non_equippable():
    # Item has to be equippable
    potion = ef.health_potion
    e = Equipment()
    result = e.equip_to_slot(slot="weapon", item=potion, add_message=False)
    assert e.weapon is None
    assert result is False


def test_Equipment_unequip_from_slot__weapon(dagger):
    e = Equipment(weapon=dagger)
    result = e.unequip_from_slot(slot="weapon", add_message=False)
    # assert result
    assert e.weapon is None


def test_Equipment_unequip_from_slot__armor(leather_armor):
    e = Equipment(armor=leather_armor)
    result = e.unequip_from_slot(slot="armor", add_message=False)
    # assert result
    assert e.armor is None


@pytest.mark.skip(reason='Needs to return a bool')
def test_Equipment_unequip_from_slot__fail_returns_False():
    e = Equipment()
    result = e.unequip_from_slot(slot="armor", add_message=False)
    assert result is False


def test_Equipment_toggle_equip__none2weapon(dagger):
    e = Equipment()
    result = e.toggle_equip(dagger, False)
    # assert result
    assert e.weapon == dagger


def test_Equipment_toggle_equip__none2armor(leather_armor):
    e = Equipment()
    result = e.toggle_equip(leather_armor, False)
    # assert result
    assert e.armor == leather_armor


def test_Equipment_toggle_equip__weapon2none(dagger):
    e = Equipment(weapon=dagger)
    result = e.toggle_equip(dagger, False)
    # assert result
    assert e.weapon is None


def test_Equipment_toggle_equip__armor2none(leather_armor):
    e = Equipment(armor=leather_armor)
    result = e.toggle_equip(leather_armor, False)
    # assert result
    assert e.armor is None


def test_Equipment_toggle_equip__weapon2weapon(dagger):
    e = Equipment(weapon=dagger)
    sword = ef.sword
    result = e.toggle_equip(sword, False)
    # assert result
    assert e.weapon == sword


def test_Equipment_toggle_equip__armor2armor(leather_armor):
    e = Equipment(armor=leather_armor)
    chainmail = ef.chain_mail
    result = e.toggle_equip(chainmail, False)
    # assert result
    assert e.armor == chainmail


@pytest.mark.skip(reason='Needs to return a bool')
def test_Equipment_toggle_equip__non_equippable__returns_False():
    e = Equipment()
    potion = ef.health_potion
    result = e.toggle_equip(potion, False)
    assert result is False


@pytest.mark.skip(reason='Needs to check the equipment')
def test_Equipment_toggle_equip__non_equippable():
    e = Equipment()
    potion = ef.health_potion
    result = e.toggle_equip(potion, False)
    assert e.armor is None
    assert e.weapon is None
