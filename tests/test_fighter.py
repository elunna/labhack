""" Tests for fighter.py """
from components.fighter import Fighter
from pytest_mock import mocker
from src import entity_factories
import copy
import pytest


@pytest.fixture
def player():
    return copy.deepcopy(entity_factories.player)


def test_Fighter__init():
    f = Fighter(hp=10, base_ac=15, base_pow=20)
    assert f.max_hp == 10
    assert f._hp == 10
    assert f.base_ac == 15
    assert f.base_pow == 20


def test_Fighter_hp_property():
    f = Fighter(hp=10, base_ac=15, base_pow=20)
    assert f.hp == 10


@pytest.mark.skip(reason='die References engine')
def test_Fighter_hp_setter__negative(player):
    f = Fighter(hp=10, base_ac=15, base_pow=20)
    f.parent = player  # Needs parent to check it's ai
    f.hp = -1
    assert f.hp == 0


@pytest.mark.skip(reason='die References engine')
def test_Fighter_hp_setter__negative__dies(player, mocker):
    f = Fighter(hp=10, base_ac=15, base_pow=20)
    f.parent = player  # Needs parent to check it's ai
    mocker.patch(f.die)
    f.hp = -1
    f.die.assert_called_once()


def test_Fighter_hp_setter__valid_num():
    f = Fighter(hp=10, base_ac=15, base_pow=20)
    f.hp = 5
    assert f.hp == 5


def test_Fighter_hp_setter__over_max():
    f = Fighter(hp=10, base_ac=15, base_pow=20)
    f.hp = 15
    assert f.hp == 10


def test_Fighter_defense_property(player):
    f = Fighter(hp=10, base_ac=15, base_pow=20)
    f.parent = player  # Needs parent to check it's equipment
    # No bonus
    assert f.ac == 15


def test_Fighter_power_property(player):
    f = Fighter(hp=10, base_ac=15, base_pow=20)
    f.parent = player  # Needs parent to check it's equipment
    # No bonus
    assert f.pow == 20


def test_Fighter_defense_bonus_property(player):
    f = Fighter(hp=10, base_ac=15, base_pow=20)
    f.parent = player  # Needs parent to check it's ai
    # No bonus when player has no equipment
    assert f.ac_bonus == 0


def test_Fighter_power_bonus_property(player):
    f = Fighter(hp=10, base_ac=15, base_pow=20)
    f.parent = player  # Needs parent to check it's ai
    # No bonus when player has no equipment
    assert f.pow_bonus == 0


def test_Fighter_heal__under_max():
    f = Fighter(hp=10, base_ac=15, base_pow=20)
    f.hp = 5
    f.heal(1)
    assert f.hp == 6


def test_Fighter_heal__to_max():
    f = Fighter(hp=10, base_ac=15, base_pow=20)
    f.hp = 5
    f.heal(5)
    assert f.hp == 10


def test_Fighter_heal__over_max():
    f = Fighter(hp=10, base_ac=15, base_pow=20)
    f.hp = 5
    f.heal(10000)
    assert f.hp == 10


def test_Fighter_take_damage__non_lethal():
    f = Fighter(hp=10, base_ac=15, base_pow=20)
    f.take_damage(2)
    assert f.hp == 8


@pytest.mark.skip(reason='die References engine')
def test_Fighter_take_damage__lethal(player):
    f = Fighter(hp=10, base_ac=15, base_pow=20)
    f.parent = player  # Needs parent to check it's equipment
    f.take_damage(1000)
    assert f.hp < 0


@pytest.mark.skip(reason='die References engine')
def test_Fighter_die():
    f = Fighter(hp=10, base_ac=15, base_pow=20)
    f.parent = player  # Needs parent to check it's equipment
    f.die()
