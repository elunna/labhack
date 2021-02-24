from actions.actions import ActionWithDirection
from actions.move import MovementAction
from actions.attack_actions import MeleeAttack, WeaponAttack


class BumpAction(ActionWithDirection):
    """ When acting in a direction, decides which class, between MeleeAction and
        MovementAction to return.
    """
    def perform(self):
        if self.target_actor:
            # Does the entity have a weapon?
            if self.entity.equipment.slots['WEAPON']:
                return WeaponAttack(self.entity, self.dx, self.dy)
            else:
                return MeleeAttack(self.entity, self.dx, self.dy)
        else:
            return MovementAction(self.entity, self.dx, self.dy)
