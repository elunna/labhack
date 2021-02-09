from components.ai import HostileAI
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from . import actor
import copy

from .item_data import (
    health_potion,
    lightning_scroll,
    confusion_scroll,
    fireball_scroll,
    dagger,
    sword,
    leather_armor,
    chain_mail
)
from .monster_data import grid_bug, orc, troll


def make(entity_name):
    if entity_name == 'player':
        return copy.deepcopy(player)
    elif entity_name == 'grid bug':
        return copy.deepcopy(grid_bug)
    elif entity_name == 'orc':
        return copy.deepcopy(orc)
    elif entity_name == 'troll':
        return copy.deepcopy(troll)
    elif entity_name == 'dagger':
        return copy.deepcopy(dagger)
    elif entity_name == 'sword':
        return copy.deepcopy(sword)
    elif entity_name == 'leather armor':
        return copy.deepcopy(leather_armor)
    elif entity_name == 'chain mail':
        return copy.deepcopy(chain_mail)
    elif entity_name == 'health potion':
        return copy.deepcopy(health_potion)
    elif entity_name == 'lightning scroll':
        return copy.deepcopy(lightning_scroll)
    return None

player = actor.Actor(
    char="@",
    color=(255, 255, 255),
    name="Player",
    ai_cls=HostileAI,
    equipment=Equipment(),
    fighter=Fighter(hp=30, base_ac=10, base_power=5),

    # Original inventory capacity is 26 because we have 26 lowercase letters.
    inventory=Inventory(capacity=26),
    level=Level(level_up_base=20),
)

item_chances = {
    # keys in the dictionary represent the floor number,
    # and the value is a list of tuples.
    0: [(health_potion, 35)],
    2: [(confusion_scroll, 10)],
    4: [(lightning_scroll, 25), (sword, 5)],
    6: [(fireball_scroll, 25), (chain_mail, 15)],
}

enemy_chances = {
    0: [(orc, 80)],
    3: [(troll, 15)],
    5: [(troll, 30)],
    7: [(troll, 60)],
}
