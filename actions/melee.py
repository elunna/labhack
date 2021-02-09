import random

from actions.actions import ActionWithDirection
from actions.death import DieAction
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

        # Setup for the attack descriptions
        entity = self.entity.name.capitalize()
        target_number = self.calc_target_number(target)

        if self.roll_hit_die() < self.calc_target_number(target):
            # It's a hit!
            result = 0
            # Calculate the damage
            if self.entity.equipment.weapon:
                dmg = self.hit_with_weapon(target)
            else:
                dmg = self.hit_with_barehands(target)

            target.fighter.hp -= dmg

            # Check if the target is dead...
            if target.fighter.is_dead():
                return DieAction(entity=target, cause=self.entity)

        else:
            self.miss(target)

    def calc_target_number(self, target):
        return self.target_base + target.fighter.ac + target.level.current_level

    def roll_hit_die(self):
        # Rolls a 1d20 die to determine if the attacker will land the hit.
        return random.randint(1, self.die)

    def hit_with_weapon(self, target):
        # Get the damage from the weapon
        weapon = self.entity.equipment.weapon
        dmg = weapon.equippable.attack.roll_dmg()
        # atk_text = self.entity.fighter.attacks.description
        self.msg = f"The {self.entity} hits the {target.name} with a {weapon.name} for {dmg}! "

        # TODO Case where we hit something
        # TODO Case where something hits us

        return dmg

    def hit_with_barehands(self, target):
        # We'll use the entities "natural" attack, or Bare-Handed for our Hero.
        dmg = self.entity.fighter.attacks.roll_dmg()
        self.msg = f"The {self.entity} hits the {target.name} for {dmg}! "

        # TODO Case where we hit something
        # TODO Case where something hits us
        return dmg

    def miss(self, target):
        self.msg = f"The {self.entity.name.capitalize()} misses the {target.name}. "
        # TODO Add "Wildly misses"