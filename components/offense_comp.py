from components.component import Component


class OffenseComponent(Component):
    """Manages the attacks that an entity can perform."""
    def __init__(self, *args):
        # args is a tuple of Attack named tuples
        self.attacks = tuple(args)

    def __len__(self):
        """Returns the number of attacks in this component."""
        return len(self.attacks)
