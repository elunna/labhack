from components.attack import Attack
from components.offense_comp import OffenseComponent
from components.component import Component
import pytest


@pytest.fixture
def testattacks():
    return [
        Attack('bite', [8]),
        Attack('bite', [8]),
        Attack('kick', [6, 6])
    ]


def test_init__is_Component(testattacks):
    oc = OffenseComponent(*testattacks)
    assert isinstance(oc, Component)


def test_init__tuple():
    atk = Attack('bite', [8])
    oc = OffenseComponent(atk)
    assert oc.attacks == (atk,)  # Single tuple


def test_init__2_attacks_tuple_():
    atk = Attack('bite', [8])
    oc = OffenseComponent(atk, atk)
    assert oc.attacks == (atk, atk)


def test_len(testattacks):
    oc = OffenseComponent(*testattacks)
    assert len(oc) == 3


def test_init__single_attack():
    oc = OffenseComponent(Attack('bite', [8]))
    assert len(oc) == 1
    assert isinstance(oc.attacks, tuple)
