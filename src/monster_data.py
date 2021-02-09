from components.ai import HostileAI
from components.attacks import AttackType
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from src import actor

grid_bug = actor.Actor(
    char="x",
    color=(0, 127, 0),
    name="Grid Bug",
    ai_cls=HostileAI,
    equipment=Equipment(),
    fighter=Fighter(
        hp=1,
        base_ac=1,
        base_power=1,
        attacks=AttackType(die_sides=1),
    ),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=1),
)
orc = actor.Actor(
    char="o",
    color=(63, 127, 63),
    name="Orc",
    ai_cls=HostileAI,
    equipment=Equipment(),
    fighter=Fighter(
        hp=4,
        base_ac=7,
        base_power=3,
        attacks=AttackType(die_sides=3),
    ),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
)
troll = actor.Actor(
    char="T",
    color=(0, 127, 0),
    name="Troll",
    ai_cls=HostileAI,
    equipment=Equipment(),
    fighter=Fighter(
        hp=11,
        base_ac=2,
        base_power=10,
        attacks=AttackType(die_sides=6),
    ),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=100),
)