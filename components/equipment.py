from components.component import Component
from src import exceptions
from src.thindict import ThinDict
from src.equipment_types import EquipmentType


class Equipment(Component):
    """ An Actor can equip a piece of Equipment. The weapon and armor attributes
        are what will hold the actual equippable entity. Both can be set to None,
        which represents nothing equipped in those slots.
    """
    def __init__(self, *args):
        # The equipment slots are derived from the EquipmentType enum.
        # We can only use these pre-determined slots that are enforced by the ThinDict.
        self.slots = ThinDict(allowed_keys=[et.name for et in EquipmentType])

        # We will accept a list of items (*args) to try and equip at init.
        for item in args:
            self.toggle_equip(item)

    @property
    def ac_bonus(self):
        # TODO: Remove check for equippable? If it's in a slot, we know it's equippable!
        equipped_items = [i for i in self.slots.values() if i and i.equippable]
        return sum(i.equippable.ac_bonus for i in equipped_items)

    @property
    def strength_bonus(self):
        equipped_items = [i for i in self.slots.values() if i and i.equippable]
        return sum(i.equippable.strength_bonus for i in equipped_items)

    @property
    def dexterity_bonus(self):
        equipped_items = [i for i in self.slots.values() if i and i.equippable]
        return sum(i.equippable.dexterity_bonus for i in equipped_items)

    def item_is_equipped(self, item):
        """ Returns True if the item is equipped, otherwise returns False."""
        return item in self.slots.values()

    def unequip_message(self, item_name):
        return f"You remove the {item_name}. "

    def equip_message(self, item_name):
        return f"You equip the {item_name}. "

    def equip_to_slot(self, slot, item):
        """ Attempts to equip an item to a slot on the actor.
            If successful, returns a string describing what happened.
            If not, returns an empty string.
        """
        # Check if the item is equippable
        equippable = getattr(item, "equippable")
        if not equippable:
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
        # TODO: Duplicated in equip.. remove?
        if not item.equippable:
            raise exceptions.Impossible(f"We cannot equip the {item.name}!")

        # Does the item slot match what is available?
        slot = item.equippable.equipment_type.name
        if slot not in self.slots:
            raise exceptions.Impossible("Cannot equip item f{item.name} to slot f{slot}!")

        if self.slots[slot] == item:
            return self.unequip_from_slot(slot)
        else:
            return self.equip_to_slot(slot, item)
