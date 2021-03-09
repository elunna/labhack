from actions.actions import Action


class EquipAction(Action):
    """An action describing an actor equipping a specific piece of gear."""
    def __init__(self, entity, item):
        super().__init__(entity)
        self.item = item

    def perform(self):
        """Directs the actor to toggle the equipped status of an item.
            If it's equipped, it unequips it. If not equipped, it equips it.
        """
        self.msg = self.entity.equipment.toggle_equip(self.item)