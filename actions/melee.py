import random

from actions.actions import ActionWithDirection
from actions.death import DieAction
from components.attacks import AttackComponent
from src import exceptions


class MeleeAction(ActionWithDirection):
    def __init__(self, entity, dx, dy):
        super().__init__(entity, dx, dy)
        # Determine if the entity will hit or miss the target entity.
        # The entity will roll a 20 sided die, and try to get below a target number.
        self.target_base = 10
        self.die = 20

    def perform(self):
        target = self.target_actor
        if not target:
            raise exceptions.Impossible("Nothing to attack!")

        weapon = self.entity.equipment.slots['WEAPON']
        if weapon:
            attack_comp = weapon.equippable.attack
            use_method = self.hit_with_weapon
        else:
            attack_comp = self.entity.attacks
            use_method = self.hit_with_barehands

        # Iterate through all the attacks
        for atk in attack_comp.attacks:
            if self.roll_hit_die() < self.calc_target_number(target):
                # It's a hit!
                # Calculate the damage
                dmg = use_method(target, atk)

                target.fighter.hp -= dmg

                # Check if the target is dead...
                if target.fighter.is_dead():
                    return DieAction(entity=target, cause=self.entity)

            else:
                self.miss(target)

    def calc_target_number(self, target):
        defender_ac = target.attributes.ac
        attacker_level = self.entity.level.current_level

        if target.attributes.ac < 0:
            # If the defender has negative AC, choose a number from -1 to their AC
            defender_ac = -random.randint(1, abs(target.attributes.ac))

        num = self.target_base + defender_ac + attacker_level

        if num < 1:
            # If we get a negative, set it to 1.
            return 1
        return num

    def roll_hit_die(self):
        # Rolls a 1d20 die to determine if the attacker will land the hit.
        return random.randint(1, self.die)

    def hit_with_weapon(self, target, atk):
        # Get the damage from the weapon
        dmg = AttackComponent.roll_dies(atk.dies)

        # atk_text = self.entity.fighter.attacks.description
        self.msg = f"The {self.entity} hits the {target.name} with a {atk.name} for {dmg}! "

        if self.entity.name == "Player":
            self.msg = f"You hit the {target.name} with your {atk.name} for {dmg}! "
        elif target.name == "Player":
            self.msg = f"The {self.entity} hits you with it's {atk.name} for {dmg}! "
        else:
            self.msg = f"The {self.entity} hits the {target.name} with a {atk.name} for {dmg}! "

        return dmg

    def hit_with_barehands(self, target, atk):
        # We'll use the entities "natural" attack, or Bare-Handed for our Hero.
        dmg = AttackComponent.roll_dies(atk.dies)
        self.msg = f"The {self.entity} {atk.name}s the {target.name} for {dmg}! "

        if self.entity.name == "Player":
            self.msg = f"You {atk.name} the {target.name} for {dmg}! "
        elif target.name == "Player":
            self.msg = f"The {self.entity} {atk.name}s you for {dmg}! "
        else:
            self.msg = f"The {self.entity} {atk.name}s the {target.name} for {dmg}! "

        return dmg

    def miss(self, target):
        # TODO Add "Just Miss" for one off roll, wildly miss for 15+ off

        if self.entity.name == "Player":
            self.msg = f"You miss the {target.name}. "
        elif target.name == "Player":
            self.msg = f"The {self.entity} misses you. "
        else:
            self.msg = f"The {self.entity} misses the {target.name}. "
