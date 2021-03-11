""" Tests for consumable.py """

from components import consumable
from components.component import Component
from actions.item_action import ItemAction
from src import factory, player
import pytest


@pytest.fixture
def test_player():
    return player.Player()


def test_Consumable__is_Component():
    c = consumable.Consumable()
    assert isinstance(c, Component)


def test_Consumable_init():
    c = consumable.Consumable()
    assert c.parent is None


def test_Consumable_get_action(test_player):
    # This returns an ItemAction initialized with the consumer and this
    # Consumables parent.
    c = consumable.Consumable()
    vial = factory.make("healing vial")
    c.parent = vial
    result = c.get_action(consumer=test_player)

    assert isinstance(result, ItemAction)
    assert result.entity == test_player
    assert result.item == vial


def test_Consumable_activate():
    c = consumable.Consumable()
    with pytest.raises(NotImplementedError):
        c.activate('fake_action')


def test_Consumable_consume(test_player):
    vial = factory.make('healing vial')
    test_player.inventory.add_inv_item(vial)  # Add potion to test_players inv.
    vial.consumable.consume()

    # Item should be removed from inventory
    # assert test_player.inventory.rm_item(vial) is None
    assert vial not in test_player.inventory.item_dict.values()
