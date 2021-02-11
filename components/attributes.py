from components.component import Component


class Attributes(Component):
    def __init__(
        self,
        base_ac=10,
        base_strength=10,
        base_dexterity=10,
        base_constitution=10,
    ):
        self.base_ac = base_ac
        self.base_strength = base_strength
        self.base_dexterity = base_dexterity
        self.base_constitution = base_constitution

    @property
    def ac(self):
        return self.base_ac + self.ac_bonus

    @property
    def strength(self):
        return self.base_strength + self.strength_bonus

    @property
    def dexterity(self):
        return self.base_dexterity + self.dexterity_bonus

    @property
    def ac_bonus(self):
        if self.parent.equipment:
            return self.parent.equipment.ac_bonus
        else:
            return 0

    @property
    def strength_bonus(self):
        if self.parent.equipment:
            return self.parent.equipment.strength_bonus
        else:
            return 0

    @property
    def dexterity_bonus(self):
        if self.parent.equipment:
            return self.parent.equipment.dexterity_bonus
        else:
            return 0
