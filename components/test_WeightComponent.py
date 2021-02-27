import pytest
from components.component import Component
from components.weight import WeightComponent


def test_init__is_Component():
    w = WeightComponent(1)
    assert isinstance(w, Component)


def test_init__weight__valid_weight():
    w = WeightComponent(10)
    assert w.weight == 10


def test_init__weight__negative_weight():
    with pytest.raises(ValueError):
        w = WeightComponent(-10)


def test_init__weight__zero_weight():
    with pytest.raises(ValueError):
        w = WeightComponent(0)