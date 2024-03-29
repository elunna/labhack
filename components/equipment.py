from enum import Enum, auto
from components.component import Component
from src import exceptions


class EquipmentType(Enum):
    """Represents all the available slots of equipment an actor can equip."""
    WEAPON = auto()     # Main Hand?
    ARMOR = auto()
    HELMET = auto()
    BOOTS = auto()
    GLOVES = auto()
    SHIELD = auto()     # Offhand?
    BELT = auto()
    ARMS = auto()       # (R/L)

    # SUIT

    # TODO: Slot over another slot (Ex: Tshirt under armor, under cloak)


class Equipment(Component):
    """ An Actor can equip a piece of Equipment. The weapon and armor attributes
        are what will hold the actual equippable entity. Both can be set to None,
        which represents nothing equipped in those slots.
    """
    def __init__(self, *args):
        # The equipment slots are derived from the EquipmentType enum.
        self.slots = {et.name: None for et in EquipmentType}

        # We will accept a list of items (*args) to try and equip at init.
        for item in args:
            self.toggle_equip(item)

    def attribute_bonus(self, attribute):
        """Calculates how much of a bonus the given attribute gets from all the equipped items."""
        equipped_items = [i for i in self.slots.values() if i]
        return sum(i.equippable.modifiers[attribute] for i in equipped_items)

    def is_equipped(self, item):
        """ Returns True if the item is equipped, otherwise returns False."""
        return item in self.slots.values()

    def slot_equipped(self, slot):
        """ Returns True if the item is equipped, otherwise returns False."""
        if slot not in self.slots:
            raise ValueError("Invalid slot!")
        return self.slots.get(slot) is not None

    def unequip_message(self, item_name):
        """Returns an unequip message."""
        return f"You remove the {item_name}. "

    def equip_message(self, item_name):
        """Returns an equipment message."""
        return f"You equip the {item_name}. "

    def equip_to_slot(self, slot, item):
        """ Attempts to equip an item to a slot on the actor.
            If successful, returns a string describing what happened.
            If not, returns an empty string.
        """
        # Check if the item is equippable
        if not getattr(item, "equippable", None):
            raise exceptions.Impossible("f{item.name} is not an Equippable!")

        # Check if item's slot is valid
        # Convert the enum to a str so we can compare...
        item_slot = item.equippable.equipment_type.name

        if item_slot not in self.slots:
            raise exceptions.Impossible(f"The item's slot ({slot}) is not valid!")

        # Item slot must also match the provided slot.
        if item_slot != slot:
            raise exceptions.Impossible(f"The item's slot ({slot}) does not match the provided slot {item_slot}!")

        msg = ''
        # current_item = getattr(self, slot)
        current_item = self.slots[slot]

        if current_item is not None:
            msg += self.unequip_from_slot(slot)

        # Equip the new item
        self.slots[item_slot] = item

        msg += self.equip_message(item.name)
        return msg

    def unequip_from_slot(self, slot):
        """ Attempts to unequip an item from a slot on the actor.
            If successful, returns a string describing what happened.
            If not, returns an empty string.
        """
        current_item = self.slots[slot]

        if current_item:
            self.slots[slot] = None
            return self.unequip_message(current_item.name)
        return f'The {slot} slot is not equipped with anything!'

    def toggle_equip(self, item):
        """ Attempts to equip an unequipped item, or unequip an equipped item.
            Returns a string describing what happened.
        """
        # Can we equip it?
        if not getattr(item, "equippable", None):
            raise exceptions.Impossible("f{item.name} is not an Equippable!")

        # Does the item slot match what is available?
        slot = item.equippable.equipment_type.name

        if self.slots[slot] == item:
            return self.unequip_from_slot(slot)
        else:
            return self.equip_to_slot(slot, item)
