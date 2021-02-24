from src import messages
from tests.test_MsgLog import test_text


def test_init():
    m = messages.Msg(test_text)
    assert m.plain_text == test_text
    assert m.fg == (255, 255, 255) # Default white


def test_count():
    m = messages.Msg(test_text)
    assert m.count == 1


def test_fulltext():
    m = messages.Msg(test_text)
    assert m.full_text == test_text


def test_fulltext_count2():
    m = messages.Msg(test_text)
    m.count = 2
    assert m.full_text == f'{test_text} (x2)'
