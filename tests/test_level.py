""" Tests for level.py """

from components.level import Level
from components.component import Component
import pytest

def test_Level_init__is_BaseComponent():
    l = Level()
    assert isinstance(l, Component)


def test_Level_init__defaults():
    l = Level()
    assert l.current_level == 1
    assert l.current_xp == 0
    assert l.level_up_base == 20
    assert l.level_up_factor == 2
    assert l.xp_given == 0
    assert l.base_gain_per_level == .25


def test_Level_experience_to_next_level():
    l = Level()
    assert l.experience_to_next_level == 25


def test_Level_requires_level_up():
    l = Level()
    needed = l.experience_to_next_level
    l.add_xp(needed)
    assert l.requires_level_up


def test_Level_add_xp():
    l = Level()
    xp = 30
    l.add_xp(xp)
    assert l.current_xp == xp


@pytest.mark.skip(reason='Tweak to return a bool')
def test_Level_increase_level__not_enough_xp():
    l = Level()
    assert l.increase_level() is False


@pytest.mark.skip(reason='Tweak to return a bool')
def test_Level_increase_level__has_required_xp():
    l = Level()
    needed = l.experience_to_next_level
    l.add_xp(needed)
    assert l.increase_level()

