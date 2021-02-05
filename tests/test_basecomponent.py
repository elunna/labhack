""" Tests for basecomponent.py """

from components.component import Component
import pytest


def test_BaseComponent__init():
    c = Component()
    assert c.parent is None


@pytest.mark.skip(reason='Annoying')
def test_BaseComponent__gamemap__no_parent():
    c = Component()
    assert c.gamemap is None


@pytest.mark.skip(reason='Annoying')
def test_BaseComponent__engine__no_parent():
    c = Component()
    assert c.engine is None
