from components.component import Component
from src.equipment_types import EquipmentType


class Equippable(Component):
    # parent: Item
    parent = None

    def __init__(self, equipment_type, power_bonus=0, ac_bonus=0):
        self.equipment_type = equipment_type

        self.power_bonus = power_bonus
        self.ac_bonus = ac_bonus


# TODO: Create Weapon class
# TODO: Create Armor class
# TODO: Other slots: Helmet, Boots, Gloves, Belt

class Weapon(Equippable):
    def __init__(self):
        super().__init__(
            equipment_type=EquipmentType.WEAPON,
            power_bonus=2
        )

class Dagger(Equippable):
    def __init__(self):
        super().__init__(
            equipment_type=EquipmentType.WEAPON,
            power_bonus=2
        )


class Sword(Equippable):
    def __init__(self):
        super().__init__(
            equipment_type=EquipmentType.WEAPON,
            power_bonus=4
        )


class LeatherArmor(Equippable):
    def __init__(self):
        super().__init__(
            equipment_type=EquipmentType.ARMOR,
            ac_bonus=1
        )


class ChainMail(Equippable):
    def __init__(self):
        super().__init__(
            equipment_type=EquipmentType.ARMOR,
            ac_bonus=3
        )
