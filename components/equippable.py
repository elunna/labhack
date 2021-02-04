from components.component import Component
from settings import EquipmentType


class Equippable(Component):
    """ Represents an item that can be wielded or worn, like a weapon or piece
        of armor.
        TODO: Add dict or enum for equipment_type
        TODO: Check that equipment_type is valid
        TODO: Erosion, Corrosion, Burnedness, etc
        TODO: Enchantment level?

    """
    # parent: Item
    parent = None

    def __init__(self, equipment_type, power_bonus=0, defense_bonus=0):
        self.equipment_type = equipment_type

        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus


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
            defense_bonus=1
        )


class ChainMail(Equippable):
    def __init__(self):
        super().__init__(
            equipment_type=EquipmentType.ARMOR,
            defense_bonus=3
        )
