import random


class AttackType:
    """ Describes an Actors attack types and corresponding damage dies.
        bite: d6
        hit: d2
        punch: d2

        We might be able to create lambdas for more advanced calculations.
        claw: 2d6 + 1
    """
    def __init__(self, description, die_sides):
        self.description = description
        self.die_sides = die_sides

    def roll_attacks(self):
        # Generator to roll through all attacks
        # Simulates a die roll for the attack die.
        return random.randint(1, self.die_sides)