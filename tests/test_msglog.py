""" Tests for msg_log.py """
import msg_log

test_text = 'This is a test'


def test_Message():
    m = msg_log.Message(test_text)
    assert m.plain_text == test_text


def test_Message_count():
    m = msg_log.Message(test_text)
    assert m.count == 1


def test_Message_fulltext():
    m = msg_log.Message(test_text)
    assert m.full_text == test_text


def test_Message_fulltext_count2():
    m = msg_log.Message(test_text)
    m.count = 2
    assert m.full_text == f'{test_text} (x2)'


def test_MessageLog():
    ml = msg_log.MessageLog()
    assert ml.messages == []


def test_MessageLog__add_message():
    ml = msg_log.MessageLog()
    ml.add_message(test_text)
    assert len(ml.messages) == 1


def test_MessageLog__add_message_same():
    ml = msg_log.MessageLog()
    ml.add_message(test_text)
    ml.add_message(test_text)
    assert len(ml.messages) == 1  # Only one message with count of 2
    assert ml.messages[0].full_text == f'{test_text} (x2)'


def test_MessageLog__wrap():
    ml = msg_log.MessageLog()
    result = ml.wrap(test_text, 4)

    # We get a generator, so have to convert to list first.
    assert list(result) == [
        'This', 'is a', 'test'
    ]
