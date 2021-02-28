from enum import Enum, auto


class RenderOrder(Enum):
    TRAP = auto()
    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()