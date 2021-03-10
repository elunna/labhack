from components.attack import Attack
from components.attack_cmp import AttackComponent
from components.attributes import Attributes
from components.energy import EnergyComponent
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import PlayerInventory
from components.level import Level
from components.regeneration import Regeneration
from src.actor import Actor


class Player(Actor):
    def __init__(self):
        super().__init__(
            player=True,  # Let's us work with the player component around the game.
            char="@",
            color=(255, 255, 255),
            ai=None,
            equipment=Equipment(),
            fighter=Fighter(max_hp=30, base_ac=10),
            attack_comp=AttackComponent(Attack('punch', [2])),
            attributes=Attributes(base_strength=5),

            # Original inventory capacity is 267 because we have 26 lowercase letters plus $
            inventory=PlayerInventory(capacity=27),

            level=Level(level_up_base=20, difficulty=0),
            energy=EnergyComponent(refill=12),
            regeneration=Regeneration(),
        )
