from components.component import Component
from src.utils import myround


class Level(Component):
    def __init__(
        self,
        current_level=1,
        current_xp=0,
        level_up_base=20,
        level_up_factor=2,
        xp_given=0,
    ):
        self.current_level = current_level
        self.current_xp = current_xp
        self.level_up_base = level_up_base
        self.level_up_factor = level_up_factor
        self.xp_given = xp_given
        self.base_gain_per_level = .25

    @property
    def experience_to_next_level(self):
        # return self.level_up_base + self.current_level * self.level_up_factor
        result = self.level_up_base * (self.current_level ** self.level_up_factor)
        return myround(result)

    @property
    def requires_level_up(self):
        return self.current_xp >= self.experience_to_next_level

    def add_xp(self, xp):
        if xp == 0 or self.level_up_base == 0:
            return
        self.current_xp += xp

    def increase_level(self):
        if not self.requires_level_up:
            return False

        self.current_xp -= self.experience_to_next_level
        self.current_level += 1

        # Increase the level_up_base to get a bigger curve
        self.level_up_base += self.level_up_base * self.base_gain_per_level

        return True

    def increase_max_hp(self, amount=20):
        self.parent.fighter.max_hp += amount
        self.parent.fighter.hp += amount
        self.increase_level()

    def increase_strength(self, amount=1):
        self.parent.attributes.base_strength += amount
        self.increase_level()

    def increase_ac(self, amount=-1):
        self.parent.fighter.base_ac += amount
        self.increase_level()


def display_chart(base=20, factor=2):
    """Useful for comparing the XP level requirements."""
    max_level = 20

    level = Level(
        level_up_base=base,
        level_up_factor=factor,
    )

    for i in range(max_level):
        current = level.current_level
        to_next = level.experience_to_next_level

        print(f"level: {current} required: {to_next}")

        # increase level
        level.add_xp(to_next)

        if level.requires_level_up:
            level.increase_level()


if __name__ == "__main__":
    display_chart()
