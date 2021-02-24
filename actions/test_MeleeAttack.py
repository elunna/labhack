from .attack_actions import MeleeAttack
from src import factory
from tests import toolkit
import pytest


@pytest.fixture
def test_map():
    return toolkit.test_map()


def test_hit_msg__you_hit_enemy(test_map):
    player = test_map.player
    a = MeleeAttack(entity=player, dx=-1, dy=-1)
    target = factory.orc
    atk = player.attack_comp.attacks[0]
    dmg = 10
    a.hit_msg(target, atk, dmg)
    assert a.msg == f"You punch the Orc for {dmg}! "


def test_hit_msg__enemy_hits_you(test_map):
    target = test_map.player
    orc = factory.orc
    a = MeleeAttack(entity=orc, dx=0, dy=1)
    atk = orc.attack_comp.attacks[0]
    dmg = 10
    a.hit_msg(target, atk, dmg)
    assert a.msg == f"The Orc hits you for {dmg}! "


def test_hit_msg__enemy_hits_enemy():
    orc = factory.orc
    a = MeleeAttack(entity=orc, dx=0, dy=1)
    atk = orc.attack_comp.attacks[0]
    dmg = 10
    a.hit_msg(orc, atk, dmg)
    assert a.msg == f"The Orc hits the Orc for {dmg}! "
