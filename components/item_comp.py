from .component import Component


class ItemComponent(Component):
    def __init__(self, stackable=False, breakable=0):
        # The breakable number means it has a 1 in x chance of breaking, 0 never breaks
        self.breakable = breakable

        self.stackable = stackable
        self.last_letter = None  # Last letter used for the player's inventory.

        # TODO: Can we limit access to this if the item isn't stackable?
        self.stacksize = 1