from .attack import Attack
from .attack_cmp import AttackComponent
from .component import Component
import pytest


@pytest.fixture
def testattacks():
    return [
        Attack('bite', [8]),
        Attack('bite', [8]),
        Attack('kick', [6, 6])
    ]


def test_init__is_Component(testattacks):
    ac = AttackComponent(*testattacks)
    assert isinstance(ac, Component)


def test_init__tuple():
    atk = Attack('bite', [8])
    ac = AttackComponent(atk)
    assert ac.attacks == (atk,)  # Single tuple


def test_init__2_attacks_tuple_():
    atk = Attack('bite', [8])
    ac = AttackComponent(atk, atk)
    assert ac.attacks == (atk, atk)


def test_len(testattacks):
    ac = AttackComponent(*testattacks)
    assert len(ac) == 3


def test_init__single_attack():
    ac = AttackComponent(Attack('bite', [8]))
    assert len(ac) == 1
    assert isinstance(ac.attacks, tuple)
