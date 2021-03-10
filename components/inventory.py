from collections import defaultdict
from components.component import Component
from components.equippable import Weapon
from components.letter import LetterComponent
from src import exceptions, settings, utils
from src.entity_manager import EntityManager
from src.letterroll import LetterRoll


class Inventory(Component, EntityManager):
    """ Manages the inventory of a regular game actor."""
    def __init__(self, capacity):
        # capacity is the max number of items an Actor can hold.
        # Only accepts entities with the item component
        super().__init__(capacity=capacity, required_comp="item")

    def add_inv_item(self, item, qty=0):
        """Adds an item to the inventory. just a wrapper for EntityManager.add_item."""
        return self.add_item(item, qty)

    def rm_inv_item(self, item, qty=0):
        """Removes an item from the inventory. just a wrapper for EntityManager.rm_item."""
        return self.rm_item(item, qty)


class PlayerInventory(Component, EntityManager):
    """ Special inventory for the player. Items are assigned letters and managed with a item_dict
    so we can access items by inventory letter.
    """
    def __init__(self, capacity):
        # Only accepts entities with the item component
        super().__init__(capacity=capacity, required_comp="item")
        self.item_dict = {}
        self.letterroll = LetterRoll()
        self.current_letter = self.letterroll.next_letter()

    def add_inv_item(self, item, qty=0):
        """Attempts to add an item to the inventory.
        Returns True if successful, False otherwise.
        Money always goes in $
        """

        previous_size = len(self)
        result = self.add_item(item, qty)
        size_changed = len(self) != previous_size
        current_items = self.item_dict.values()

        if result and not size_changed:
            # it added to a stackable. Letter is already set
            twin = self.get_similar(item)
            return twin.letter.letter

        elif result and size_changed:
            # a new slot was occupied
            # Scan the entities to see what was added.
            new_item = [e for e in self.entities if e not in current_items][0]

            # See if this item has a previous letter
            letter = None
            if new_item.has_comp("letter"):
                letter = new_item.letter.letter

            # We'll need to find a new letter if there the last_letter is being used or is None.
            # Otherwise, we can just use it by default!
            if not letter or letter in self.item_dict:
                letter = self.find_next_letter()

            # Also set the letter in the ItemComponent
            new_item.add_comp(letter=LetterComponent(letter))

            self.item_dict[letter] = new_item
            return letter

        # Something went wrong...
        raise exceptions.Impossible

    def rm_inv_item(self, item, qty=0):
        """ Removes an item from the inventory and returns it.
        If the item doesn't exist in the inventory, returns None
        $ always money, $ is never completely removed.
        """
        if item in self.entities:
            # First, get the letter of the item
            letter = item.letter.letter
            result = self.rm_item(item, qty)

            if item not in self.entities:
                self.item_dict.pop(letter)
            return result
        return None

    def find_next_letter(self):
        """ Finds the next logical letter to assign to a new item. First we check the current_letter,
        and if that one is used we run through the letter roll for the next available one.
        """
        while True:
            if self.current_letter not in self.item_dict:
                return self.current_letter
            self.current_letter = self.letterroll.next_letter()

    def rm_letter(self, letter, qty=0):
        """ Removes an item from the inventory by using it's assigned letter.
        If the letter is being used, we remove the item and return it.
        If no item is found using that letter, return None
        """
        if letter in self.item_dict:
            item = self.item_dict.get(letter)
            return self.rm_inv_item(item, qty)
        return None

    def sorted_dict(self):
        """ Sort out the items by char/category (weapons(/), potions(!), etc
        Create a dict of char and values is a list of item letters
        """
        result = defaultdict(list)
        for key_letter, item in sorted(self.item_dict.items()):
            result[item.char].append(key_letter)
        return result

    def list_contents(self):
        contents = []
        item_groups = self.sorted_dict()

        for char in settings.ITEM_CATEGORIES:
            groups = item_groups.get(char)
            if groups:
                group_name = settings.ITEM_CATEGORIES[char]
                contents.append(f" {char}  {group_name}:")
            else:
                continue

            for group in groups:
                for letter in group:
                    item_key = letter
                    item = self.item_dict[letter]
                    is_equipped = self.parent.equipment.is_equipped(item)
                    item_string = f"({item_key}) {item}"

                    # Weapon notation strings
                    if "equippable" in item and isinstance(item.equippable, Weapon):
                        dnotation = item.equippable.attack_comp.attacks[0].to_text()
                        item_string += f"({dnotation})"

                    if is_equipped:
                        item_string += f" (Equipped)"

                    contents.append(item_string)

            contents.append('')  # Blank line between groups.
        return contents
