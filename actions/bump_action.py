from actions.actions import ActionWithDirection
from actions.attack_actions import MeleeAttack, WeaponAttack
from actions.movement_action import MovementAction, WriggleAction
from src import settings
import random


class BumpAction(ActionWithDirection):
    """ When acting in a direction, decides which class, between MeleeAction and
        MovementAction to return.
    """
    def perform(self):
        """Has the actor perform a 'Bump' in a certain direction - which is basically a test to
        see if they can move.
            If a move is valid, we return a MoveAction.
            If they encounter any obstacles, like another actor, then a different action will be performed instead.
        """
        # Is the actor confused? If so, we'll hijack the destination.
        if "confused" in self.entity.states.states:
            self.dx, self.dy = random.choice(settings.DIRECTIONS)

        if self.target_actor:
            # Does the entity have a weapon?
            if self.entity.equipment.slots['WEAPON']:
                return WeaponAttack(self.entity, self.dx, self.dy)
            else:
                return MeleeAttack(self.entity, self.dx, self.dy)
        elif "trapped" in self.entity.states.states:
            return WriggleAction(self.entity, self.dx, self.dy)
        else:
            return MovementAction(self.entity, self.dx, self.dy)

