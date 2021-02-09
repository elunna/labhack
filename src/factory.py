from components import consumable, attacks
from components import equippable
from components.ai import HostileAI
from components.attacks import AttackType
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from . import actor
from . import item
import copy

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

health_potion = item.Item(
    char="!",
    color=(127, 0, 255),
    name="Health Potion",
    consumable=consumable.HealConsumable(amount=5),
)

lightning_scroll = item.Item(
    char="~",
    color=(255, 255, 0),
    name="Lightning Scroll",
    consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
)

confusion_scroll = item.Item(
    char="~",
    color=(207, 63, 255),
    name="Confusion Scroll",
    consumable=consumable.ConfusionConsumable(number_of_turns=10),
)

fireball_scroll = item.Item(
    char="~",
    color=(255, 0, 0),
    name="Fireball Scroll",
    consumable=consumable.FireballDamageConsumable(damage=12, radius=3),
)


dagger = item.Item(
    char="/",
    color=(0, 191, 255),
    name="Dagger",
    equippable=equippable.Weapon(
        attack=attacks.AttackType(die_sides=3),
    ),
)

sword = item.Item(
    char="/",
    color=(0, 191, 255),
    name="Sword",
    equippable=equippable.Weapon(
        attack=attacks.AttackType(die_sides=8)
    ),
)

leather_armor = item.Item(
   char="[",
   color=(139, 69, 19),
   name="Leather Armor",
   equippable=equippable.Armor(ac_bonus=-1),
)

chain_mail = item.Item(
    char="[",
    color=(139, 69, 19),
    name="Chain Mail",
    equippable=equippable.Armor(ac_bonus=-3),
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
