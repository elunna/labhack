""" Tests for fighter.py """

from components.fighter import Fighter
import pytest

from src import player


@pytest.fixture
def test_player():
    return player.Player()


@pytest.fixture
def test_fighter():
    return Fighter(max_hp=10, base_ac=15)


def test_init__max_hp_and_hp(test_fighter):
    assert test_fighter.max_hp == 10
    assert test_fighter._hp == 10


def test_hp_property(test_fighter):
    assert test_fighter.hp == 10


def test_hp_setter__negative(test_fighter, test_player):
    test_fighter.parent = test_player  # Needs parent to check it's ai
    test_fighter.hp = -1
    assert test_fighter.hp == 0


def test_hp_setter__valid_num(test_fighter):
    test_fighter.hp = 5
    assert test_fighter.hp == 5


def test_hp_setter__over_max(test_fighter):
    test_fighter.hp = 15
    assert test_fighter.hp == 10


def test_ac_property(test_fighter, test_player):
    test_fighter.parent = test_player  # Needs parent to check it's equipment
    assert test_fighter.ac == 15  # No bonus


def test_bonus__ac(test_fighter, test_player):
    test_fighter.parent = test_player  # Needs parent to check it's ai
    # No bonus when test_player has no equipment
    assert test_fighter.ac_bonus() == 0


def test_heal__under_max(test_fighter):
    test_fighter.hp = 5
    test_fighter.heal(1)
    assert test_fighter.hp == 6


def test_heal__to_max(test_fighter):
    test_fighter.hp = 5
    test_fighter.heal(5)
    assert test_fighter.hp == 10


def test_heal__over_max(test_fighter):
    test_fighter.hp = 5
    test_fighter.heal(10000)
    assert test_fighter.hp == 10


def test_is_dead__entity_is_still_alive(test_fighter):
    assert not test_fighter.is_dead()


def test_is_dead__hes_dead_jim(test_fighter):
    test_fighter.hp = 0
    assert test_fighter.is_dead()
