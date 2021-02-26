from .actions import ActionWithDirection
from actions.die_action import DieAction
from src import exceptions
import random


class AttackAction(ActionWithDirection):
    def __init__(self, entity, dx, dy):
        super().__init__(entity, dx, dy)
        # Determine if the entity will hit or miss the target entity.
        # The entity will roll a 20 sided die, and try to get below a target number.
        self.target_base = 10
        self.die = 20
        self.attack_comp = None

    def perform(self):
        target = self.target_actor
        if not target:
            raise exceptions.Impossible("Nothing to attack!")

        # Iterate through all the attacks
        for atk in self.attack_comp.attacks:
            if self.roll_hit_die() < self.calc_target_number(target):
                dmg = self.execute_damage(target, atk)

                # Generate appropriate message
                if dmg > 0:
                    self.hit_msg(target, atk, dmg)
                else:
                    # Blocking message
                    self.blocked_msg(target)
            else:
                self.miss(target)

        # Check if the target is dead...
        if target.fighter.is_dead():
            return DieAction(entity=target, cause=self.entity)

    def roll_hit_die(self):
        # Rolls a 1d20 die to determine if the attacker will land the hit.
        return random.randint(1, self.die)

    def calc_target_number(self, target):
        # TODO: Factor in penalty for multi-hit moves.
        defender_ac = target.fighter.ac
        attacker_level = self.entity.level.current_level

        if target.fighter.ac < 0:
            # If the defender has negative AC, choose a number from -1 to their AC
            defender_ac = -random.randint(1, abs(target.fighter.ac))

        num = self.target_base + defender_ac + attacker_level

        if num < 1:
            # If we get a negative, set it to 1.
            return 1
        return num

    def execute_damage(self, target, atk):
        # It's a hit! Calculate the damage
        dmg = atk.roll_dies()

        # Calculate damage reduction from targets AC
        dmg = self.reduce_dmg(target, dmg)
        target.fighter.hp -= dmg
        return dmg

    @staticmethod
    def reduce_dmg(target, dmg):
        """ Calculates how much damage the defender takes after  factoring in it's AC.
            There is no damage reduction if the defender has 0+ AC.
            If the target has negative AC, calculates how much damage reduction it recieves.
            If the damage would be reduced below 1, it is always set to at least 1.
        """
        if target.fighter.ac >= 0:
            return dmg

        dmg_reduced = random.randint(1, abs(target.fighter.ac))
        result = dmg - dmg_reduced
        if result < 1:
            return 1
        else:
            return result

    def blocked_msg(self, target):
        # TODO: Update with component type/breed check
        if self.entity.name == "player":
            self.msg = f"The {target.name} blocks your attack! "
        # TODO: Update with component type/breed check
        elif target.name == "player":
            self.msg = f"You block the {self.entity}'s attack! "
        else:
            self.msg = f"The {target.name} blocks the {self.entity}'s attack! "

    def miss(self, target):
        # TODO Add "Just Miss" for one off roll, wildly miss for 15+ off

        # TODO: Update with component type/breed check
        if self.entity.name == "player":
            self.msg = f"You miss the {target.name}. "
        # TODO: Update with component type/breed check
        elif target.name == "player":
            self.msg = f"The {self.entity} misses you. "
        else:
            self.msg = f"The {self.entity} misses the {target.name}. "

    def hit_msg(self, target, atk, dmg):
        """Creates the msg to describe one Actor hitting another Actor with a weapon."""
        raise NotImplementedError()


class MeleeAttack(AttackAction):
    def __init__(self, entity, dx, dy):
        super().__init__(entity, dx, dy)
        self.attack_comp = self.entity.attack_comp

    def hit_msg(self, target, atk, dmg):
        """Creates the msg to describe one Actor hitting another Actor with a melee attack."""

        self.msg = f"The {self.entity} {atk.name}s the {target.name} for {dmg}! "

        # TODO: Update with component type/breed check
        if self.entity.name == "player":
            self.msg = f"You {atk.name} the {target.name} for {dmg}! "
        # TODO: Update with component type/breed check
        elif target.name == "player":
            self.msg = f"The {self.entity} {atk.name}s you for {dmg}! "
        else:
            self.msg = f"The {self.entity} {atk.name}s the {target.name} for {dmg}! "


class WeaponAttack(AttackAction):
    def __init__(self, entity, dx, dy):
        super().__init__(entity, dx, dy)

        self.weapon = self.entity.equipment.slots['WEAPON']
        self.attack_comp = self.weapon.equippable.attack_comp

    def hit_msg(self, target, atk, dmg):
        """Creates the msg to describe one Actor hitting another Actor with a weapon."""

        self.msg = f"The {self.entity} hits the {target.name} with a {atk.name} for {dmg}! "

        # TODO: Update with component type/breed check
        if self.entity.name == "player":
            self.msg = f"You hit the {target.name} with your {atk.name} for {dmg}! "
        # TODO: Update with component type/breed check
        elif target.name == "player":
            self.msg = f"The {self.entity} hits you with it's {atk.name} for {dmg}! "
        else:
            self.msg = f"The {self.entity} hits the {target.name} with it's {atk.name} for {dmg}! "
