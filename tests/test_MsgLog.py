""" Tests for msglog.py """
from src import messages

test_text = 'This is a test'

# TODO: Separate Message to own module.


def test_init__messages_list():
    ml = messages.MsgLog()
    assert ml.messages == []


def test_add_message():
    ml = messages.MsgLog()
    ml.add_message(test_text)
    assert len(ml.messages) == 1


def test_add_message_same():
    ml = messages.MsgLog()
    ml.add_message(test_text)
    ml.add_message(test_text)
    assert len(ml.messages) == 1  # Only one message with count of 2
    assert ml.messages[0].full_text == f'{test_text} (x2)'


def test_wrap():
    ml = messages.MsgLog()
    result = ml.wrap(test_text, 4)

    # We get a generator, so have to convert to list first.
    assert list(result) == [
        'This', 'is a', 'test'
    ]
