from components.component import Component
from collections import defaultdict
from src import settings
import string


class Inventory(Component):
    """ Dictionary based Inventory
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
        if len(self.items) >= 26:
            # Inventory full
            return False

        # If we add the item, we need to choose a new inventory letter
        # We cannot use an existing letter, but we will keep a running
        # letter count to keep new letter being assigned in a logical order
        while True:
            if self.current_letter not in self.items:
                self.items[self.current_letter] = item
                return True
            self.current_letter = self.letterroll.next_letter()

    def rm_item(self, item):
        for k, v in self.items.items():
            if v == item:
                item = self.items.pop(k)
                return item

    def rm_letter(self, letter):
        if letter in self.items:
            self.items.pop(letter)

    def sorted_dict(self):
        # Sort out the items by char/category (weapons(/), potions(!), etc
        # Create a dict of char and values is a list of item letters
        result = defaultdict(list)
        for key_letter, item in self.items.items():
            result[item.char].append(key_letter)
        return result


class LetterRoll:
    def __init__(self):
        # self.letters = string.ascii_lowercase + string.ascii_uppercase
        self.letters = string.ascii_lowercase
        self.index = -1

    def next_letter(self):
        self.index += 1
        i = self.index % len(self.letters)
        return self.letters[i]
