""" Tests for msglog.py """
from src import msglog

test_text = 'This is a test'


def test_Message():
    m = msglog.Msg(test_text)
    assert m.plain_text == test_text
    assert m.fg == (255, 255, 255) # Default white

def test_Message_count():
    m = msglog.Msg(test_text)
    assert m.count == 1


def test_Message_fulltext():
    m = msglog.Msg(test_text)
    assert m.full_text == test_text


def test_Message_fulltext_count2():
    m = msglog.Msg(test_text)
    m.count = 2
    assert m.full_text == f'{test_text} (x2)'


def test_MessageLog():
    ml = msglog.MsgLog()
    assert ml.messages == []


def test_MessageLog__add_message():
    ml = msglog.MsgLog()
    ml.add_message(test_text)
    assert len(ml.messages) == 1


def test_MessageLog__add_message_same():
    ml = msglog.MsgLog()
    ml.add_message(test_text)
    ml.add_message(test_text)
    assert len(ml.messages) == 1  # Only one message with count of 2
    assert ml.messages[0].full_text == f'{test_text} (x2)'


def test_MessageLog__wrap():
    ml = msglog.MsgLog()
    result = ml.wrap(test_text, 4)

    # We get a generator, so have to convert to list first.
    assert list(result) == [
        'This', 'is a', 'test'
    ]
