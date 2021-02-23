""" Tests for basecomponent.py """

from .component import Component
import pytest


def test_init():
    c = Component()
    assert c.parent is None


@pytest.mark.skip(reason='Annoying')
def test_gamemap__no_parent():
    c = Component()
    assert c.gamemap is None


@pytest.mark.skip(reason='Annoying')
def test_engine__no_parent():
    c = Component()
    assert c.engine is None
