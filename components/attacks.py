import random


class AttackType:
    """ Describes an attack type and corresponding damage dies and bonus.
        bite: d6
        hit: d2
        punch: d2

        We might be able to create lambdas for more advanced calculations.
        claw: 2d6 + 1
    """
    def __init__(self, die_sides, damage_bonus=0):
        self.die_sides = die_sides  # Any extra damage added after the die rolls
        self.damage_bonus = damage_bonus

    def roll_dmg(self):
        # Generator to roll through all attacks
        # Simulates a die roll for the attack die.
        return random.randint(1, self.die_sides)