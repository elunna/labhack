from . import actions
from . import toolkit
from .meleeaction import MeleeAction
from src import factory
from src import exceptions
import pytest


@pytest.fixture
def test_map():
    return toolkit.test_map()


def test_MeleeAction_is_Action(test_map):
    player = test_map.get_player()
    a = MeleeAction(entity=player, dx=1, dy=-1)
    assert isinstance(a, actions.Action)


def test_MeleeAction_is_ActionWithDirection(test_map):
    player = test_map.get_player()
    a = MeleeAction(entity=player, dx=1, dy=-1)
    assert isinstance(a, actions.ActionWithDirection)


def test_MeleeAction_is_ActionWithDirection(test_map):
    player = test_map.get_player()
    a = MeleeAction(entity=player, dx=1, dy=-1)
    assert a.dx == 1
    assert a.dy == -1
    assert a.entity == player


def test_MeleeAction_perform__no_target__raises_Impossible(test_map):
    player = test_map.get_player()
    a = MeleeAction(entity=player, dx=-1, dy=-1)
    with pytest.raises(exceptions.Impossible):
        a.perform()

# perform-Case: no target
# perform-Case: miss, calls miss
# perform-Case: hit w weapon, calls hit_with_weapon
# perform-Case: hit w hands, calls hit_withhands_

def test_MeleeAction_calc_target_number(test_map):
    player = test_map.get_player()
    a = MeleeAction(entity=player, dx=-1, dy=-1)

    target = factory.orc
    assert target.level.current_level == 1
    assert target.fighter.ac == 7

    result = a.calc_target_number(target)
    expected = 10 + target.fighter.ac + target.level.current_level
    assert result == expected


def test_MeleeAction_roll_hit_die(test_map):
    player = test_map.get_player()
    a = MeleeAction(entity=player, dx=-1, dy=-1)
    result = a.roll_hit_die()
    # Just testing that the random number is between 1 and the sides (usually
    # 20)
    assert result >= 1
    assert result <= a.die


def test_MeleeAction_hit_with_weapon__returns_dmg(test_map):
    player = test_map.get_player()
    dagger = player.inventory.items.get('a')
    assert player.equipment.toggle_equip(dagger)

    a = MeleeAction(entity=player, dx=-1, dy=-1)
    target = factory.orc
    result = a.hit_with_weapon(target)
    attack_max = player.equipment.weapon.equippable.attack.die_sides
    assert result >= 1
    assert result <= attack_max


def test_MeleeAction_hit_with_weapon__msg(test_map):
    player = test_map.get_player()
    dagger = player.inventory.items.get('a')
    assert player.equipment.toggle_equip(dagger)

    a = MeleeAction(entity=player, dx=-1, dy=-1)
    target = factory.orc
    result = a.hit_with_weapon(target)
    assert a.msg == f"The Player hits the Orc with a Dagger for {result}! "


def test_MeleeAction_hit_with_barehands__returns_dmg(test_map):
    player = test_map.get_player()
    assert not player.equipment.weapon

    a = MeleeAction(entity=player, dx=-1, dy=-1)
    target = factory.orc
    result = a.hit_with_barehands(target)
    attack_max = player.fighter.attacks.die_sides
    assert result >= 1
    assert result <= attack_max


def test_MeleeAction_hit_with_barehands__msg(test_map):
    player = test_map.get_player()

    a = MeleeAction(entity=player, dx=-1, dy=-1)
    target = factory.orc
    result = a.hit_with_barehands(target)
    assert a.msg == f"The Player hits the Orc for {result}! "


def test_MeleeAction_miss(test_map):
    player = test_map.get_player()
    a = MeleeAction(entity=player, dx=-1, dy=-1)
    target = factory.orc
    result = a.miss(target)
    assert a.msg == f"The Player misses the Orc. "