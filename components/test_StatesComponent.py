from components.component import Component
from components.states import StatesComponent


def test_init__is_Component():
    s = StatesComponent()
    assert isinstance(s, Component)


def test_init__states_dict():
    s = StatesComponent()
    assert s.states == {}


def test_add_state__new_state():
    s = StatesComponent()
    s.add_state("confused", 10)
    assert s.states["confused"] == 10


def test_add_state__existing_state():
    s = StatesComponent()
    s.add_state("confused", 10)
    s.add_state("confused", 10)
    assert s.states["confused"] == 20


def test_decrease():
    s = StatesComponent()
    s.add_state("confused", 10)
    s.decrease()
    assert s.states["confused"] == 9


def test_decrease__eliminate_state():
    s = StatesComponent()
    s.add_state("confused", 2)
    s.decrease()
    s.decrease()
    assert "confused" not in s.states
