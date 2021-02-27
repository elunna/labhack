""" Tests for energy.py """

from .component import Component
from .energy import EnergyComponent
from src.settings import DEFAULT_THRESHOLD
import pytest


def test_init__is_Component():
    em = EnergyComponent(threshold=10)
    assert isinstance(em, Component)


def test_init__default_threshold():
    em = EnergyComponent()
    assert em.threshold == DEFAULT_THRESHOLD


def test_init__energy_is_random():
    em = EnergyComponent()
    assert em.energy >= 0
    assert em.energy <= DEFAULT_THRESHOLD


def test_init__set_threshold():
    THRESHOLD = 20
    em = EnergyComponent(threshold=THRESHOLD)
    assert em.threshold == THRESHOLD
    assert em.energy >= 0 and em.energy <= THRESHOLD


def test_init__0_threshold__raises_ValueError():
    with pytest.raises(ValueError):
        EnergyComponent(threshold=0)


def test_add_energy():
    em = EnergyComponent(threshold=10)
    expected = em.energy + 10

    em.add_energy(10)
    assert em.energy == expected


def test_burn_turn__unsuccessful_returns_False():
    em = EnergyComponent(threshold=10)
    em.energy = 0  # Make sure this is 0 to force fail
    assert em.burn_turn() is False


def test_burn_turn__success_returns_True():
    em = EnergyComponent(threshold=10)
    em.add_energy(10)
    assert em.burn_turn() is True


def test_burned_out__success_uses_energy():
    em = EnergyComponent(threshold=10)
    em.energy = 10  # Force set this for testing
    em.burn_turn()
    assert em.energy == 0