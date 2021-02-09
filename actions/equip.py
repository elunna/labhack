from actions.actions import Action


class EquipAction(Action):
    def __init__(self, entity, item):
        super().__init__(entity)
        self.item = item

    def perform(self):
        self.msg = self.entity.equipment.toggle_equip(self.item)