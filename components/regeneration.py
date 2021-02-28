import math
import random

from components.component import Component
"""
todo: Hit point regeneration
    RegenerationComponent
    x_turns
    eligible_for_regen()
"""


class Regeneration(Component):
    def x_turns(self, level):
        if level < 10:
            return math.floor((42 / (level + 2)) + 1)
        else:
            return 3

    def eligible_for_regen(self, level, turns):
        return turns % self.x_turns(level) == 0

    def regen_amt(self, con, level):
        if level < 10 or con <= 12:
            return 1
        max_gain = level - 9
        gain = random.randint(1, con)
        if gain > max_gain:
            return max_gain
        return gain

    #  If your Constitution is 12 or lower, you get one hit point.
    # Otherwise, you get d(Con) hitpoints up to a maximum of your level minus 9.