""" Tests for component.py """

from components.component import Component


# Tests for BaseComponent
def test_Component__init():
    c = Component()
    assert c.parent is None


def test_Component__gamemap__no_parent():
    c = Component()
    assert c.gamemap is None


def test_Component__engine__no_parent():
    c = Component()
    assert c.engine is None
