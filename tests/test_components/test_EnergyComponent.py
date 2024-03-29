""" Tests for energy.py """

from components.component import Component
from components.energy import EnergyComponent
from src.settings import ENERGY_THRESHOLD
import pytest


def test_init__is_Component():
    ec = EnergyComponent(refill=12)
    assert isinstance(ec, Component)


def test_init__refill_arg():
    ec = EnergyComponent(refill=12)
    assert ec.threshold == ENERGY_THRESHOLD


def test_init__energy_is_random():
    ec = EnergyComponent(refill=12)
    assert ec.energy >= 0
    assert ec.energy <= ENERGY_THRESHOLD


def test_init__0_refill__valid_for_stationary_actors():
    ec = EnergyComponent(refill=0)
    assert ec.refill == 0


def test_init__negative_refill__raises_ValueError():
    with pytest.raises(ValueError):
        ec = EnergyComponent(refill=-1)


def test_add_energy():
    ec = EnergyComponent(refill=12)
    expected = ec.energy + 12
    ec.add_energy()
    assert ec.energy == expected


def test_burn_turn__unsuccessful_returns_False():
    ec = EnergyComponent(refill=12)
    ec.energy = 0  # Make sure this is 0 to force fail
    assert ec.burn_turn() is False


def test_burn_turn__success_returns_True():
    ec = EnergyComponent(refill=12)
    ec.add_energy()
    assert ec.burn_turn() is True


def test_burned_out__success_uses_energy():
    ec = EnergyComponent(refill=12)
    ec.energy = 12  # Force set this for testing. Minimum is 12 for a turn.
    ec.burn_turn()
    assert ec.energy == 0
