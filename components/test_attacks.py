import pytest

from .component import Component
from .attacks import Attack, AttackComponent


@pytest.fixture
def testattacks():
    return [
        Attack('bite', [8]),
        Attack('bite', [8]),
        Attack('kick', [6, 6])
    ]


def test_AttackComponent_is_Component(testattacks):
    ac = AttackComponent(*testattacks)
    assert isinstance(ac, Component)


def test_AttackComponent_init__tuple():
    atk = Attack('bite', [8])
    ac = AttackComponent(atk)
    assert ac.attacks == (atk,)  # Single tuple


def test_AttackComponent_init__2_attacks_tuple_():
    atk = Attack('bite', [8])
    ac = AttackComponent(atk, atk)
    assert ac.attacks == (atk, atk)


def test_AttackComponent_len(testattacks):
    ac = AttackComponent(*testattacks)
    assert len(ac) == 3


def test_AttackComponent_init__single_attack():
    ac = AttackComponent(Attack('bite', [8]))
    assert len(ac) == 1
    assert isinstance(ac.attacks, tuple)


def test_AttackComponent_init__roll_dies__1d1():
    result = AttackComponent.roll_dies([1])
    assert result == 1


def test_AttackComponent_init__roll_dies__2d1():
    result = AttackComponent.roll_dies([1, 1])
    assert result == 2


def test_AttackComponent_init__roll_dies__1d2():
    result = AttackComponent.roll_dies([2])
    assert result >= 1
    assert result <= 2
