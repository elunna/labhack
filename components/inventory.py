from components.component import Component
from collections import defaultdict
from src.letterroll import LetterRoll


class Inventory(Component):
    """ Dictionary based Inventory
        # TODO: Add contains, subscrioption, weight, size
        ex:
            $ XXX.XX dogecoin
            # Weapons
            (a) Dagger
            (b) Dagger
            (c) Sword

            # Armor
            (d) Leather Jacket

            # Potions
            (e) Potion of Health

            # Scrolls
            (f) Scroll of Confusion
    """
    def __init__(self, capacity):
        # Max number of items an Actor can hold.
        self.capacity = capacity
        self.items = {}
        self.letterroll = LetterRoll()
        self.current_letter = self.letterroll.next_letter()

    def add_item(self, item):
        # Attempts to add an item to the inventory. Returns True if successful, False otherwise.
        # If we add the item
        if len(self.items) >= self.capacity:
            # Inventory full
            return False

        # If we add the item, we need to choose a new inventory letter
        # We cannot use an existing letter, but we will keep a running
        # letter count to keep new letter being assigned in a logical order
        while True:
            if self.current_letter not in self.items:
                self.items[self.current_letter] = item

                # Set the item's parent to be this inventory
                item.parent = self

                return True
            self.current_letter = self.letterroll.next_letter()

    def rm_item(self, item):
        # Removes an item from the inventory. Returns True if successful, False
        # otherwise.
        for k, v in self.items.items():
            if v == item:
                item = self.items.pop(k)

                # Reset the item's parent to None
                item.parent = None

                return True
        return False

    def rm_letter(self, letter):
        # Removes an item from the inventory by using it's assigned letter.
        # If the letter is being used, we remove the item and return True.
        # If no item is found using that letter, return False
        if letter in self.items:
            item = self.items.pop(letter)

            # Reset the item's parent to None
            item.parent = None

            return True
        return False

    def sorted_dict(self):
        # Sort out the items by char/category (weapons(/), potions(!), etc
        # Create a dict of char and values is a list of item letters
        result = defaultdict(list)
        for key_letter, item in self.items.items():
            result[item.char].append(key_letter)
        return result
