from components.component import Component
from components.letter import LetterComponent


def test_init__is_Component():
    lc = LetterComponent()
    assert isinstance(lc, Component)


def test_init__default_letter_is_None():
    lc = LetterComponent()
    assert lc.letter is None


def test_init__letter_arg():
    lc = LetterComponent('a')
    assert lc.letter == "a"