""" Tests for consumable.py """

from . import consumable
from .component import Component
from actions.item_action import ItemAction
from src import factory
from tests import toolkit
import pytest


@pytest.fixture
def player():
    return toolkit.cp_player()


def test_Consumable__is_Component():
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


def test_Consumable_activate():
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