from components.stackable import StackableComponent
from pytest_mock import mocker
from src.entity import Entity
from src.entity_manager import EntityManager, NO_LIMIT
import pytest


@pytest.fixture
def em():
    return EntityManager()


@pytest.fixture
def fleeb3():
    return Entity(item=True, x=-1, y=-1, name="fleeb", stackable=StackableComponent(3))


@pytest.fixture
def fleeb2():
    return Entity(item=True, x=-1, y=-1, name="fleeb", stackable=StackableComponent(2))


@pytest.fixture
def floob5():
    return Entity(item=True, x=-1, y=-1, name="floob", stackable=StackableComponent(5))


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


def test_add_entity__e_missing_required_component__raise_ValueError():
    em = EntityManager(required_comp="item")
    with pytest.raises(ValueError):
        em.add_entity(Entity(name="fleeb"))


def test_add_entity__e_has_required_component():
    em = EntityManager(required_comp="item")
    e = Entity(name="fleeb", item="item")
    assert em.add_entity(e)


def test_add_entity__added__returns_True():
    em = EntityManager()
    e = Entity(name="fleeb", item="item")
    assert em.add_entity(e)


def test_add_entity__full__returns_False():
    em = EntityManager(capacity=1)
    e = Entity(name="fleeb", item="item")
    f = Entity(name="floop", item="item")
    em.add_entity(e)
    assert em.is_full()
    assert em.add_entity(f) is False


def test_add_entity__dupe_in_em__returns_False():
    em = EntityManager()
    e = Entity(name="fleeb", item="item")
    em.add_entity(e)
    assert em.add_entity(e) is False


def test_add_entity__added__updates_entity_parent(em):
    e = Entity(name="fleeb")
    em.add_entity(e)
    assert e.parent == em


@pytest.mark.skip
def test_add_entity__item_calls_add_item(em, mocker):
    e = Entity(name="fleeb")
    em.add_entity(e)
    assert e.parent == em


def test_add_item__has_required_component(fleeb3):
    em = EntityManager(required_comp="item")
    assert em.add_item(fleeb3)


def test_add_item__no_twin__added_returns_True(em, fleeb3):
    assert em.add_item(fleeb3)


def test_add_item__no_twin__e_in_entities(em, fleeb3):
    # We don't want the original stack added, we'll always create a new stack
    em.add_item(fleeb3)
    assert fleeb3 in em.entities


def test_add_item__no_twin__similar_in_entities(em, fleeb3):
    em.add_item(fleeb3)
    assert em.get_similar(fleeb3)


def test_add_item__no_twin__e_parent_updated(em, fleeb3):
    em.add_item(fleeb3)
    assert fleeb3.parent == em


def test_add_item__no_twin__default_qty_0__full_stack_source_intact(em, fleeb3):
    em.add_item(fleeb3)
    assert fleeb3.stackable.size == 3  # full stack


def test_add_item__no_twin__default_qty_0__same_stack(em, fleeb3):
    em.add_item(fleeb3)
    result = em.get_similar(fleeb3)
    assert fleeb3 is result
    assert result.stackable.size == 3
    assert fleeb3.stackable.size == 3


def test_add_item__no_twin__qty_2__source_depleted(em, fleeb3):
    em.add_item(fleeb3, 2)
    assert fleeb3.stackable.size == 1


def test_add_item__no_twin__qty_2__new_stack_created(em, floob5):
    em.add_item(floob5, 2)
    result = em.get_similar(floob5)
    assert floob5 is not result
    assert result.stackable.size == 2


def test_add_item__no_twin__qty_0_full_stack(em, fleeb3):
    em.add_item(fleeb3)
    assert fleeb3.stackable.size == 3


def test_add_item__no_twin__qty_0_fullstack_same_stack_(em, floob5):
    em.add_item(floob5)
    result = em.get_similar(floob5)
    assert floob5 is result
    assert result.stackable.size == 5
    assert floob5.stackable.size == 5


def test_add_item__twin_entities_len_does_not_change(em, fleeb2, fleeb3):
    expected = len(em) + 1
    em.add_item(fleeb3)
    em.add_item(fleeb2)  # Has a twin in the container
    assert len(em) == expected


def test_add_item__twin__returns_True(em, fleeb2, fleeb3):
    em.add_item(fleeb2)
    assert em.add_item(fleeb3)  # Has a twin in the container


def test_add_item__twin__qty_1_source_depleted(em, fleeb2, fleeb3):
    em.add_item(fleeb2, 1)
    em.add_item(fleeb3, 1)
    assert fleeb2.stackable.size == 1  # -1
    assert fleeb3.stackable.size == 2  # -1


def test_add_item__twin__qty_1_dest_added_to(em, fleeb2, fleeb3):
    em.add_item(fleeb2, 1)
    em.add_item(fleeb3, 1)
    result = em.get_similar(fleeb2)
    assert result.stackable.size == 2


def test_add_item__twin__qty_arg_source_depleted(em, fleeb2, fleeb3):
    em.add_item(fleeb2)  # Add full stack
    em.add_item(fleeb3, 2)  # Adding this one to the dest entity
    assert fleeb2.stackable.size == 4  # +2
    assert fleeb3.stackable.size == 1  # -2


def test_add_item__twin__qty_arg_dest_added_to(em, fleeb2, fleeb3):
    em.add_item(fleeb2)     # Add full stack
    em.add_item(fleeb3, 2)  # Adding this one to the dest entity
    result = em.get_similar(fleeb3)
    assert result.stackable.size == 4
    assert fleeb2.stackable.size == 4
    assert fleeb3.stackable.size == 1


def test_add_item__twin__qty_0_depletes_full_source_stack(em, fleeb2, fleeb3):
    em.add_item(fleeb2)  # Add full stack
    em.add_item(fleeb3)  # Add full stack
    assert fleeb2.stackable.size == 5
    assert fleeb3.stackable.size == 0  # Merged into fleeb2

    # TODO: fleeb3 should equal fleeb3...
    assert fleeb2 != fleeb3  # fleeb3 merged into fleeb2
    assert fleeb2 is not fleeb3  # fleeb3 merged into fleeb2


def test_add_item__twin__qty_0_adds_full_stack_to_dest(em, fleeb2, fleeb3):
    em.add_item(fleeb2, 0)  # dest
    em.add_item(fleeb3, 0)  # Add full stack to the dest entity
    result = em.get_similar(fleeb2)
    assert result.stackable.size == 5


def test_add_item__no_twin__default_full_qty(em, fleeb2):
    em.add_item(fleeb2)
    assert fleeb2.stackable.size == 2
    assert em.get_similar(fleeb2).stackable.size == 2


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


def test_rm_entity__entity_DNE_returns_None(em):
    e = Entity(name="fleeb")
    result = em.rm_entity(e)
    assert result is None


def test_rm_entity__entity_returned(em):
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


def test_rm_item__qty_lt_0_raises_ValueError(em):
    e = Entity(name="fleeb", stackable=StackableComponent(5))
    em.add_entity(e)
    with pytest.raises(ValueError):
        em.rm_item(e, -1)


def test_rm_item__non_stackable__qty_not_1_raises_ValueError(em):
    e = Entity(name="fleeb")
    em.add_entity(e)
    with pytest.raises(ValueError):
        em.rm_item(e, 2)


def test_rm_item__no_twin__returns_None(em):
    e = Entity(name="fleeb", stackable=StackableComponent(10))
    assert em.rm_item(e) is None


def test_rm_item__twin__returns_same_entity(em, fleeb3):
    em.add_entity(fleeb3)
    result = em.rm_item(fleeb3)  # Full stack
    assert result is fleeb3
    assert result == fleeb3


def test_rm_item__twin__new_stack_parent_None(em, fleeb3):
    em.add_entity(fleeb3)
    result = em.rm_item(fleeb3, 1)
    assert result.parent is None
    assert fleeb3.parent == em


def test_rm_item__twin__default_qty_0_full_stack(em, fleeb3):
    em.add_entity(fleeb3)
    result = em.rm_item(fleeb3)
    assert result.stackable.size == 3
    assert fleeb3.stackable.size == 3  # both have same reference
    assert fleeb3 not in em


def test_rm_item__has_twin__qty_1(em, fleeb2):
    em.add_entity(fleeb2)
    result = em.rm_item(fleeb2, 1)
    assert result.stackable.size == 1
    assert fleeb2.stackable.size == 1  # 1 subtracted from 2


@pytest.mark.skip(reason="Might not need this test...")
def test_rm_item__twin__qty_gt_source__raises_ValueError(em):
    e = Entity(name="fleeb", stackable=StackableComponent(10))
    em.add_entity(e)
    with pytest.raises(ValueError):
        em.rm_item(e, 11)


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
    e1 = Entity(name="fleeb", x=0, y=1)
    e2 = Entity(name="fleeb", x=0, y=1)
    em.add_entities(e1)
    assert em.get_similar(e2) == e1


def test_get_similar__no_match_returns_None(em):
    e1 = Entity(name="fleeb", x=0, y=1)
    e2 = Entity(name="fleeb", x=0, y=0)
    em.add_entities(e1)
    assert em.get_similar(e2) is None


def test_get_similar__item_coordinates_returns_entity(em):
    e1 = Entity(name="fleeb", x=-1, y=-1)
    e2 = Entity(name="fleeb", x=-1, y=-1)
    em.add_entities(e1)
    assert em.get_similar(e2) == e1
