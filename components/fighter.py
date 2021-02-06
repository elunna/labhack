from src import color
from components.component import Component
from src.renderorder import RenderOrder


class Fighter(Component):
    # TODO: Pass in Equipment variable?
    parent = None  # Should be Actor

    def __init__(self, hp, base_defense, base_power):
        self.max_hp = hp
        self._hp = hp
        self.base_defense = base_defense
        self.base_power = base_power

    @property
    def hp(self):
        # Just returns the hp
        return self._hp

    @hp.setter
    def hp(self, value):
        # Never set the hp to less than 0 or higher than max_hp.
        self._hp = max(0, min(value, self.max_hp))

    @property
    def defense(self):
        return self.base_defense + self.defense_bonus

    @property
    def power(self):
        return self.base_power + self.power_bonus

    @property
    def defense_bonus(self):
        if self.parent.equipment:
            return self.parent.equipment.defense_bonus
        else:
            return 0

    @property
    def power_bonus(self):
        if self.parent.equipment:
            return self.parent.equipment.power_bonus
        else:
            return 0

    def heal(self, amount):
        if self.hp == self.max_hp:
            return 0

        new_hp_value = self.hp + amount

        if new_hp_value > self.max_hp:
            new_hp_value = self.max_hp

        amount_recovered = new_hp_value - self.hp

        self.hp = new_hp_value

        return amount_recovered

    def take_dmg(self, amount):
        self.hp -= amount
        if self._hp == 0 and self.parent.ai:
            return self.die()
        return ''

    def die(self):
        if self.engine.player is self.parent:
            death_message = "You died!"
        else:
            death_message = f"The {self.parent.name} dies!"

        self.parent.char = "%"
        self.parent.color = (191, 0, 0)
        self.parent.blocks_movement = False
        self.parent.ai = None
        self.parent.name = f"{self.parent.name} corpse"
        self.parent.render_order = RenderOrder.CORPSE
        self.engine.player.level.add_xp(self.parent.level.xp_given)

        return death_message
