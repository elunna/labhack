import copy

from components.component import Component


class StackableComponent(Component):
    def __init__(self, size=1):
        # TODO: Can we limit access to this if the item isn't stackable?
        self.size = size

    def merge_stack(self, item):
        """ Merge a different item's stack into this one.
            This stack gains an amount equal to the other stack's size
            The other stack is depleted.
            returns True if the operation succeeded, False if it did not.
        """
        # if not self.parent.is_similar(item):
        #     return False

        self.size += item.stackable.size
        item.stackable.size = 0

        # Should this also destroy the other?  Call parent.rm_entity?
        return True

    def split_stack(self, qty):
        """ Splits this items stack into a new Item with a stack of qty size.
            Cannot split more than the stack size.
            Returns a new Item if successful, None if not.
        """
        cloned_item = copy.deepcopy(self.parent)
        cloned_item.stackable.size = qty
        self.deplete_stack(qty)
        return cloned_item

    def deplete_stack(self, qty):
        """ Consumes a portion (or all) of the items in this stack. If all the items are
        used up, the Item is destroyed. Returns True if successful, False otherwise.
        """
        if qty < 1 or qty > self.size:
            raise ValueError("deplete stack must be within the size!")
        self.size -= qty
        return True