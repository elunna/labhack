from .item_action import ItemAction
from src import exceptions


class DropAction(ItemAction):
    def perform(self):
        """ Removes an item from an entity's inventory and places it on the
            current game map, at the entity's coordinates.
        """
        # If the item is an equipped item, first unequip it.
        if self.entity.equipment.is_equipped(self.item):
            self.entity.equipment.toggle_equip(self.item)

        # If stackable, drop all of them
        if self.item.item.stackable:
            amount = self.item.item.stacksize
        else:
            amount = 1

        result = self.entity.inventory.rm_item(self.item, amount)

        if result:
            # Put it on the map
            self.entity.gamemap.add_entity(result, self.entity.x, self.entity.y)

            if amount == 1:
                self.msg = f"You dropped a {result.name}."
            else:
                self.msg = f"You dropped {amount} {result.name}s."
        else:
            raise exceptions.Impossible("You cannot drop an item you do not have!")
