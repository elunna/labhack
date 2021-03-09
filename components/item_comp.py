from .component import Component


class ItemComponent(Component):
    """An entity which has this component is defined as an Item. If the player picks up an
    item it keeps track of the letter used so it can be reused if dropped.
    """
    def __init__(self, breakable=0):
        # The breakable number means it has a 1 in x chance of breaking, 0 never breaks
        self.breakable = breakable
        self.last_letter = None  # Last letter used for the player's inventory.