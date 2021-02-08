""" Tests for consumable.py """
import pytest
import toolkit
from components import consumable
from components.component import Component
from src import factory
from src import actions


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

    assert isinstance(result, actions.ItemAction)
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
    c = consumable.HealingConsumable(amount=5)
    assert isinstance(c, Component)

@pytest.mark.skip(reason='Skeleton')
def test_HealingConsumable__is_Consumable():
    pass


@pytest.mark.skip(reason='Skeleton')
def test_HealingConsumable_init():
    pass


@pytest.mark.skip(reason='Skeleton')
def test_HealingConsumable_activate():
    pass


def test_LightningDamageConsumable__is_Component():
    c = consumable.LightningDamageConsumable(damage=10, maximum_range=5)
    assert isinstance(c, Component)

@pytest.mark.skip(reason='Skeleton')
def test_LightningDamageConsumable__is_Consumable():
    pass


@pytest.mark.skip(reason='Skeleton')
def test_LightningDamageConsumable_init():
    pass


@pytest.mark.skip(reason='Skeleton')
def test_LightningDamageConsumable_activate():
    pass


def test_ConfusionConsumable__is_Component():
    c = consumable.ConfusionConsumable(number_of_turns=5)
    assert isinstance(c, Component)


@pytest.mark.skip(reason='Skeleton')
def test_ConfusionConsumable__is_Consumable():
    pass


@pytest.mark.skip(reason='Skeleton')
def test_ConfusionConsumable_init():
    pass


@pytest.mark.skip(reason='Skeleton')
def test_ConfusionConsumable_get_action():
    pass


@pytest.mark.skip(reason='Skeleton')
def test_ConfusionConsumable_activate():
    pass


def test_FireballDamageConsumable__is_Component():
    c = consumable.FireballDamageConsumable(damage=5, radius=3)
    assert isinstance(c, Component)


@pytest.mark.skip(reason='Skeleton')
def test_FireballDamageConsumable__is_Consumable():
    pass


@pytest.mark.skip(reason='Skeleton')
def test_FireballDamageConsumable_init():
    pass


@pytest.mark.skip(reason='Skeleton')
def test_FireballDamageConsumable_get_action():
    pass


@pytest.mark.skip(reason='Skeleton')
def test_FireballDamageConsumable_activate():
    pass

