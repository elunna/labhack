import random
from collections import defaultdict


class Attack:
    """Represents a single attack in a monsters arsenal or a weapon."""
    def __init__(self, name, dies):
        self.name = name
        self.dies = dies

    def min_dmg(self):
        """Returns the lowest possible damage this can deal."""
        return len(self.dies)

    def max_dmg(self):
        """Returns the highest possible damage this can deal."""
        return sum(self.dies)

    def roll_dies(self):
        """Rolls all of dice in self.dies, and returns the sum of the results."""
        return sum(random.randint(1, d) for d in self.dies)

    def to_text(self):
        """Returns a Dnotation representation of the dice."""
        groups = defaultdict(int)
        for d in self.dies:
            groups[d] += 1

        # display by smallest groups first, then by size of dice
        return '+'.join([f"{groups[g]}d{g}" for g in sorted(groups)])
