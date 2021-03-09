from components.component import Component
from src.settings import DEFAULT_THRESHOLD
import random


class EnergyComponent(Component):
    """ Manages the actor's energy which allows them to perform actions during a turn.
        Each turn the engine provides a refill, which is determined by the refill amount in this
        component. The standard threshold is 12.
    """
    def __init__(self, threshold=DEFAULT_THRESHOLD):
        if threshold <= 0:
            raise ValueError("EnergyMeter threshold must be a positive integer!")

        self.threshold = threshold

        # Start each actor with a random amount of energy so movements
        # are staggered for like enemies.
        self.energy = random.randint(0, threshold)

    def add_energy(self, amt):
        """ Adds the refill amount to the actor's entergy."""
        self.energy += amt

    def burn_turn(self):
        """ Depletes the actor's energy by a turn's amount (standard is 12)"""
        if self.energy >= self.threshold:
            self.energy -= self.threshold
            return True
        return False

    def burned_out(self):
        """Returns True if the actor has enough energy for another turn, False otherwise."""
        return self.energy < self.threshold
