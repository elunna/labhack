from . import actions
from .actions import ActionWithDirection
from .attack_actions import AttackAction, MeleeAttack, WeaponAttack
from .bump_action import BumpAction
from .movement_action import MovementAction
from tests import toolkit
import pytest


@pytest.fixture
def test_map():
    return toolkit.test_map()


def test_is_Action(test_map):
    player = test_map.player
    a = BumpAction(entity=player, dx=1, dy=-1)
    assert isinstance(a, actions.Action)


def test_is_ActionWithDirection(test_map):
    player = test_map.player
    a = BumpAction(entity=player, dx=1, dy=-1)
    assert isinstance(a, ActionWithDirection)


def test_init(test_map):
    player = test_map.player
    a = BumpAction(entity=player, dx=1, dy=-1)
    assert a.entity == player
    assert a.dx == 1
    assert a.dy == -1
    assert a.msg == ''


def test_perform__Move(test_map):
    player = test_map.player
    a = BumpAction(entity=player, dx=1, dy=1)
    result = a.perform()
    assert isinstance(result, MovementAction)


def test_perform__attack_with_weapon(test_map):
    # We'll attack the Grid Bug at (2, 5)
    player = test_map.player
    dagger = player.inventory.item_dict['a']
    player.equipment.toggle_equip(dagger)
    weapon = player.equipment.slots['WEAPON']
    assert weapon

    player.x, player.y = 2, 4
    a = BumpAction(entity=player, dx=0, dy=1)
    result = a.perform()
    assert isinstance(result, WeaponAttack)


def test_perform__attack_without_weapon(test_map):
    # We'll attack the Grid Bug at (2, 5)
    player = test_map.player
    assert player.equipment.slots['WEAPON'] is None

    player.x, player.y = 2, 4
    a = BumpAction(entity=player, dx=0, dy=1)
    result = a.perform()
    assert isinstance(result, MeleeAttack)
