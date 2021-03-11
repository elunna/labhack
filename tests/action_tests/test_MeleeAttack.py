from actions.attack_actions import MeleeAttack
from src import factory
from tests import toolkit
import pytest


@pytest.fixture
def test_map():
    return toolkit.test_map()


def test_hit_msg__you_hit_enemy(test_map):
    player = test_map.player
    a = MeleeAttack(entity=player, dx=-1, dy=-1)
    target = factory.make("henchman")
    atk = player.offense.attacks[0]
    dmg = 10
    a.hit_msg(target, atk, dmg)
    assert a.msg == f"You punch the henchman for {dmg}! "


def test_hit_msg__enemy_hits_you(test_map):
    target = test_map.player
    henchman = factory.make("henchman")
    a = MeleeAttack(entity=henchman, dx=0, dy=1)
    atk = henchman.offense.attacks[0]
    dmg = 10
    a.hit_msg(target, atk, dmg)
    assert a.msg == f"The henchman punchs you for {dmg}! "


def test_hit_msg__enemy_hits_enemy():
    henchman = factory.make("henchman")
    a = MeleeAttack(entity=henchman, dx=0, dy=1)
    atk = henchman.offense.attacks[0]
    dmg = 10
    a.hit_msg(henchman, atk, dmg)
    assert a.msg == f"The henchman punchs the henchman for {dmg}! "
