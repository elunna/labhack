from actions.actions import Action
from src import exceptions


class PickupAction(Action):
    """Pickup an item and add it to the inventory, if there is room for it."""
    def __init__(self, entity):
        super().__init__(entity)

    def perform(self):
        # TODO: Support for piles
        # TODO: Pickup menu handler

        actor_location_x = self.entity.x
        actor_location_y = self.entity.y
        inventory = self.entity.inventory

        for item in self.entity.gamemap.items:
            if actor_location_x == item.x and actor_location_y == item.y:
                if len(inventory.items) >= inventory.capacity:
                    raise exceptions.Impossible("Your inventory is full.")

                self.entity.gamemap.rm_entity(item)
                item.parent = self.entity.inventory
                inventory.add_item(item)
                self.msg = f"({item.item.last_letter}) - {item.name}"
                return

        raise exceptions.Impossible("There is nothing here to pick up.")