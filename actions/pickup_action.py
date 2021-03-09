from actions.actions import Action
from src import exceptions


class PickupAction(Action):
    """Pickup an item and add it to the inventory, if there is room for it."""
    def __init__(self, entity):
        super().__init__(entity)

    def perform(self):
        """Picks up an item from the entities' current location and adds it to their inventory."""
        inventory = self.entity.inventory
        # items_on_location = self.entity.gamemap.get_items_at(self.entity.x, self.entity.y)
        items_on_location = self.entity.gamemap.filter(
            "item",
            x=self.entity.x,
            y=self.entity.y
        )
        for item in items_on_location:
            # If stackable, pickup all of them
            if "stackable" in item:
                amount = item.stackable.size
            else:
                amount = 1

            result = self.entity.gamemap.rm_item(item)
            if result:
                result.x = -1
                result.y = -1
                letter = inventory.add_inv_item(result, amount)
            else:
                raise Exception('No result from rm_item!')

            if amount > 1:
                self.msg = f"({letter}) - {amount} {result.name}s"
            else:
                self.msg = f"({letter}) - {result.name}"
            return

        raise exceptions.Impossible("There is nothing here to pick up.")
