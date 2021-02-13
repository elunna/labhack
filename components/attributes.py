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
        return self.base_ac + self.equipment_bonus('AC')

    @property
    def strength(self):
        return self.base_strength + self.equipment_bonus('STRENGTH')

    @property
    def dexterity(self):
        return self.base_dexterity + self.equipment_bonus('DEXTERITY')

    def equipment_bonus(self, attribute):
        # Is this more usable if it takes Equipment as an arg?
        if self.parent.equipment:
            return self.parent.equipment.attribute_bonus(attribute)
        else:
            return 0
