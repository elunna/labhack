import pytest

from components.component import Component
from components.light import LightComponent
from src.entity import Entity


@pytest.fixture
def test_entity():
    return Entity(x=1, y=1)


def test_init__is_Component():
    lc = LightComponent()
    assert isinstance(lc, Component)


def test_init__radius_default_1():
    lc = LightComponent()
    assert lc.radius == 1


def test_init__radius_arg():
    lc = LightComponent(radius=5)
    assert lc.radius == 5


def test_init__area(test_entity):
    lc = LightComponent(radius=1)
    test_entity.add_comp(light=lc)
    assert lc.area() == {
        (0, 0), (1, 0), (2, 0),
        (0, 1), (1, 1), (2, 1),
        (0, 2), (1, 2), (2, 2)
    }
