from enum import Enum, auto
from components.component import Component


class AttributeType(Enum):
    AC = auto()
    STRENGTH = auto()
    DEXTERITY = auto()
    CONSTITUTION = auto()
    # INTELLIGENCE
    # CHARISMA
    # AGILITY?


class Attributes(Component):
    """Represents all the important characteristics of a player: Strength, Dexterity, etc."""
    def __init__(
        self,
        base_strength=10,
        base_dexterity=10,
        base_constitution=10,
    ):
        self.base_strength = base_strength
        self.base_dexterity = base_dexterity
        self.base_constitution = base_constitution

    @property
    def strength(self):
        """Returns the player's current strength with any bonuses."""
        return self.base_strength + self.equipment_bonus('STRENGTH')

    @property
    def dexterity(self):
        """Returns the player's current dexterity with any bonuses."""
        return self.base_constitution + self.equipment_bonus('CONSTITUTION')

    @property
    def constitution(self):
        """Returns the player's current constitution with any bonuses."""
        return self.base_dexterity + self.equipment_bonus('DEXTERITY')

    def equipment_bonus(self, attribute):
        """Checks the players equipment for any stat bonuses."""
        # Is this more usable if it takes Equipment as an arg?
        if self.parent.equipment:
            return self.parent.equipment.attribute_bonus(attribute)
        else:
            return 0
