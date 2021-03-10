import pytest

from components.component import Component
from components.inventory import PlayerInventory
from components.letter import LetterComponent
from src import factory, exceptions
from src.entity_manager import EntityManager


@pytest.fixture
def plunger():
    return factory.make('plunger')


@pytest.fixture
def dagger():
    return factory.make('dagger')


@pytest.fixture
def vials5():
    vials = factory.make('healing vial')
    vials.stackable.size = 5
    return vials


@pytest.fixture
def money():
    cash = factory.make('money')
    cash.stackable.size = 10
    return cash


def test_init__is_Component():
    pi = PlayerInventory(10)
    assert isinstance(pi, Component)


def test_init__is_EntityManager():
    pi = PlayerInventory(10)
    assert isinstance(pi, EntityManager)


def test_init__requires_item_components():
    pi = PlayerInventory(10)
    assert pi.required_comp == "item"


def test_init__capacity():
    pi = PlayerInventory(10)
    assert pi.capacity == 10


def test_init__first_inv_letter_is_a():
    pi = PlayerInventory(10)
    assert pi.current_letter == 'a'


def test_add_inv_item__adding_money_uses_dollar_sign(money):
    pi = PlayerInventory(10)
    assert pi.add_inv_item(money) == "$"


def test_add_inv_item__adding_money_size_unchanged(money):
    pi = PlayerInventory(10)
    pi.add_inv_item(money)
    expected = len(pi)
    pi.add_inv_item(money)
    assert len(pi) == expected


def test_add_inv_item__adding_money_full_capacity_returns_True(money):
    pi = PlayerInventory(1)
    pi.add_inv_item(money)
    assert pi.add_inv_item(money) == "$"


def test_add_inv_item__added_to_stackable__size_unchanged(dagger):
    pi = PlayerInventory(10)
    pi.add_inv_item(dagger)
    expected = len(pi)
    pi.add_inv_item(dagger)
    assert len(pi) == expected


def test_add_inv_item__added_to_stackable__no_new_letter(dagger):
    pi = PlayerInventory(10)
    pi.add_inv_item(dagger)
    pi.add_inv_item(dagger)
    assert pi.item_dict == {"a": dagger}


def test_add_inv_item__added_to_stackable__returns_letter(dagger):
    pi = PlayerInventory(10)
    assert pi.add_inv_item(dagger) == "a"
    assert pi.add_inv_item(dagger) == "a"


def test_add_inv_item__added_to_stackable__full_capacity_returns_letter(dagger):
    pi = PlayerInventory(1)
    pi.add_inv_item(dagger)
    assert pi.add_inv_item(dagger) == "a"


def test_add_inv_item__new_slot__full_stack__size_increased(vials5):
    pi = PlayerInventory(10)
    expected = len(pi)
    assert pi.add_inv_item(vials5) == 'a'
    assert len(pi) == expected + 1


def test_add_inv_item__new_slot__full_stack__last_letter_unoccupied(vials5):
    pi = PlayerInventory(10)
    vials5.add_comp(letter=LetterComponent('z'))
    assert pi.add_inv_item(vials5) == 'z'
    assert pi.item_dict['z'] == vials5


def test_add_inv_item__new_slot__full_stack__last_letter_occupied(dagger, vials5):
    pi = PlayerInventory(10)
    vials5.add_comp(letter=LetterComponent('a'))
    pi.add_inv_item(dagger)
    pi.add_inv_item(vials5)
    assert pi.item_dict['a'] == dagger
    assert pi.item_dict['b'] == vials5  # rolls to next available letter


def test_add_inv_item__new_slot__full_stack__new_letter(vials5):
    pi = PlayerInventory(10)
    pi.add_inv_item(vials5)
    assert pi.item_dict['a'] == vials5


def test_add_inv_item__new_slot__full_stack__full_capacity_raises_Impossible(dagger, vials5):
    pi = PlayerInventory(1)
    pi.add_inv_item(dagger)
    with pytest.raises(exceptions.Impossible):
        pi.add_inv_item(vials5)


def test_add_inv_item__new_slot__partial_stack__size_increased(vials5):
    pi = PlayerInventory(10)
    expected = len(pi)
    pi.add_inv_item(vials5, 2)
    assert len(pi) == expected + 1


def test_add_inv_item__new_slot__partial_stack__last_letter_unoccupied(vials5):
    pi = PlayerInventory(10)
    vials5.add_comp(letter=LetterComponent('z'))
    pi.add_inv_item(vials5, 2)
    result = pi.item_dict['z']
    assert result.name == "healing vial"
    assert result.stackable.size == 2


def test_add_inv_item__new_slot__partial_stack__last_letter_occupied(dagger, vials5):
    pi = PlayerInventory(10)
    vials5.add_comp(letter=LetterComponent('a'))
    pi.add_inv_item(dagger)
    pi.add_inv_item(vials5, 2)
    result = pi.item_dict['b']  # rolls to next available letter
    assert result.name == "healing vial"
    assert result.stackable.size == 2


def test_add_inv_item__new_slot__partial_stack__new_letter(vials5):
    pi = PlayerInventory(10)
    pi.add_inv_item(vials5, 2)
    result = pi.item_dict['a']  # rolls to next available letter
    assert result.name == "healing vial"
    assert result.stackable.size == 2


def test_add_inv_item__new_slot__partial_stack__full_capacity_raises_Impossible(dagger, vials5):
    pi = PlayerInventory(1)
    pi.add_inv_item(dagger)
    with pytest.raises(exceptions.Impossible):
        pi.add_inv_item(vials5, 2)


def test_add_inv_item__new_slot__nonstackable__size_increased(plunger):
    pi = PlayerInventory(10)
    expected = len(pi)
    pi.add_inv_item(plunger, 2)
    assert len(pi) == expected + 1


def test_add_inv_item__new_slot__nonstackable__last_letter_unoccupied(plunger):
    pi = PlayerInventory(10)
    plunger.add_comp(letter=LetterComponent('z'))
    pi.add_inv_item(plunger)
    assert pi.item_dict['z'] == plunger


def test_add_inv_item__new_slot__nonstackable__last_letter_occupied(dagger, plunger):
    pi = PlayerInventory(10)
    plunger.add_comp(letter=LetterComponent('a'))
    pi.add_inv_item(dagger)
    pi.add_inv_item(plunger)
    assert pi.item_dict['a'] == dagger
    assert pi.item_dict['b'] == plunger  # rolls to next available letter


def test_add_inv_item__new_slot__nonstackable__new_letter(plunger):
    pi = PlayerInventory(10)
    pi.add_inv_item(plunger)
    assert pi.item_dict['a'] == plunger


def test_add_inv_item__new_slot__nonstackable__full_capacity_raises_Impossible(dagger, plunger):
    pi = PlayerInventory(1)
    pi.add_inv_item(dagger)
    with pytest.raises(exceptions.Impossible):
        pi.add_inv_item(plunger)


# def test_add_inv_item__non_entity__returns_False():
# def test_add_inv_item__non_item__returns_False():


# def test_rm_inv_item__remove_money__size_unchanged():
# def test_rm_inv_item__remove_money__returns_money_item():
# def test_rm_inv_item__remove_money__dollar_key_remains():


def test_rm_inv_item__item_dne__returns_None(dagger):
    pi = PlayerInventory(10)
    result = pi.rm_inv_item(dagger)
    assert result is None


def test_rm_inv_item__stackable__removed_full_stack__pops_letter(vials5):
    pi = PlayerInventory(10)
    pi.add_inv_item(vials5)
    pi.rm_inv_item(vials5)
    assert pi.is_empty()
    assert vials5 not in pi.entities


def test_rm_inv_item__stackable__removed_partial_stack__letter_remains(vials5):
    pi = PlayerInventory(10)
    pi.add_inv_item(vials5)
    pi.rm_inv_item(vials5, 2)
    assert not pi.is_empty()
    assert vials5 in pi.entities
    assert "a" in pi.item_dict


def test_rm_inv_item__nonstackable__pops_letter(plunger):
    pi = PlayerInventory(10)
    pi.add_inv_item(plunger)
    pi.rm_inv_item(plunger)
    assert "a" not in pi.item_dict
    assert plunger not in pi.entities


def test_find_next_letter__first_letter_is_a():
    pi = PlayerInventory(10)
    assert pi.find_next_letter() == 'a'


def test_find_next_letter__abc__next_is_d():
    pi = PlayerInventory(10)
    pi.item_dict = {'a': 1, 'b': 2, 'c': 3}
    assert pi.find_next_letter() == 'd'


def test_find_next_letter__abd__next_is_c():
    pi = PlayerInventory(10)
    pi.item_dict = {'a': 1, 'b': 2, 'd': 4}
    assert pi.find_next_letter() == 'c'


def test_rm_letter__letter_in_item_dict__returns_item(dagger):
    pi = PlayerInventory(10)
    pi.add_inv_item(dagger)
    assert pi.rm_letter('a') == dagger


def test_rm_letter__letter_not_in_item_dict__returns_False(dagger):
    pi = PlayerInventory(10)
    pi.add_inv_item(dagger)
    assert pi.rm_letter('b') is None

# def test_rm_letter__default_qty_is_0_for_full_stack():


def test_sorted_dict__one_item(dagger):
    pi = PlayerInventory(10)
    pi.add_inv_item(dagger)
    result = pi.sorted_dict()
    assert result == {'/': ['a']}


def test_sorted_dict__multiple_items():
    pi = PlayerInventory(10)
    pi.add_inv_item(factory.make("dagger"))
    pi.add_inv_item(factory.make("leather vest"))
    pi.add_inv_item(factory.make("bulletproof vest"))
    pi.add_inv_item(factory.make("healing vial"))
    result = pi.sorted_dict()
    assert result == {
        '/': ['a'],
        '[': ['b', 'c'],
        '!': ['d'],
    }
