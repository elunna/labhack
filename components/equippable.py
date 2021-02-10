from components.component import Component
from src.equipment_types import EquipmentType


class Equippable(Component):
    # parent: Item
    parent = None

    def __init__(
            self,
            equipment_type,
            strength_bonus=0,
            ac_bonus=0
    ):

        self.equipment_type = equipment_type
        self.strength_bonus = strength_bonus
        self.ac_bonus = ac_bonus


class Weapon(Equippable):
    def __init__(self, attack):
        super().__init__(equipment_type=EquipmentType.WEAPON)
        self.attack = attack


class Armor(Equippable):
    def __init__(self, ac_bonus=0):
        super().__init__(
            equipment_type=EquipmentType.ARMOR,
            ac_bonus=ac_bonus
        )
