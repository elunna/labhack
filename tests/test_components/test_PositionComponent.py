from components.component import Component
from components.position import PositionComponent


def test_init__is_Component():
    pc = PositionComponent(x=1, y=2)
    assert isinstance(pc, Component)


def test_init():
    pc = PositionComponent(x=1, y=2)
    assert pc.x == 1
    assert pc.y == 2

