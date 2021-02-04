from components.component import Component
import random


def myround(x, base=25):
    """ Simple rounding function to make xp levels look cleaner.
        Rounds to the nearest 'base'
    """
    return base * round(x/base)


class Level(Component):
    # parent: Actor

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
        # TODO: Rename
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

        # Too much info
        # self.engine.msg_log.add_message(f"You gain {xp} experience points.")

        # Move this to an action
        # if self.requires_level_up:
            # self.engine.msg_log.add_message(
                # f"You advance to level {self.current_level + 1}!"
            # )

    def increase_level(self):
        if not self.requires_level_up:
            return False

        self.current_xp -= self.experience_to_next_level
        self.current_level += 1

        # Increase the level_up_base to get a bigger curve
        self.level_up_base += self.level_up_base * self.base_gain_per_level

        return True

    def get_random_stat_increase(self):
        # TODO: Move to FighterComponent?
        choice = random.randint(1, 3)
        if choice == 1:
            self.increase_max_hp()
        elif choice == 2:
            self.increase_power()
        else:
            self.increase_defense()

    def increase_max_hp(self, amount = 20):
        # TODO: Move to FighterComponent?
        self.parent.fighter.max_hp += amount
        self.parent.fighter.hp += amount
        self.engine.msg_log.add_message("Your health improves!")
        self.increase_level()

    def increase_power(self, amount = 1):
        # TODO: Move to FighterComponent?
        self.parent.fighter.base_power += amount
        self.engine.msg_log.add_message("You feel stronger!")
        self.increase_level()

    def increase_defense(self, amount = 1):
        # TODO: Move to FighterComponent?
        self.parent.fighter.base_defense += amount
        self.engine.msg_log.add_message("Your movements are getting swifter!")
        self.increase_level()


def display_chart(base=20, factor=2):
    'Useful for comparing the XP level requirements.'
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

