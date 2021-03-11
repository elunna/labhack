from components.component import Component
from src.settings import ENERGY_THRESHOLD
import random


class EnergyComponent(Component):
    """ Manages the actor's energy which allows them to perform actions during a turn.
        Each turn the engine provides a refill, which is determined by the refill amount in this
        component. The standard threshold is 12.
        A refill value of 0 makes the actor a stationary actor, since it will never act.
    """
    def __init__(self, refill):
        if refill < 0:
            raise ValueError("refill amount must be greater than or equal to 0!")

        self.threshold = ENERGY_THRESHOLD  # Standard is 12 for all actors.
        self.refill = refill

        # Start each actor with a random amount of energy so movements
        # are staggered for like enemies.
        self.energy = random.randint(0, refill)

    def add_energy(self):
        """ Adds the refill amount to the actor's entergy."""
        self.energy += self.refill

    def burn_turn(self):
        """ Depletes the actor's energy by a turn's amount (standard is 12)"""
        if self.energy >= self.threshold:
            self.energy -= self.threshold
            return True
        return False

    def burned_out(self):
        """Returns True if the actor has enough energy for another turn, False otherwise."""
        return self.energy < self.threshold
