from components.component import Component
from components.regeneration import Regeneration


def test_init__is_Component():
    r = Regeneration()
    assert isinstance(r, Component)


def test_init__x_turns__level_1():
    # regenerate one hit point every (42 / (level + 2)) + 1 turns
    # level 1: (42 / (1 + 2)) + 1 == (42 / 3) + 1 == 15

    r = Regeneration()
    assert r.x_turns(1) == 15


def test_init__x_turns__level_2():
    # regenerate one hit point every (42 / (level + 2)) + 1 turns
    # level 1: (42 / (2 + 2)) + 1 == (42 / 4) + 1 == 11.5 == 11

    r = Regeneration()
    assert r.x_turns(2) == 11


def test_init__x_turns__level_10():
    # Above level 10, regenerate every 3rd turn
    r = Regeneration()
    assert r.x_turns(10) == 3


def test_init__x_turns__level_30():
    # Above level 10, regenerate every 3rd turn
    r = Regeneration()
    assert r.x_turns(30) == 3


def test_eligible_for_regen__lev1():
    r = Regeneration()
    # Level 1, every 15 turns we regen. 15 % 15 == 0
    assert not r.eligible_for_regen(level=1, turns=1)
    assert r.eligible_for_regen(level=1, turns=15)
    assert r.eligible_for_regen(level=1, turns=30)


def test_eligible_for_regen__lev10():
    r = Regeneration()
    # Level 10, every 10 turns we regen.
    assert r.eligible_for_regen(level=10, turns=0)
    assert not r.eligible_for_regen(level=10, turns=1)
    assert r.eligible_for_regen(level=10, turns=3)
    assert r.eligible_for_regen(level=10, turns=6)


def test_regen_amt__level_less_than_10__1HP():
    r = Regeneration()
    assert r.regen_amt(con=12, level=1) == 1
    assert r.regen_amt(con=18, level=2) == 1


def test_regen_amt__lev10_con12():
    r = Regeneration()
    # Since the max is our level - 9, that leaves only 1.
    assert r.regen_amt(con=12, level=10) == 1


def test_regen_amt__lev11_con12():
    r = Regeneration()
    result = r.regen_amt(con=12, level=11)
    assert 1 <= result <= 2


def test_regen_amt__lev12_con12():
    r = Regeneration()
    result = r.regen_amt(con=12, level=11)
    assert 1 <= result <= 3
