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
