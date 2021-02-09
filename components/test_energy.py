""" Tests for energy.py """

from .component import Component
from .energy import EnergyMeter


def test_EnergyMeter_is_Component():
    em = EnergyMeter(threshold=10)
    assert isinstance(em, Component)


def test_EnergyMeter_init__default():
    em = EnergyMeter()
    DEFAULT_THRESHOLD = 10
    assert em.threshold == DEFAULT_THRESHOLD
    assert em.energy == 0


def test_EnergyMeter_init():
    em = EnergyMeter(threshold=10)
    assert em.threshold == 10
    assert em.energy == 0


def test_EnergyMeter_add_energy():
    em = EnergyMeter(threshold=10)
    em.add_energy(10)
    assert em.energy == 10


def test_EnergyMeter_burn_turn__unsuccessful_returns_False():
    em = EnergyMeter(threshold=10)
    assert em.burn_turn() is False


def test_EnergyMeter_burned_out__success_returns_True():
    em = EnergyMeter(threshold=10)
    em.add_energy(10)
    assert em.burn_turn() is True


def test_EnergyMeter_burned_out__success_uses_energy():
    em = EnergyMeter(threshold=10)
    em.add_energy(10)
    em.burn_turn()
    assert em.energy == 0
