import pytest

from components import consumable
from components.component import Component


def test_FireballDamageConsumable__is_Component():
    c = consumable.FireballDamageConsumable(damage=5, radius=3)
    assert isinstance(c, Component)


def test_FireballDamageConsumable__is_Consumable():
    c = consumable.FireballDamageConsumable(damage=5, radius=3)
    assert isinstance(c, consumable.Consumable)


def test_FireballDamageConsumable_init():
    c = consumable.FireballDamageConsumable(damage=5, radius=3)
    assert c.parent is None
    assert c.damage == 5
    assert c.radius == 3


@pytest.mark.skip(reason='Skeleton')
def test_FireballDamageConsumable_get_action():
    pass


@pytest.mark.skip(reason='Needs an ItemAction made')
def test_FireballDamageConsumable_activate():
    pass