import pytest

from components import consumable
from components.component import Component


def test_ConfusionConsumable__is_Component():
    c = consumable.ConfusionConsumable(number_of_turns=5)
    assert isinstance(c, Component)


def test_ConfusionConsumable__is_Consumable():
    c = consumable.ConfusionConsumable(number_of_turns=5)
    assert isinstance(c, consumable.Consumable)


def test_ConfusionConsumable_init():
    c = consumable.ConfusionConsumable(number_of_turns=5)
    assert c.parent is None
    assert c.number_of_turns == 5


@pytest.mark.skip(reason='Skeleton')
def test_ConfusionConsumable_get_action():
    pass


@pytest.mark.skip(reason='Needs an ItemAction made')
def test_ConfusionConsumable_activate():
    pass