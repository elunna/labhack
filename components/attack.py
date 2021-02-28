import random
from collections import defaultdict


class Attack:
    def __init__(self, name, dies):
        self.name = name
        self.dies = dies

    def min_dmg(self):
        return len(self.dies)

    def max_dmg(self):
        return sum(self.dies)

    def roll_dies(self):
        # Takes in a list of dies, rolls all of them, and returns the sum of the results.
        return sum(random.randint(1, d) for d in self.dies)

    def to_text(self):
        groups = defaultdict(int)
        for d in self.dies:
            groups[d] += 1

        # display by smallest groups first, then by size of dice
        return '+'.join([f"{groups[g]}d{g}" for g in sorted(groups)])
