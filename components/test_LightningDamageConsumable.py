import pytest

from components import consumable
from components.component import Component


def test_LightningDamageConsumable__is_Component():
    c = consumable.LightningDamageConsumable(damage=10, maximum_range=5)
    assert isinstance(c, Component)


def test_LightningDamageConsumable__is_Consumable():
    c = consumable.LightningDamageConsumable(damage=10, maximum_range=5)
    assert isinstance(c, consumable.Consumable)


def test_LightningDamageConsumable_init():
    c = consumable.LightningDamageConsumable(damage=10, maximum_range=5)
    assert c.parent is None
    assert c.damage == 10
    assert c.maximum_range == 5


@pytest.mark.skip(reason='Needs an ItemAction made')
def test_LightningDamageConsumable_activate():
    pass