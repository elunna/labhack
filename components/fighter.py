from components.component import Component
from components.attack_cmp import AttackComponent
from components.attack import Attack


class Fighter(Component):
    parent = None  # Should be Actor

    def __init__(self, hp, attacks=None):
        self.max_hp = hp
        self._hp = hp

    @property
    def hp(self):
        # Just returns the hp
        return self._hp

    @hp.setter
    def hp(self, value):
        # Never set the hp to less than 0 or higher than max_hp.
        self._hp = max(0, min(value, self.max_hp))

    def heal(self, amount):
        if self.hp == self.max_hp:
            return 0

        new_hp_value = self.hp + amount

        if new_hp_value > self.max_hp:
            new_hp_value = self.max_hp

        amount_recovered = new_hp_value - self.hp

        self.hp = new_hp_value

        return amount_recovered

    def is_dead(self):
        return self.hp <= 0
