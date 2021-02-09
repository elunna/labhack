from actions.actions import ActionWithDirection
from actions.move import MovementAction
from actions.melee import MeleeAction


class BumpAction(ActionWithDirection):
    """ When acting in a direction, decides which class, between MeleeAction and
        MovementAction to return.
    """
    def perform(self):
        if self.target_actor:
            return MeleeAction(self.entity, self.dx, self.dy)
        else:
            return MovementAction(self.entity, self.dx, self.dy)