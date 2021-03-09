from components.component import Component


class Fighter(Component):
    """Represents an Actor that can receieve and deal damage."""
    parent = None  # Should be Actor

    def __init__(self, max_hp, base_ac):
        self.max_hp = max_hp
        self._hp = max_hp
        self.base_ac = base_ac

    @property
    def hp(self):
        """ Return the actor's current hp."""
        return self._hp

    @hp.setter
    def hp(self, value):
        """Attempts to set the actor's hp to the given value.
        The hp cannot be set above the actor's max_hp or lower than 0.
        """
        self._hp = max(0, min(value, self.max_hp))

    @property
    def ac(self):
        """Returns the actor's current AC with any bonuses."""
        return self.base_ac + self.ac_bonus()

    def ac_bonus(self):
        """Returns the sum of any AC bonuses that the actor's equipment provides. """
        if self.parent.equipment:
            return self.parent.equipment.attribute_bonus('AC')
        return 0

    def heal(self, amount):
        """ Heals actor's HP for the given amount and returns the amount recovered."""
        if self.hp == self.max_hp:
            return 0

        new_hp_value = self.hp + amount

        if new_hp_value > self.max_hp:  # TODO: Is this needed with the setter?
            new_hp_value = self.max_hp

        amount_recovered = new_hp_value - self.hp

        self.hp = new_hp_value

        return amount_recovered

    def is_dead(self):
        """Returns True if the actor's HP is 0 or less, False otherwise."""
        return self.hp <= 0
