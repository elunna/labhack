from components.base_component import BaseComponent


class Inventory(BaseComponent):
    def __init__(self, capacity):
        # Max number of items an Actor can hold.
        self.capacity = capacity
        self.items = []

    def drop(self, item):
        """ Removes an item from the inventory and restores it to the game map,
            at the player's current location.
        """
        self.items.remove(item)
        item.place(self.parent.x, self.parent.y, self.gamemap)

        self.engine.message_log.add_message(f"You dropped the {item.name}.")
