""" Tests for factories.py """
import factories
import pytest

item_chances = {
    # keys in the dictionary represent the floor number,
    # and the value is a list of tuples.
    # 0: [(health_potion, 35), (confusion_potion, 35)],
    0: [('a', 5), ('b', 5)],
    1: [('a', 10), ('c', 5)],
    2: [('a', 15), ('d', 5)],
}

@pytest.mark.skip(reason='Create sample tables for testing')
def test_get_max_value_for_floor():
    pass


@pytest.mark.skip(reason='Create sample tables for testing')
def test_get_entities_at_random():
    pass


