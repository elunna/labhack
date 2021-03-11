import random
from collections import defaultdict


class Attack:
    """ Represents the capabilities of a single attack in a monster, weapon, item, or trap (or other entity)."""
    def __init__(self, name, dies):
        # the attack name:
        self.name = name

        # The attack "verbs" (ie: kicks, bites, punches, etc)
        # self.verbs = verbs

        # The die(s) to roll for each attack
        self.dies = dies

        # Any special power associated with the attack (cold, fire, poison)
        # self.special = ...

        # bonus to-hit

        # bonus damage

        # against specific breeds of monsters, we can also add (or subtract) certain bonuses:
        # Water vs metallic enemies
        # Poison vs non-poison resistant enemies
        # Cold vs Fire-resistant enemies
        # Fire vs cold-resistant enemies

        # Also good to note what kind of attack this falls into:
        # Melee: standard
        # Ranged (thrown object)
        # Ray (Wand/gun)
        # Firearms
        # Explosive (huge to-hit bonus

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
