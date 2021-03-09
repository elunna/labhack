from enum import Enum, auto


class RenderOrder(Enum):
    """Represents the order that entities are rendered."""
    TRAP = auto()
    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()