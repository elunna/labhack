import pytest

from components import consumable
from components.component import Component


def test_HealingConsumable__is_Component():
    c = consumable.HealConsumable(amount=5)
    assert isinstance(c, Component)


def test_HealingConsumable__is_Consumable():
    c = consumable.HealConsumable(amount=5)
    assert isinstance(c, consumable.Consumable)


def test_HealingConsumable_init():
    c = consumable.HealConsumable(amount=5)
    assert c.parent is None
    assert c.amount == 5


@pytest.mark.skip(reason='Needs an ItemAction made')
def test_HealingConsumable_activate__fullhealth_raises_Impossible(player):
    pass


@pytest.mark.skip
def test_HealingConsumable_activate__heals_and_consumes(player):
    c = consumable.HealConsumable(amount=5)
