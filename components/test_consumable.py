""" Tests for consumable.py """

from . import consumable
from .component import Component
from actions import actions
from actions.useitem import ItemAction
from src import factory
from tests import toolkit
import pytest


@pytest.fixture
def player():
    return toolkit.cp_player()


def test_Consumable__is_Component(player):
    c = consumable.Consumable()
    assert isinstance(c, Component)


def test_Consumable_init():
    c = consumable.Consumable()
    assert c.parent is None


def test_Consumable_get_action(player):
    # This returns an ItemAction initialized with the consumer and this
    # Consumables parent.
    c = consumable.Consumable()
    c.parent = factory.health_potion
    result = c.get_action(consumer=player)

    assert isinstance(result, ItemAction)
    assert result.entity == player
    assert result.item == factory.health_potion


def test_Consumable_activate(player):
    c = consumable.Consumable()
    with pytest.raises(NotImplementedError):
        c.activate('fake_action')


def test_Consumable_consume(player):
    c = consumable.Consumable()
    potion = factory.make('health potion')
    c.parent = potion
    player.inventory.add_item(c.parent)  # Add potion to players inv.
    c.consume()

    # Item should be removed from inventory
    assert player.inventory.rm_item(potion) is False


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

def test_HealingConsumable_activate__heals_and_consumes(player):
    c = consumable.HealConsumable(amount=5)


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

