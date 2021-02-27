from components.component import Component
from components.attack_cmp import AttackComponent
from components.attack import Attack


class Fighter(Component):
    parent = None  # Should be Actor

    def __init__(self, max_hp, base_ac):
        self.max_hp = max_hp
        self._hp = max_hp
        self.base_ac = base_ac

    @property
    def hp(self):
        # Just returns the hp
        return self._hp

    @hp.setter
    def hp(self, value):
        # Never set the hp to less than 0 or higher than max_hp.
        self._hp = max(0, min(value, self.max_hp))

    @property
    def ac(self):
        return self.base_ac + self.ac_bonus()

    def ac_bonus(self):
        if self.parent.equipment:
            return self.parent.equipment.attribute_bonus('AC')
        return 0

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
