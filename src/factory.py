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
        return copy.deepcopy(riot_baton)
    elif entity_name == 'leather armor':
        return copy.deepcopy(leather_vest)
    elif entity_name == 'chain mail':
        return copy.deepcopy(bulletproof_vest)
    elif entity_name == 'health potion':
        return copy.deepcopy(health_potion)
    elif entity_name == 'lightning scroll':
        return copy.deepcopy(lightning_scroll)
    return None


player = actor.Actor(
    char="@",
    color=(255, 255, 255),
    name="Player",
    ai_cls=HostileAI(),
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
    ai_cls=HostileAI(),
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
    ai_cls=HostileAI(),
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
    color=tcod.silver,
    name="Spider Drone",
    ai_cls=HostileAI(),
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
    ai_cls=HostileAI(),
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
    ai_cls=HostileAI(),
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
    ai_cls=HostileAI(),
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
    ai_cls=HostileAI(),
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
    ai_cls=HostileAI(),
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

# WEAPONS

dagger = item.Item(
    char="/",
    color=(0, 191, 255),
    name="Dagger",
    equippable=equippable.Weapon(
        attack=attacks.AttackComponent(Attack('dagger', [3])),
    ),
)

riot_baton = item.Item(
    char="/",
    color=(0, 191, 255),
    name="Riot Baton",
    equippable=equippable.Weapon(
        attack=attacks.AttackComponent(Attack('baton', [8])),
    ),
)

scalpal = item.Item(
    char="/",
    color=(0, 191, 255),
    name="Scalpal",
    equippable=equippable.Weapon(
        attack=attacks.AttackComponent(Attack('scalpal', [4])),
    ),
)

police_baton = item.Item(
    char="/",
    color=(0, 191, 255),
    name="Police Baton",
    equippable=equippable.Weapon(
        attack=attacks.AttackComponent(Attack('club', [4])),
    ),
)

golf_club = item.Item(
    char="/",
    color=(0, 191, 255),
    name="Golf Club",
    equippable=equippable.Weapon(
        attack=attacks.AttackComponent(Attack('club', [5])),
    ),
)


tennis_racket = item.Item(
    char="/",
    color=(0, 191, 255),
    name="Tennis Racket",
    equippable=equippable.Weapon(
        attack=attacks.AttackComponent(Attack('club', [5])),
    ),
)

frying_pan = item.Item(
    char="/",
    color=(0, 191, 255),
    name="Frying Pan",
    equippable=equippable.Weapon(
        attack=attacks.AttackComponent(Attack('club', [7])),
    ),
)


hammer = item.Item(
    char="/",
    color=(0, 191, 255),
    name="Hammer",
    equippable=equippable.Weapon(
        attack=attacks.AttackComponent(Attack('club', [4])),
    ),
)

metal_pipe = item.Item(
    char="/",
    color=(0, 191, 255),
    name="Metal Pipe",
    equippable=equippable.Weapon(
        attack=attacks.AttackComponent(Attack('club', [5])),
    ),
)

big_crowbar = item.Item(
    char="/",
    color=(0, 191, 255),
    name="Big Crowbar",
    equippable=equippable.Weapon(
        attack=attacks.AttackComponent(Attack('club', [6])),
    ),
)

plunger = item.Item(
    char="/",
    color=(0, 191, 255),
    name="Plunger",
    equippable=equippable.Weapon(
        attack=attacks.AttackComponent(Attack('club', [2])),
    ),
)

rebar_pipe = item.Item(
    char="/",
    color=(0, 191, 255),
    name="Rebar Pipe",
    equippable=equippable.Weapon(
        attack=attacks.AttackComponent(Attack('club', [6])),
    ),
)

sledgehammer = item.Item(
    char="/",
    color=(0, 191, 255),
    name="Sledgehammer",
    equippable=equippable.Weapon(
        attack=attacks.AttackComponent(Attack('club', [10])),
    ),
)

wooden_stick = item.Item(
    char="/",
    color=(0, 191, 255),
    name="Wooden Stick",
    equippable=equippable.Weapon(
        attack=attacks.AttackComponent(Attack('club', [4])),
    ),
)


gr_light_saber = item.Item(
    char="/",
    color=(0, 191, 255),
    name="Green lightsaber",
    equippable=equippable.Weapon(
        attack=attacks.AttackComponent(Attack('lightsaber', [3, 9])),
    ),
)

bl_light_saber = item.Item(
    char="/",
    color=(0, 191, 255),
    name="Blue lightsaber",
    equippable=equippable.Weapon(
        attack=attacks.AttackComponent(Attack('lightsaber', [5, 8])),
    ),
)

# ARMOR


leather_vest = item.Item(
   char="[",
   color=tcod.dark_amber,
   name="Leather Vest",
   equippable=equippable.Armor(ac_bonus=-1),
)

bulletproof_vest = item.Item(
    char="[",
    color=tcod.turquoise,
    name="Bulletproof Vest",
    equippable=equippable.Armor(ac_bonus=-3),
)

chain_vest = item.Item(
    char="[",
    color=tcod.dark_gray,
    name="Chain Vest",
    equippable=equippable.Armor(ac_bonus=-3),
)

chest_guard = item.Item(
    char="[",
    color=tcod.cyan,
    name="Chest Guard",
    equippable=equippable.Armor(ac_bonus=-2),
)

tactical_vest = item.Item(
    char="[",
    color=tcod.green,
    name="Tactical Vest",
    equippable=equippable.Armor(ac_bonus=-2),
)

riot_armor = item.Item(
    char="[",
    color=tcod.dark_blue,
    name="Riot Armor",
    equippable=equippable.Armor(ac_bonus=-4),
)

power_armor = item.Item(
    char="[",
    color=tcod.flame,
    name="Power Armor",
    equippable=equippable.Armor(ac_bonus=-5),
)

fedora = item.Item(
    char="[",
    color=tcod.dark_crimson,
    name="Fedora",
    equippable=equippable.Helmet(ac_bonus=0),
)

bandana = item.Item(
    char="[",
    color=tcod.light_green,
    name="Bandana",
    equippable=equippable.Helmet(ac_bonus=0),
)

helmet = item.Item(
    char="[",
    color=tcod.orange,
    name="Helmet",
    equippable=equippable.Helmet(ac_bonus=-1),
)

visored_helmet = item.Item(
    char="[",
    color=tcod.orange,
    name="Visored Helmet",
    equippable=equippable.Helmet(ac_bonus=-1),
)

riot_helmet = item.Item(
    char="[",
    color=tcod.dark_blue,
    name="Riot Helmet",
    equippable=equippable.Helmet(ac_bonus=-2),
)

ballistic_helmet = item.Item(
    char="[",
    color=tcod.turquoise,
    name="Ballistic Helmet",
    equippable=equippable.Helmet(ac_bonus=-3),
)

power_helmet = item.Item(
    char="[",
    color=tcod.flame,
    name="Power Helmet",
    equippable=equippable.Helmet(ac_bonus=-4),
)

rubber_gloves = item.Item(
    char="[",
    color=tcod.orange,
    name="Rubber Gloves",
    equippable=equippable.Gloves(ac_bonus=0),
)

leather_gloves = item.Item(
    char="[",
    color=tcod.dark_amber,
    name="Leather Gloves",
    equippable=equippable.Gloves(ac_bonus=-1),
)

riot_gloves = item.Item(
    char="[",
    color=tcod.dark_blue,
    name="Riot Gloves",
    equippable=equippable.Gloves(ac_bonus=-2),
)

tactical_boots = item.Item(
    char="[",
    color=tcod.green,
    name="Tactical Boots",
    equippable=equippable.Boots(ac_bonus=-1),
)

combat_boots = item.Item(
    char="[",
    color=tcod.dark_green,
    name="Combat Boots",
    equippable=equippable.Boots(ac_bonus=-2),
)

power_boots = item.Item(
    char="[",
    color=tcod.flame,
    name="Power Boots",
    equippable=equippable.Boots(ac_bonus=-3),
)

garbage_lid = item.Item(
    char="[",
    color=tcod.light_gray,
    name="Garbage Can Lid",
    equippable=equippable.Shield(ac_bonus=-1),
)

riot_shield = item.Item(
    char="[",
    color=tcod.dark_blue,
    name="Riot Shield",
    equippable=equippable.Shield(ac_bonus=-2),
)

ballistic_shield = item.Item(
    char="[",
    color=tcod.turquoise,
    name="Ballistic Shield",
    equippable=equippable.Shield(ac_bonus=-3),
)

leather_belt = item.Item(
    char="[",
    color=tcod.dark_amber,
    name="Leather Belt",
    equippable=equippable.Belt(ac_bonus=-1),
)

tactical_belt = item.Item(
    char="[",
    color=tcod.green,
    name="Tactical Belt",
    equippable=equippable.Belt(ac_bonus=-2),
)

power_belt = item.Item(
    char="[",
    color=tcod.flame,
    name="Power Belt",
    equippable=equippable.Belt(ac_bonus=-3),
)

leather_wrists = item.Item(
    char="[",
    color=tcod.dark_amber,
    name="Leather Wrists",
    equippable=equippable.Arms(ac_bonus=-1),
)

elbow_pads = item.Item(
    char="[",
    color=tcod.orange,
    name="Elbow Pads",
    equippable=equippable.Arms(ac_bonus=-1),
)

forearm_guards = item.Item(
    char="[",
    color=tcod.dark_gray,
    name="Forearm Guards",
    equippable=equippable.Arms(ac_bonus=-2),
)

power_wrists = item.Item(
    char="[",
    color=tcod.flame,
    name="Power Wrists",
    equippable=equippable.Arms(ac_bonus=-3),
)


item_chances = {
    # keys in the dictionary represent the floor number,
    # and the value is a list of tuples.
    0: [
        (health_potion, 200),
        (confusion_scroll, 45),
        (lightning_scroll, 35),
        (fireball_scroll, 35),

        (dagger, 3),
        (riot_baton, 3),
        (scalpal, 3),
        (police_baton, 1),
        (golf_club, 2),
        (hammer, 3),
        (metal_pipe, 3),
        (big_crowbar, 3),
        (plunger, 3),
        (rebar_pipe, 3),
        (sledgehammer, 1),
        (wooden_stick, 3),
        (gr_light_saber, 1),
        (bl_light_saber, 1),
        (tennis_racket, 2),
        (frying_pan, 2),

        (leather_vest, 5),      # AC1
        (chest_guard, 5),       # AC2
        (tactical_vest, 5),     # AC2
        (bulletproof_vest, 3),  # AC3
        (chain_vest, 2),        # AC3
        (riot_armor, 2),        # AC4
        (power_armor, 1),       # AC5
        (fedora, 1),            # AC0
        (bandana, 2),           # AC0
        (helmet, 5),            # AC1
        (visored_helmet, 3),    # AC1
        (riot_helmet, 5),       # AC2
        (ballistic_helmet, 2),  # AC3
        (power_helmet, 1),      # AC4
        (rubber_gloves, 3),     # AC0
        (leather_gloves, 6),    # AC1
        (riot_gloves, 1),       # AC2
        (tactical_boots, 5),    # AC1
        (combat_boots, 3),      # AC2
        (power_boots, 1),       # AC3
        (garbage_lid, 5),       # AC1
        (riot_shield, 6),       # AC2
        (ballistic_shield, 1),  # AC3
        (leather_belt, 6),      # AC1
        (tactical_belt, 3),     # AC2
        (power_belt, 1),        # AC3
        (elbow_pads, 6),        # AC1
        (leather_wrists, 5),    # AC1
        (forearm_guards, 6),    # AC2
        (power_wrists, 1),      # AC3
    ],
}

enemy_chances = {
    0: [(grid_bug, 40), (spider_drone, 80)],
    3: [(giant_leech, 15), (med_school_dropout, 25)],
    5: [(giant_leech, 30), (cyber_cat, 35)],
    7: [(giant_leech, 60), (cyber_cat, 40)],
}
