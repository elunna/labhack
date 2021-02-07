import random


class AttackType:
    def __init__(self, die_sides, description='hits'):
        self.die_sides = die_sides
        self.description = description

    def roll_attack(self):
        # Simulates a die roll for the attack die.
        return random.randint(1, self.die_sides)
