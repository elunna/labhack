from .attack_actions import WeaponAttack
from src import factory
from tests import toolkit
import pytest


@pytest.fixture
def test_map():
    return toolkit.test_map()


def test_hit_with_weapon__msg__you_hit(test_map):
    player = test_map.player
    dagger = player.inventory.items.get('a')
    assert player.equipment.toggle_equip(dagger)

    a = WeaponAttack(entity=player, dx=-1, dy=-1)
    target = factory.orc
    atk = player.equipment.slots['WEAPON'].equippable.attack_comp.attacks[0]
    dmg = 10
    a.hit_msg(target, atk, dmg)
    assert a.msg == f"You hit the Orc with your dagger for {dmg}! "
