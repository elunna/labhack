from components.attack import Attack


def test_min_dmg__1_die():
    atk = Attack('bite', [2])
    result = atk.min_dmg()
    assert result == 1


def test_min_dmg__2_die():
    atk = Attack('bite', [2, 2])
    result = atk.min_dmg()
    assert result == 2


def test_max_dmg__1_die():
    atk = Attack('bite', [2])
    result = atk.max_dmg()
    assert result == 2


def test_max_dmg__2_die():
    atk = Attack('bite', [2, 2])
    result = atk.max_dmg()
    assert result == 4


def test_init__roll_dies__1d1():
    atk = Attack('bite', [1])
    result = atk.roll_dies()
    assert result == 1


def test_init__roll_dies__2d1():
    atk = Attack('bite', [1, 1])
    result = atk.roll_dies()
    assert result == 2


def test_init__roll_dies__1d2():
    atk = Attack('bite', [2])
    result = atk.roll_dies()
    assert result >= 1
    assert result <= 2


def test_to_text__1d2():
    atk = Attack('bite', [2])
    assert atk.to_text() == '1d2'


def test_to_text__2d4():
    atk = Attack('bite', [4, 4])
    assert atk.to_text() == '2d4'


def test_to_text__1d2_1d10_1d8():
    atk = Attack('bite', [2, 10, 8])
    assert atk.to_text() == '1d2+1d8+1d10'


def test_to_text__1d2_3d10_2d8():
    atk = Attack('bite', [2, 10, 10, 10, 8, 8])
    assert atk.to_text() == '1d2+2d8+3d10'


def test_to_text__1d8_plus_2d6():
    atk = Attack('bite', [8, 6, 6])
    assert atk.to_text() == '2d6+1d8'
