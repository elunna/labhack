from components.component import Component
from settings import EquipmentType


class Equipment(Component):
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
        # TODO: Rename to is_equipped
        """ Returns True if the item is equipped, otherwise returns False."""
        return self.weapon == item or self.armor == item

    def unequip_message(self, item_name):
        # TODO: Remove/refactor this
        self.parent.gamemap.engine.msg_log.add_message(
            f"You remove the {item_name}."
        )

    def equip_message(self, item_name):
        # TODO: Remove/refactor this
        self.parent.gamemap.engine.msg_log.add_message(
            f"You equip the {item_name}."
        )

    def equip_to_slot(self, slot, item, add_message):
        """ Attempts to equip an item to a slot on the actor.
            add_message: Optional boolean to specify if we want to print a message about equipping.

            Returns True if successful, False otherwise.
        """
        # Check if item is suitable for the slot.
        # Convert the enum to a str so we can compare...
        # TODO: Needs to check if the item has the EquippableComponent
        item_slot = item.equippable.equipment_type.name.lower()

        if item_slot != slot:
            # TODO: Put a msg here "Item doesn't match slot"
            return False

        current_item = getattr(self, slot)

        if current_item is not None:
            self.unequip_from_slot(slot, add_message)

        setattr(self, slot, item)

        if add_message:
            self.equip_message(item.name)

        return True

    def unequip_from_slot(self, slot, add_message):
        """ Attempts to unequip an item from a slot on the actor.
            add_message: Optional boolean to specify if we want to print a message about equipping.

            Returns True if successful, False otherwise.
        """
        current_item = getattr(self, slot)

        if add_message:
            self.unequip_message(current_item.name)

        if current_item:
            setattr(self, slot, None)
            return True
        return False

    def toggle_equip(self, item, add_message=True):
        """ Attempts to equip an unequipped item, or unequip an equipped item.
            add_message: Optional boolean to specify if we want to print a message about equipping.
        """
        # Can we equip it?
        if not item.equippable:
            return False

        # Does the item slot match what is available?
        slot = item.equippable.equipment_type.name.lower()
        if slot not in ["weapon", "armor"]:
            return False

        if getattr(self, slot) == item:
            self.unequip_from_slot(slot, add_message)
        else:
            self.equip_to_slot(slot, item, add_message)

        return True
