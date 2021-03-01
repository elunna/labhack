import copy

from .component import Component
from src import exceptions


class ItemComponent(Component):
    def __init__(self, stackable=False, breakable=0):
        # The breakable number means it has a 1 in x chance of breaking, 0 never breaks
        self.breakable = breakable

        self.stackable = stackable
        self.last_letter = None  # Last letter used for the player's inventory.

        # TODO: Can we limit access to this if the item isn't stackable?
        self.stacksize = 1

    def merge_stack(self, other):
        """ Merge another stackable item of the same type into this one.
            This stack gains an amount equal to the other stack's size
            The other stack & item is destroyed.
            returns True if the operation succeeded, False if it did not.
        """
        if not self.stackable:
            raise exceptions.Impossible("Item is not stackable!")

    def split_stack(self, qty):
        """ Splits this items stack into a new Item with a stack of qty size.
            Cannot split more than the stack size.
            Returns a new Item if successful, None if not.
        """
        if not self.stackable:
            raise exceptions.Impossible("Item is not stackable!")
        elif qty < 1 or qty >= self.stacksize:
            raise ValueError("split_stack requires positive integer for qty!")
        self.deplete_stack(qty)
        new_item = copy.deepcopy(self.parent)
        new_item.item.stacksize = qty
        return new_item

    def deplete_stack(self, qty):
        """ Consumes a portion (or all) of the items in this stack
            If all the items are used up, the Item is destroyed.
            Returns True if successful, False otherwise.
        """
        if not self.stackable:
            raise exceptions.Impossible("Item is not stackable!")
        elif qty < 1 or qty > self.stacksize:
            raise ValueError("deplete stack must be within the stacksize!")

        self.stacksize -= qty
        return True
