from components.component import Component
from src import exceptions


class Equipment(Component):
    """ An Actor can equip a piece of Equipment. The weapon and armor attributes
        are what will hold the actual equippable entity. Both can be set to None,
        which represents nothing equipped in those slots.
    """
    def __init__(self, weapon=None, armor=None):
        self.weapon = None
        self.armor = None

        if weapon:
            self.toggle_equip(weapon)

        if armor:
            self.toggle_equip(armor)

    @property
    def ac_bonus(self):
        bonus = 0

        if self.weapon is not None and self.weapon.equippable is not None:
            bonus += self.weapon.equippable.ac_bonus

        if self.armor is not None and self.armor.equippable is not None:
            bonus += self.armor.equippable.ac_bonus

        return bonus

    @property
    def strength_bonus(self):
        bonus = 0

        if self.weapon is not None and self.weapon.equippable is not None:
            bonus += self.weapon.equippable.strength_bonus

        if self.armor is not None and self.armor.equippable is not None:
            bonus += self.armor.equippable.strength_bonus

        return bonus

    @property
    def dexterity_bonus(self):
        bonus = 0

        if self.weapon is not None and self.weapon.equippable is not None:
            bonus += self.weapon.equippable.dexterity_bonus

        if self.armor is not None and self.armor.equippable is not None:
            bonus += self.armor.equippable.dexterity_bonus

        return bonus


    def item_is_equipped(self, item):
        """ Returns True if the item is equipped, otherwise returns False."""
        return self.weapon == item or self.armor == item

    def unequip_message(self, item_name):
        return f"You remove the {item_name}. "

    def equip_message(self, item_name):
        return f"You equip the {item_name}. "

    def equip_to_slot(self, slot, item):
        """ Attempts to equip an item to a slot on the actor.
            If successful, returns a string describing what happened.
            If not, returns an empty string.
        """

        equippable = getattr(item, "equippable")
        if not equippable:
            raise exceptions.Impossible("f{item.name} is not an Equippable!")

        # Check if item is suitable for the slot.
        # Convert the enum to a str so we can compare...
        item_slot = item.equippable.equipment_type.name.lower()

        if item_slot != slot:
            raise exceptions.Impossible("Cannot equip item f{item.name} to slot f{slot}!")

        msg = ''
        current_item = getattr(self, slot)

        if current_item is not None:
            msg += self.unequip_from_slot(slot)

        setattr(self, slot, item)

        msg += self.equip_message(item.name)
        return msg


    def unequip_from_slot(self, slot):
        """ Attempts to unequip an item from a slot on the actor.
            If successful, returns a string describing what happened.
            If not, returns an empty string.
        """
        current_item = getattr(self, slot)

        if current_item:
            setattr(self, slot, None)
            return self.unequip_message(current_item.name)
        return f'The {slot} slot is not equipped with anything!'

    def toggle_equip(self, item):
        """ Attempts to equip an unequipped item, or unequip an equipped item.
            Returns a string describing what happened.
        """
        # Can we equip it?
        if not item.equippable:
            raise exceptions.Impossible(f"We cannot equip the {item.name}!")


        # Does the item slot match what is available?
        slot = item.equippable.equipment_type.name.lower()
        if slot not in ["weapon", "armor"]:
            raise exceptions.Impossible("Cannot equip item f{item.name} to slot f{slot}!")

        if getattr(self, slot) == item:
            return self.unequip_from_slot(slot)
        else:
            return self.equip_to_slot(slot, item)
