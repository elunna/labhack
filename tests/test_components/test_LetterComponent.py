import pytest

from components.component import Component
from components.letter import LetterComponent


def test_init__is_Component():
    lc = LetterComponent('a')
    assert isinstance(lc, Component)


def test_init__letter_arg():
    lc = LetterComponent('a')
    assert lc.letter == "a"


def test_init__invalid_letter():
    with pytest.raises(ValueError):
        lc = LetterComponent('?')
