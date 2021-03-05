import copy

from components.component import Component


class StackableComponent(Component):
    def __init__(self, size=1):
        # self.max_size = 1000
        self.size = size

    def merge_stack(self, item, qty=0):
        """ Merge a different item's stack into this one.
            This stack gains an amount equal to the other stack's size
            The other stack is depleted.
            The default for qty is 0 - which forces the full stack to merge into this one.
            returns True if the operation succeeded, False if it did not.
        """
        # if not self.parent.is_similar(item):
        #     return False

        if qty == 0:
            qty = item.stackable.size

        item.stackable.split_stack(qty)  # Decrease the source stack
        self.size += qty  # Add to this stack

        return True

    def split_stack(self, qty):
        """ Splits this items stack into a new Item with a stack of qty size.
            Cannot split more than the stack size.
            Returns a new Item if successful, None if not.
        """
        if qty <= 0:
            raise ValueError("split_stack requires a positive integer for stack size!")

        if qty > self.size:
            raise ValueError("split_stack received qty greater than stack size!")

        cloned_item = copy.deepcopy(self.parent)
        cloned_item.stackable.size = qty

        self.size -= qty

        return cloned_item
