from actions.itemaction import ItemAction
from src import exceptions


class DropItem(ItemAction):
    def perform(self):
        """ Removes an item from an entity's inventory and places it on the
            current game map, at the entity's coordinates.
        """
        # If the item is an equipped item, first unequip it.
        if self.entity.equipment.item_is_equipped(self.item):
            self.entity.equipment.toggle_equip(self.item)

        # Remove it from inventory
        result = self.entity.inventory.rm_item(self.item)

        if result:
            # Put it on the map
            # self.item.place(self.entity.x, self.entity.y, self.entity.gamemap)

            self.entity.gamemap.entities.add(self.item)
            self.item.x = self.entity.x
            self.item.y = self.entity.y

            self.msg = f"You dropped the {self.item.name}."
        else:
            raise exceptions.Impossible("You cannot drop an item you do not have!")