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

    def activate(self, turns):
        level = self.parent.level.current_level
        if self.eligible_for_regen(level, turns):
            heal_amt = self.regen_amt(self.parent.attributes.constitution, level)
            self.parent.fighter.heal(heal_amt)