from components.component import Component
from collections import defaultdict

from src.item import Item
from src.letterroll import LetterRoll


class Inventory(Component):
    """ Dictionary based Inventory
        # TODO: Add contains, subscrioption, weight, size

    """
    def __init__(self, capacity):
        # Max number of items an Actor can hold.
        self.capacity = capacity
        self.items = {}
        self.letterroll = LetterRoll()
        self.current_letter = self.letterroll.next_letter()

    def add_item(self, item, qty=1):
        # Attempts to add an item to the inventory. Returns True if successful, False otherwise.

        # Only add Entity's that have the ItemComponent
        if not isinstance(item, Item):
            return False

        # Is it stackable and does it have a matching item it can stack with?
        if "stackable" in item:
            match = self.get_matching_item(item)
            if match:
                # This should match the other items size
                match.stackable.size += qty

                # Also set the letter in the ItemComponent
                item.item.last_letter = match.item.last_letter
                return True

        # Do we have room for a new item slot?
        if len(self.items) >= self.capacity:
            # Inventory full
            return False

        # If we add the item, we need to choose an inventory letter.
        # If we have owned the item before, it will have the last letter used, we'll try that first.
        letter = item.item.last_letter
        if not letter or letter in self.items:
            letter = self.find_next_letter()

        # Also set the letter in the ItemComponent
        item.item.last_letter = letter

        self.items[letter] = item

        # Set the item's parent to be this inventory
        item.parent = self

        return True

    def find_next_letter(self):
        # We cannot use an existing letter, but we will keep a running
        # letter count to keep new letter being assigned in a logical order
        while True:
            if self.current_letter not in self.items:
                return self.current_letter
            self.current_letter = self.letterroll.next_letter()

    def rm_entity(self, e):
        # Adapter for gamemap
        self.rm_item(e)

    def rm_item(self, item, qty=1):
        # Removes an item from the inventory and returns it.
        # If the item doesn't exist in the inventory, returns None
        for k, v in self.items.items():
            if v == item:
                new_item = self.items.get(k)
                # Check if the item is stackable
                if "stackable" in item:
                    # Reduce it by the specified qty
                    # Split the stack
                    new_item = item.stackable.split_stack(qty)

                # Totally remove items that are not stackable, or have a 0 size.
                if "stackable" not in item or item.stackable.size == 0:
                    self.items.pop(k)
                # Reset the item's parent to None
                new_item.parent = None

                # Don't forget the new_item's Parent setting.
                return new_item
        return None

    def rm_letter(self, letter, qty=1):
        # Removes an item from the inventory by using it's assigned letter.
        # If the letter is being used, we remove the item and return True.
        # If no item is found using that letter, return False
        if letter in self.items:
            item = self.items.get(letter)
            # Use rm_item
            self.rm_item(item, qty)
            return True
        return False

    def sorted_dict(self):
        # Sort out the items by char/category (weapons(/), potions(!), etc
        # Create a dict of char and values is a list of item letters

        result = defaultdict(list)
        for key_letter, item in self.items.items():
            result[item.char].append(key_letter)
        return result

    def get_matching_item(self, item):
        """ Searches the inventory items for a matching item type,
            if found it returns the item, otherwise returns None.
        """
        for k, v in self.items.items():
            # TODO: Use a more sophisticated check than item name.
            if item.name == v.name:
                return v
        return None
