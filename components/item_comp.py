from .component import Component


class ItemComponent(Component):
    def __init__(self, breakable=0):
        # The breakable number means it has a 1 in x chance of breaking, 0 never breaks
        self.breakable = breakable

        self.last_letter = None  # Last letter used for the player's inventory.
