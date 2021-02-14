from components.component import Component
from components.equipment import EquipmentType
from components.attributes import AttributeType
from src.thindict import ThinDict


class Equippable(Component):
    # parent: Item
    parent = None

    def __init__(
            self,
            equipment_type,
            ac_bonus=0,
            strength_bonus=0,
            dexterity_bonus=0,
    ):
        # Validate the equipment type, must be in the EquipmentType enum
        self.equipment_type = equipment_type

        # The attribute modifiers are derived from the AttributeType enum.
        # We can only use these pre-determined slots that are enforced by the ThinDict.
        self.modifiers = ThinDict(allowed_keys=[a.name for a in AttributeType], initial_val=0)
        self.modifiers['AC'] = ac_bonus
        self.modifiers['STRENGTH'] = strength_bonus
        self.modifiers['DEXTERITY'] = dexterity_bonus


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


class Helmet(Equippable):
    def __init__(self, ac_bonus=0):
        super().__init__(
            equipment_type=EquipmentType.HELMET,
            ac_bonus=ac_bonus
        )


class Gloves(Equippable):
    def __init__(self, ac_bonus=0):
        super().__init__(
            equipment_type=EquipmentType.GLOVES,
            ac_bonus=ac_bonus
        )


class Boots(Equippable):
    def __init__(self, ac_bonus=0):
        super().__init__(
            equipment_type=EquipmentType.BOOTS,
            ac_bonus=ac_bonus
        )


class Shield(Equippable):
    def __init__(self, ac_bonus=0):
        super().__init__(
            equipment_type=EquipmentType.SHIELD,
            ac_bonus=ac_bonus
        )


class Arms(Equippable):
    def __init__(self, ac_bonus=0):
        super().__init__(
            equipment_type=EquipmentType.ARMS,
            ac_bonus=ac_bonus
        )



class Belt(Equippable):
    def __init__(self, ac_bonus=0):
        super().__init__(
            equipment_type=EquipmentType.BELT,
            ac_bonus=ac_bonus
        )