import tcod

from components import consumable, attacks
from components import equippable
from components.ai import HostileAI
from components.attacks import AttackComponent, Attack
from components.energy import EnergyMeter
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from components.attributes import Attributes
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
    fighter=Fighter(hp=30),
    attacks=AttackComponent(Attack('punch', [2])),
    attributes=Attributes(base_ac=10, base_strength=5),
    # Original inventory capacity is 26 because we have 26 lowercase letters.
    inventory=Inventory(capacity=26),
    level=Level(level_up_base=20),
    energymeter=EnergyMeter(threshold=10)
)

grid_bug = actor.Actor(
    char="x",
    color=tcod.purple,
    name="Grid Bug",
    ai_cls=HostileAI,
    equipment=Equipment(),
    fighter=Fighter(hp=1),
    attacks=AttackComponent(Attack('zap', [1])),
    attributes=Attributes(base_ac=1, base_strength=1),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=1),
    energymeter=EnergyMeter(threshold=10)
)


storm_drone = actor.Actor(
    char="x",
    color=(0, 127, 0),
    name="Storm Drone",
    ai_cls=HostileAI,
    equipment=Equipment(),
    fighter=Fighter(hp=1),
    attacks=AttackComponent(Attack('zap', [5])),
    attributes=Attributes(base_ac=-20, base_strength=10),
    inventory=Inventory(capacity=0),
    level=Level(current_level=4, xp_given=55),
    energymeter=EnergyMeter(threshold=8)
)


spider_drone = actor.Actor(
    char="s",
    color=tcod.dark_gray,
    name="Spider Drone",
    ai_cls=HostileAI,
    equipment=Equipment(),
    fighter=Fighter(hp=4),
    attacks=AttackComponent(Attack('claw', [3])),
    attributes=Attributes(base_ac=7, base_strength=3),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
    energymeter=EnergyMeter(threshold=13)
)

med_school_dropout = actor.Actor(
    char="@",
    color=tcod.dark_gray,
    name="Med-School Dropout",
    ai_cls=HostileAI,
    equipment=Equipment(),
    fighter=Fighter(hp=6),
    attacks=AttackComponent(Attack('kick', [5])),
    attributes=Attributes(base_ac=6, base_strength=8),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=55),
    energymeter=EnergyMeter(threshold=12)
)

cyber_cat = actor.Actor(
    char="f",
    color=tcod.dark_blue,
    name="Cyber Cat",
    ai_cls=HostileAI,
    equipment=Equipment(),
    fighter=Fighter(hp=6),
    attacks=AttackComponent(Attack('claw', [6])),
    attributes=Attributes(base_ac=3, base_strength=8),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=55),
    energymeter=EnergyMeter(threshold=7)
)

giant_leech = actor.Actor(
    char="L",
    color=tcod.light_green,
    name="Giant Leech",
    ai_cls=HostileAI,
    equipment=Equipment(),
    fighter=Fighter(hp=11),
    attacks=AttackComponent(Attack('suck', [6])),
    attributes=Attributes(base_ac=-2, base_strength=10),
    inventory=Inventory(capacity=0),
    level=Level(current_level=4, xp_given=100),
    energymeter=EnergyMeter(threshold=16)
)


orc = actor.Actor(
    char="o",
    color=(63, 127, 63),
    name="Orc",
    ai_cls=HostileAI,
    equipment=Equipment(),
    fighter=Fighter(hp=4),
    attacks=AttackComponent(Attack('hit', [3])),
    attributes=Attributes(base_ac=7, base_strength=3),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
    energymeter=EnergyMeter(threshold=13)
)

troll = actor.Actor(
    char="T",
    color=(0, 127, 0),
    name="Troll",
    ai_cls=HostileAI,
    equipment=Equipment(),
    fighter=Fighter(hp=11),
    attacks=AttackComponent(Attack('bites', [6])),
    attributes=Attributes(base_ac=-2, base_strength=10),
    inventory=Inventory(capacity=0),
    level=Level(current_level=4, xp_given=100),
    energymeter=EnergyMeter(threshold=16)
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
        attack=attacks.AttackComponent(Attack('dagger', [3])),
    ),
)

sword = item.Item(
    char="/",
    color=(0, 191, 255),
    name="Sword",
    equippable=equippable.Weapon(
        attack=attacks.AttackComponent(Attack('sword', [8])),
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
    0: [
        (health_potion, 35),
        (confusion_scroll, 10),
        (lightning_scroll, 25),
        (fireball_scroll, 25),
        (sword, 5),
        (chain_mail, 6),
    ],
}

enemy_chances = {
    0: [(grid_bug, 40), (spider_drone, 80)],
    3: [(giant_leech, 15), (med_school_dropout, 25)],
    5: [(giant_leech, 30), (cyber_cat, 35)],
    7: [(giant_leech, 60), (cyber_cat, 40)],
}
