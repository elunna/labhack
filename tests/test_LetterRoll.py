from src.letterroll import LetterRoll


def test_init():
    lr = LetterRoll()
    assert lr.letters == 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


def test_init_index():
    lr = LetterRoll()
    assert lr.index == -1


def test_size():
    lr = LetterRoll()
    assert len(lr) == 52


def test_next_letter__1_is_a():
    lr = LetterRoll()
    assert lr.next_letter() == 'a'


def test_next_letter__2_is_a():
    lr = LetterRoll()
    lr.next_letter()
    assert lr.next_letter() == 'b'


def test_next_letter__roll_repeats():
    lr = LetterRoll()
    roll = ''.join([lr.next_letter() for _ in range(53)])
    assert roll[-4:] == 'XYZa'
