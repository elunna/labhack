from components.base_component import BaseComponent
from src.settings import EquipmentType


class Equipment(BaseComponent):
    """ An Actor can equip a piece of Equipment. The weapon and armor attributes
        are what will hold the actual equippable entity. Both can be set to None,
        which represents nothing equipped in those slots.
    """
    def __init__(self, weapon=None, armor=None):
        self.weapon = weapon
        self.armor = armor

    @property
    def defense_bonus(self):
        bonus = 0

        if self.weapon is not None and self.weapon.equippable is not None:
            bonus += self.weapon.equippable.defense_bonus

        if self.armor is not None and self.armor.equippable is not None:
            bonus += self.armor.equippable.defense_bonus

        return bonus

    @property
    def power_bonus(self):
        bonus = 0

        if self.weapon is not None and self.weapon.equippable is not None:
            bonus += self.weapon.equippable.power_bonus

        if self.armor is not None and self.armor.equippable is not None:
            bonus += self.armor.equippable.power_bonus

        return bonus

    def item_is_equipped(self, item):
        """ Returns True if the item is equipped, otherwise returns False."""
        return self.weapon == item or self.armor == item

    def unequip_message(self, item_name):
        self.parent.gamemap.engine.message_log.add_message(
            f"You remove the {item_name}."
        )

    def equip_message(self, item_name):
        self.parent.gamemap.engine.message_log.add_message(
            f"You equip the {item_name}."
        )

    def equip_to_slot(self, slot, item, add_message):
        """ Attempts to equip an item to a slot on the actor.
            add_message: Optional boolean to specify if we want to print a message about equipping.
        """
        current_item = getattr(self, slot)

        if current_item is not None:
            self.unequip_from_slot(slot, add_message)

        setattr(self, slot, item)

        if add_message:
            self.equip_message(item.name)

    def unequip_from_slot(self, slot, add_message):
        """ Attempts to unequip an item to a slot on the actor.
            add_message: Optional boolean to specify if we want to print a message about equipping.
        """
        current_item = getattr(self, slot)

        if add_message:
            self.unequip_message(current_item.name)

        setattr(self, slot, None)

    def toggle_equip(self, equippable_item, add_message=True):
        """ Attempts to equip an unequipped item, or unequip an equipped item.
            add_message: Optional boolean to specify if we want to print a message about equipping.
        """

        if (
            equippable_item.equippable
            and equippable_item.equippable.equipment_type == EquipmentType.WEAPON
        ):
            slot = "weapon"
        else:
            slot = "armor"

        if getattr(self, slot) == equippable_item:
            self.unequip_from_slot(slot, add_message)
        else:
            self.equip_to_slot(slot, equippable_item, add_message)
