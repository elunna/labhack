from components.component import Component
from components.equipment import EquipmentType
from components.attributes import AttributeType


class Equippable(Component):
    """Represents an item that can be equipped or wielded."""
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
        self.modifiers = {a.name: 0 for a in AttributeType}
        self.modifiers['AC'] = ac_bonus
        self.modifiers['STRENGTH'] = strength_bonus
        self.modifiers['DEXTERITY'] = dexterity_bonus


class Weapon(Equippable):
    """Represents an equippable weapon."""
    def __init__(self, attack_comp):
        super().__init__(equipment_type=EquipmentType.WEAPON)
        self.attack_comp = attack_comp


class Armor(Equippable):
    """Represents an equippable piece of armor."""
    def __init__(self, ac_bonus=0):
        super().__init__(
            equipment_type=EquipmentType.ARMOR,
            ac_bonus=ac_bonus
        )


class Helmet(Equippable):
    """Represents an equippable piece of headgear."""
    def __init__(self, ac_bonus=0):
        super().__init__(
            equipment_type=EquipmentType.HELMET,
            ac_bonus=ac_bonus
        )


class Gloves(Equippable):
    """Represents an equippable pair of gloves."""
    def __init__(self, ac_bonus=0):
        super().__init__(
            equipment_type=EquipmentType.GLOVES,
            ac_bonus=ac_bonus
        )


class Boots(Equippable):
    """Represents an equippable pair of footwear."""
    def __init__(self, ac_bonus=0):
        super().__init__(
            equipment_type=EquipmentType.BOOTS,
            ac_bonus=ac_bonus
        )


class Shield(Equippable):
    """Represents an equippable shield."""
    def __init__(self, ac_bonus=0):
        super().__init__(
            equipment_type=EquipmentType.SHIELD,
            ac_bonus=ac_bonus
        )


class Arms(Equippable):
    """Represents an equippable armor for the arms, or a tool that goes on the wrist."""
    def __init__(self, ac_bonus=0):
        super().__init__(
            equipment_type=EquipmentType.ARMS,
            ac_bonus=ac_bonus
        )


class Belt(Equippable):
    """Represents an equippable belt."""
    def __init__(self, ac_bonus=0):
        super().__init__(
            equipment_type=EquipmentType.BELT,
            ac_bonus=ac_bonus
        )
