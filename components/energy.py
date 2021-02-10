from components.component import Component
from src.settings import DEFAULT_THRESHOLD
import random


class EnergyMeter(Component):
    def __init__(self, threshold=DEFAULT_THRESHOLD):
        if threshold <= 0:
            raise ValueError("EnergyMeter threshold must be a positive integer!")

        self.threshold = threshold

        # Start each actor with a random amount of energy so movements
        # are staggered for like enemies.
        self.energy = random.randint(0, threshold)

    def add_energy(self, amt):
        self.energy += amt

    def burn_turn(self):
        if self.energy >= self.threshold:
            self.energy -= self.threshold
            return True
        return False

    def burned_out(self):
        return self.energy < self.threshold
