from .component import Component


class ItemComponent(Component):
    def __init__(self, appearance, weight, material, stackable=False, breakable=0):
        self.appearance = appearance
        self.weight = weight
        self.material = material

        # The breakable number means it has a 1 in x chance of breaking, 0 never breaks
        self.breakable = breakable

        self.stackable = stackable
        self.last_letter = None  # Last letter used for the player's inventory.

