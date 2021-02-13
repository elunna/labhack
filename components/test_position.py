from .component import Component
from .position import PositionComponent


def test_PositionComponent_is_Component():
    pc = PositionComponent(x=1, y=2)
    assert isinstance(pc, Component)


def test_PositionComponent_init():
    pc = PositionComponent(x=1, y=2)
    assert pc.x == 1
    assert pc.y == 2

