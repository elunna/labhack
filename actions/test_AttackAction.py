from .actions import ActionWithDirection
from . import actions
from .attack_actions import AttackAction
from src import factory
from src import exceptions
from tests import toolkit
import pytest


@pytest.fixture
def test_map():
    return toolkit.test_map()


def test_init__is_Action(test_map):
    player = test_map.player
    a = AttackAction(entity=player, dx=1, dy=-1)
    assert isinstance(a, actions.Action)


def test_init__is_ActionWithDirection(test_map):
    player = test_map.player
    a = AttackAction(entity=player, dx=1, dy=-1)
    assert isinstance(a, ActionWithDirection)


def test_init(test_map):
    player = test_map.player
    a = AttackAction(entity=player, dx=1, dy=-1)
    assert a.dx == 1
    assert a.dy == -1
    assert a.entity == player


def test_perform__no_target__raises_Impossible(test_map):
    player = test_map.player
    a = AttackAction(entity=player, dx=-1, dy=-1)
    with pytest.raises(exceptions.Impossible):
        a.perform()


# perform-Case: miss, calls miss
# perform-Case: has weapon, calls hit_with_weapon
# perform-Case: no weapon, bare attack, calls hit_withhands

# performs all attacks in entity list (single)
# performs all attacks in entity list (double)


def test_roll_hit_die(test_map):
    player = test_map.player
    a = AttackAction(entity=player, dx=-1, dy=-1)
    result = a.roll_hit_die()
    # Just testing that the random number is between 1 and the sides (usually 20)
    assert result >= 1
    assert result <= a.die


def test_calc_target_number__positive_ac(test_map):
    player = test_map.player
    a = AttackAction(entity=player, dx=-1, dy=-1)

    target = factory.make("orc")
    assert target.attributes.ac == 7

    result = a.calc_target_number(target)
    expected = 10 + target.attributes.ac + player.level.current_level
    assert result == expected


def test_calc_target_number__negative_ac(test_map):
    player = test_map.player
    a = AttackAction(entity=player, dx=-1, dy=-1)

    target = factory.make("troll")
    assert target.attributes.ac == -2

    result = a.calc_target_number(target)
    max_expected = 10 - 1 + player.level.current_level
    min_expected = 10 + target.attributes.ac + player.level.current_level

    assert result >= min_expected
    assert result <= max_expected


def test_calc_target_number__negative_target_number(test_map):
    player = test_map.player
    a = AttackAction(entity=player, dx=-1, dy=-1)

    target = factory.make("storm drone")
    assert target.attributes.ac == -20

    result = a.calc_target_number(target)
    assert result >= 1


def test_execute_damage__with_weapon(test_map):
    player = test_map.player
    dagger = player.inventory.items.get('a')
    assert player.equipment.toggle_equip(dagger)

    a = AttackAction(entity=player, dx=-1, dy=-1)
    target = factory.make("orc")
    atk = player.equipment.slots['WEAPON'].equippable.attack_comp.attacks[0]
    result = a.execute_damage(target, atk)
    assert result >= atk.min_dmg()
    assert result <= atk.max_dmg()


def test_execute_damage__no_weapon(test_map):
    player = test_map.player
    assert not player.equipment.slots['WEAPON']

    a = AttackAction(entity=player, dx=-1, dy=-1)
    target = factory.make("orc")
    atk = player.attack_comp.attacks[0]
    result = a.execute_damage(target, atk)
    assert result >= atk.min_dmg()
    assert result <= atk.max_dmg()


def test_reduce_dmg__positive_ac_equals_no_reduction():
    orc = factory.make("orc")
    assert orc.attributes.ac == 7
    result = AttackAction.reduce_dmg(orc, 5)
    assert result == 5


def test_reduce_dmg__negative_ac():
    troll = factory.make("troll")
    assert troll.attributes.ac == -2
    result = AttackAction.reduce_dmg(troll, 5)
    assert result == 3 or result == 4


def test_reduce_dmg__ac_reduces_dmg_below_0__returns_1():
    stormdrone = factory.make("storm drone")
    assert stormdrone.attributes.ac == -20

    # Note: We'll only pass in 1 damage to test that damage can never be reduced below 1.
    # With any -AC, the defender will always try to reduce it to 0.
    result = AttackAction.reduce_dmg(stormdrone, 1)
    assert result == 1


def test_blocked_msg__player_blocks(test_map):
    target = test_map.player
    orc = factory.make("orc")
    a = AttackAction(entity=orc, dx=-1, dy=-1)
    a.blocked_msg(target)
    assert a.msg == f"You block the Orc's attack! "


def test_blocked_msg__enemy_blocks_you(test_map):
    player = test_map.player
    target = factory.make("orc")
    a = AttackAction(entity=player, dx=0, dy=1)
    a.blocked_msg(target)
    assert a.msg == f"The Orc blocks your attack! "


def test_blocked_msg__enemy_blocks_enemy():
    orc = factory.make("orc")
    a = AttackAction(entity=orc, dx=0, dy=1)
    a.blocked_msg(orc)
    assert a.msg == f"The Orc blocks the Orc's attack! "


def test_miss__player_misses(test_map):
    player = test_map.player
    a = AttackAction(entity=player, dx=-1, dy=-1)
    target = factory.make("orc")
    a.miss(target)
    assert a.msg == f"You miss the Orc. "


def test_miss__enemy_misses_you(test_map):
    target = test_map.player
    orc = factory.make("orc")
    a = AttackAction(entity=orc, dx=0, dy=1)
    a.miss(target)
    assert a.msg == f"The Orc misses you. "


def test_miss__enemy_misses_enemy(test_map):
    orc = factory.make("orc")
    a = AttackAction(entity=orc, dx=0, dy=1)
    a.miss(orc)
    assert a.msg == f"The Orc misses the Orc. "


def test_hit_msg__not_implemented(test_map):
    a = AttackAction(entity=test_map.player, dx=0, dy=1)
    orc = factory.make("orc")
    with pytest.raises(NotImplementedError):
        a.hit_msg(orc, "hit", 15)
