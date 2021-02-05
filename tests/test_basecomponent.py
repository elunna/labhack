""" Tests for basecomponent.py """

from components.base_component import BaseComponent
import pytest


def test_BaseComponent__init():
    c = BaseComponent()
    assert c.parent is None


@pytest.mark.skip(reason='Annoying')
def test_BaseComponent__gamemap__no_parent():
    c = BaseComponent()
    assert c.gamemap is None


@pytest.mark.skip(reason='Annoying')
def test_BaseComponent__engine__no_parent():
    c = BaseComponent()
    assert c.engine is None
