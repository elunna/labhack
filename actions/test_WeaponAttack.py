from .attack_actions import WeaponAttack
from src import factory
from tests import toolkit
import pytest


@pytest.fixture
def test_map():
    return toolkit.test_map()


@pytest.fixture
def player():
    m = toolkit.test_map()
    player = m.player
    dagger = player.inventory.items.get('a')
    assert player.equipment.toggle_equip(dagger)
    return player


def test_hit_msg__you_hit_enemy(player):
    a = WeaponAttack(entity=player, dx=-1, dy=-1)
    target = factory.make("orc")
    # TODO: Add reference to attacks in AttackActions? Cross link with it's weapon?
    atk = player.equipment.slots['WEAPON'].equippable.attack_comp.attacks[0]
    dmg = 10
    a.hit_msg(target, atk, dmg)
    assert a.msg == f"You hit the Orc with your dagger for {dmg}! "


def test_hit_msg__enemy_hits_you(player):
    # Arm the orc with a dagger
    orc = factory.make("orc")
    dagger = factory.make('dagger')
    orc.inventory.add_item(dagger)
    orc.equipment.toggle_equip(dagger)

    a = WeaponAttack(entity=orc, dx=-1, dy=-1)
    atk = dagger.equippable.attack_comp.attacks[0]
    dmg = 10
    a.hit_msg(player, atk, dmg)
    assert a.msg == f"The Orc hits you with it's dagger for {dmg}! "


def test_hit_msg__enemy_hits_enemy():
    # Arm the orc with a dagger
    orc = factory.make("orc")
    dagger = factory.make('dagger')
    orc.inventory.add_item(dagger)
    orc.equipment.toggle_equip(dagger)

    a = WeaponAttack(entity=orc, dx=-1, dy=-1)
    atk = dagger.equippable.attack_comp.attacks[0]
    dmg = 10
    a.hit_msg(orc, atk, dmg)
    assert a.msg == f"The Orc hits the Orc with it's dagger for {dmg}! "
