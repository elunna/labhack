""" Tests for fighter.py """

from .fighter import Fighter
from src import factory
import pytest


@pytest.fixture
def player():
    return factory.make("player")


def test_init():
    f = Fighter(hp=10)
    assert f.max_hp == 10
    assert f._hp == 10


def test_hp_property():
    f = Fighter(hp=10)
    assert f.hp == 10


def test_hp_setter__negative(player):
    f = Fighter(hp=10)
    f.parent = player  # Needs parent to check it's ai
    f.hp = -1
    assert f.hp == 0


def test_hp_setter__valid_num():
    f = Fighter(hp=10)
    f.hp = 5
    assert f.hp == 5


def test_hp_setter__over_max():
    f = Fighter(hp=10)
    f.hp = 15
    assert f.hp == 10


def test_ac_property(player):
    f = Fighter(hp=10, base_ac=15)
    f.parent = player  # Needs parent to check it's equipment
    assert f.ac == 15  # No bonus


def test_bonus__ac(player):
    f = Fighter(hp=10, base_ac=15)
    f.parent = player  # Needs parent to check it's ai
    # No bonus when player has no equipment
    assert f.ac_bonus() == 0

def test_heal__under_max():
    f = Fighter(hp=10)
    f.hp = 5
    f.heal(1)
    assert f.hp == 6


def test_heal__to_max():
    f = Fighter(hp=10)
    f.hp = 5
    f.heal(5)
    assert f.hp == 10


def test_heal__over_max():
    f = Fighter(hp=10)
    f.hp = 5
    f.heal(10000)
    assert f.hp == 10


def test_is_dead__entity_is_still_alive():
    f = Fighter(hp=10)
    assert not f.is_dead()


def test_is_dead__hes_dead_jim():
    f = Fighter(hp=10)
    f.hp = 0
    assert f.is_dead()
