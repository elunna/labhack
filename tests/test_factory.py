from src import factory
import pytest
from components.level import Level
from src.entity import Entity

actor_dict = {
    "player": {"level": Level(level_up_base=20, difficulty=0)},
    "grid bug": {"level": Level(xp_given=1, difficulty=1)},
    "storm drone": {"level": Level(current_level=4, xp_given=55, difficulty=20)},
}


def test_EntityFactory_creates_dict_of_actors():
    ef = factory.EntityFactory(actor_dict)
    assert isinstance(ef.entities["grid bug"], Entity)
    assert isinstance(ef.entities["storm drone"], Entity)


def test_EntityFactory_no_player_included():
    ef = factory.EntityFactory(actor_dict)
    assert "player" not in ef.entities


def test_difficulty_specific_monster__xp1_dlevel1():
    ef = factory.EntityFactory(actor_dict)
    result = ef.difficulty_specific_monster(1, 1)
    assert result == "grid bug"


max_foos_by_floor = [
    (0, 1), (2, 2), (3, 3), (5, 5)
]


def test_get_max_value_for_floor__negative():
    result = factory.get_max_value_for_floor(max_foos_by_floor, -1)
    assert result == 0


def test_get_max_value_for_floor__listed_floor():
    result = factory.get_max_value_for_floor(max_foos_by_floor, 0)
    assert result == 1


def test_get_max_value_for_floor__inbetween_floor():
    result = factory.get_max_value_for_floor(max_foos_by_floor, 1)
    assert result == 1


def test_get_max_value_for_floor__higher_floor():
    result = factory.get_max_value_for_floor(max_foos_by_floor, 1000)
    assert result == 5


weighted_chances = {
    # keys in the dictionary represent the floor number,
    # and the value is a list of tuples.
    # 0: [(health_potion, 35), (confusion_potion, 35)],
    0: [('a', 5), ('b', 5)],
    1: [('a', 10), ('c', 5)],
    2: [('a', 15), ('d', 5)],
}


@pytest.mark.skip(reason='Create sample tables for testing')
def test_get_entities_at_random():
    pass


@pytest.mark.skip
def test_place_items():
    pass


@pytest.mark.skip
def test_place_monsters():
    pass


@pytest.mark.skip
def test_populate_map__calls_place_monsters():
    pass


@pytest.mark.skip
def test_populate_map__calls_place_items():
    pass