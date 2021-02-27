import pytest
from components.component import Component
from components.material import MaterialComponent


def test_init__is_Component():
    m = MaterialComponent('plastic')
    assert isinstance(m, Component)


def test_init__material():
    m = MaterialComponent('plastic')
    assert m.material == 'plastic'


# invalid material
