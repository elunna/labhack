from components.stackable import StackableComponent
from pytest_mock import mocker
from src.entity import Entity
from src.entity_manager import EntityManager, NO_LIMIT
import pytest


@pytest.fixture
def em():
    return EntityManager()


def test_init__entities_list(em):
    assert em.entities == set()


def test_init__required_components_default_is_None(em):
    assert em.required_comp is None


def test_init__required_components():
    em = EntityManager(required_comp="item")
    assert em.required_comp == "item"


def test_init__capacity():
    em = EntityManager(capacity=1)
    assert em.capacity == 1


def test_init__default_capacity_is_NO_LIMIT():
    em = EntityManager()
    assert em.capacity == NO_LIMIT


def test_len(em):
    assert len(em) == 0
    em.add_entity(Entity(name="fleeb"))
    assert len(em) == 1


def test_add_entity__Entity__returns_True(em):
    e = Entity(name="fleeb")
    assert em.add_entity(e)


def test_add_entity__Entity__in_entities(em):
    e = Entity(name="fleeb")
    em.add_entity(e)
    assert e in em.entities


def test_add_entity__dupe_Entity__returns_False(em):
    e = Entity(name="fleeb")
    assert em.add_entity(e)
    assert em.add_entity(e) is False


def test_init__add_entity_when_full_returns_False():
    em = EntityManager(capacity=1)
    em.add_entity(Entity(name="fleeb"))
    assert em.add_entity(Entity(name="floop")) is False


def test_add_entity__e_has_required_component():
    em = EntityManager(required_comp="item")
    e = Entity(name="fleeb", item="item")
    assert em.add_entity(e)


def test_add_entity__e_missing_required_component__raise_ValueError():
    em = EntityManager(required_comp="item")
    with pytest.raises(ValueError):
        em.add_entity(Entity(name="fleeb"))


def test_add_entity__updates_entity_parent(em):
    e = Entity(name="fleeb")
    em.add_entity(e)
    assert e.parent == em


def test_add_entity__stackable__calls_add_stackable(em, mocker):
    mocker.patch('src.entity_manager.EntityManager.add_stackable')
    e = Entity(name="fleeb", stackable=StackableComponent(1))
    em.add_entity(e)
    em.add_stackable.assert_called_once()


def test_add_entity__stackable__no_twin__adds_like_normal(em):
    e = Entity(name="fleeb", stackable=StackableComponent(1))
    assert em.add_entity(e)
    assert e in em.entities
    assert e.parent == em


def test_add_entities__single(em):
    e = Entity(name="fleeb")
    em.add_entities(e)
    assert e in em.entities


def test_add_entities__iterable(em):
    e = Entity(name="fleeb")
    f = Entity(name="fleeb2", x=0)
    list_of_entities = [e, f]
    em.add_entities(*list_of_entities)
    assert e in em.entities
    assert f in em.entities


def test_add_entities__multiple_args(em):
    e = Entity(name="fleeb")
    f = Entity(name="fleeb2", x=0)
    em.add_entities(e, f)  # as *args
    assert e in em.entities
    assert f in em.entities


def test_add_stackable__has_twin__returns_True(em):
    e = Entity(name="fleeb", stackable=StackableComponent(5))
    f = Entity(name="fleeb", stackable=StackableComponent(1))
    assert em.add_entity(e)  # as *args
    assert em.add_stackable(f)


def test_add_stackable__has_twin__merged_into_twin(em):
    e = Entity(name="fleeb", stackable=StackableComponent(5))
    f = Entity(name="fleeb", stackable=StackableComponent(1))
    assert em.add_entity(e)  # as *args
    assert em.add_stackable(f)
    assert e.stackable.size == 6


def test_add_stackable__has_twin__source_is_depleted(em):
    e = Entity(name="fleeb", stackable=StackableComponent(5))
    f = Entity(name="fleeb", stackable=StackableComponent(1))
    assert em.add_entity(e)  # as *args
    assert em.add_stackable(f)
    assert f.stackable.size == 0


def test_add_stackable__no_twin__returns_False(em):
    e = Entity(name="fleeb", stackable=StackableComponent(5))
    assert em.add_stackable(e) is False


def test_rm_entity__entity_DNE_returns_None(em):
    e = Entity(name="fleeb")
    result = em.rm_entity(e)
    assert result is None


def test_rm_entity__returns_entity(em):
    e = Entity(name="fleeb")
    em.add_entity(e)
    result = em.rm_entity(e)
    assert result == e


def test_rm_entity__entity_removed_from_entities(em):
    e = Entity(name="fleeb")
    em.add_entity(e)
    em.rm_entity(e)
    assert e not in em.entities


def test_rm_entity__updates_entity_parent_to_None(em):
    e = Entity(name="fleeb")
    em.add_entity(e)
    em.rm_entity(e)
    assert e.parent is None


def test_rm_entity__stackable__calls_rm_stackable(em, mocker):
    mocker.patch('src.entity_manager.EntityManager.rm_stackable')
    e = Entity(name="fleeb", stackable=StackableComponent(1))
    em.add_entity(e)
    em.rm_entity(e)
    em.rm_stackable.assert_called_once()


def test_rm_entity__qty_gt_1_calls_rm_stackable(em, mocker):
    mocker.patch('src.entity_manager.EntityManager.rm_stackable')
    e = Entity(name="fleeb", stackable=StackableComponent(10))
    em.add_entity(e)
    em.rm_entity(e, 2)
    em.rm_stackable.assert_called_once()


def test_rm_entity__qty_gt_1_but_not_stackable__raises_ValueError(em):
    e = Entity(name="fleeb")
    em.add_entity(e)
    with pytest.raises(ValueError):
        em.rm_entity(e, 2)


def test_rm_entities__single_arg(em):
    e = Entity(name="fleeb")
    em.add_entity(e)
    em.rm_entities(e)
    assert len(em.entities) == 0


def test_rm_entities__multiple_args(em):
    e = Entity(name="fleeb")
    f = Entity(name="fleeb2", x=0)
    em.add_entities(e, f)
    em.rm_entities(e, f)
    assert len(em.entities) == 0


def test_rm_stackable__default_qty1(em):
    e = Entity(name="fleeb", stackable=StackableComponent(10))
    em.add_entity(e)
    result = em.rm_stackable(e)
    assert result.stackable.size == 1
    assert e.stackable.size == 9


def test_rm_stackable__success_returns_new_stackable(em):
    e = Entity(name="fleeb", stackable=StackableComponent(10))
    em.add_entity(e)
    result = em.rm_stackable(e, 2)
    assert result.stackable.size == 2
    assert e != result
    assert e.is_similar(result)


def test_rm_stackable__success_decreases_stacksize(em):
    e = Entity(name="fleeb", stackable=StackableComponent(10))
    em.add_entity(e)
    em.rm_stackable(e, 2)
    assert e.stackable.size == 8


def test_rm_stackable__full_stack_deletes_item(em):
    e = Entity(name="fleeb", stackable=StackableComponent(10))
    em.add_entity(e)
    em.rm_stackable(e, 10)
    assert e not in em


def test_rm_stackable__no_twin__returns_None(em):
    e = Entity(name="fleeb", stackable=StackableComponent(10))
    assert em.rm_stackable(e) is None


def test_has_entity__entity_DNE_returns_False(em):
    e = Entity(name="fleeb")
    assert em.has_entity(e) is False


def test_has_entity__contains_entity_returns_True(em):
    e = Entity(name="fleeb")
    em.add_entity(e)
    assert em.has_entity(e)


def test_contains(em):
    e = Entity(name="fleeb")
    assert e not in em
    em.add_entity(e)
    assert e in em


def test_get_by_name__DNE_returns_empty_set(em):
    assert em.get_by_name("fleeb") == set()


def test_get_by_name__single_in_set(em):
    e = Entity(name="fleeb")
    em.add_entity(e)
    assert em.get_by_name("fleeb") == {e}


def test_get_by_name__multiple_in_set(em):
    e1 = Entity(name="fleeb", x=0)
    e2 = Entity(name="fleeb", x=1)
    em.add_entities(e1, e2)
    assert em.get_by_name("fleeb") == {e1, e2}


def test_has_comp__none_matching_returns_empty_set(em):
    assert em.has_comp("name") == set()


def test_has_comp__1_matching_set(em):
    e = Entity(name="fleeb", x=0)
    em.add_entity(e)
    assert em.has_comp("name") == {e}


def test_has_comp__2_matching_set(em):
    e = Entity(name="fleeb", x=0)
    f = Entity(name="fleeb2", x=0)
    em.add_entities(e, f)
    assert em.has_comp("name") == {e, f}


def test_filter__1_kwarg_no_matching_empty_set(em):
    assert em.filter(name="fleeb") == set()


def test_filter__1_kwarg(em):
    e = Entity(name="fleeb", x=0)
    em.add_entity(e)
    assert em.filter(name="fleeb") == {e}


def test_filter__multiple_kwargs(em):
    e = Entity(name="fleeb", x=0)
    f = Entity(name="fleeb2", x=0)
    em.add_entities(e, f)
    assert em.filter(x=0, name="fleeb2") == {f}


def test_filter__1_arg(em):
    e = Entity(name="fleeb", x=0)
    f = Entity(name="fleeb2")
    em.add_entities(e, f)
    assert em.filter("x") == {e}


def test_filter__1_arg_1_kwarg(em):
    e = Entity(name="fleeb", x=0)
    f = Entity(name="fleeb2", x=1)
    em.add_entities(e, f)
    assert em.filter("name", x=0) == {e}


def test_is_empty(em):
    assert len(em) == 0
    assert em.is_empty()
    em.add_entity(Entity(name="fleeb"))
    assert not em.is_empty()


def test_is_full__set_capacity_is_full():
    em = EntityManager(capacity=1)
    em.add_entity(Entity(name="fleeb"))
    assert em.is_full()


def test_is_full__set_capacity_has_space():
    em = EntityManager(capacity=1)
    assert not em.is_full()


def test_is_full__no_capacity__never_is_full():
    em = EntityManager()
    assert not em.is_full()
    em.add_entity(Entity(name="fleeb"))
    assert not em.is_full()


def test_get_similar__has_twin_returns_entity(em):
    e1 = Entity(name="fleeb", x=0)
    e2 = Entity(name="fleeb", x=1)
    em.add_entities(e1, e2)
    assert em.get_similar(e1) == e1


def test_get_similar__no_match_returns_None(em):
    e1 = Entity(name="fleeb", x=0)
    assert em.get_similar(e1) is None
