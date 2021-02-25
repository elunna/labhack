import random

from . import actor, settings
from . import item
from components import consumable, attack_cmp
from components import equippable
from components.ai import HostileAI
from components.attack_cmp import AttackComponent
from components.attack import Attack
from components.attributes import Attributes
from components.energy import EnergyComponent
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
import copy
import tcod


def make(entity_name):
    if entity_name in actor_dict:
        return copy.deepcopy(actor_dict[entity_name])

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


actor_dict = {
    "player": actor.Actor(
        char="@",
        color=(255, 255, 255),
        name="Player",
        ai_cls=HostileAI(),
        equipment=Equipment(),
        fighter=Fighter(hp=30),
        attack_comp=AttackComponent(Attack('punch', [2])),
        attributes=Attributes(base_ac=10, base_strength=5),
        # Original inventory capacity is 26 because we have 26 lowercase letters.
        inventory=Inventory(capacity=26),
        level=Level(level_up_base=20),
        energy=EnergyComponent(threshold=10)
    ),

    "grid bug": actor.Actor(
        char="x",
        color=tcod.purple,
        name="Grid Bug",
        ai_cls=HostileAI(),
        equipment=Equipment(),
        fighter=Fighter(hp=1),
        attack_comp=AttackComponent(Attack('zap', [1])),
        attributes=Attributes(base_ac=1, base_strength=1),
        inventory=Inventory(capacity=0),
        level=Level(xp_given=1),
        energy=EnergyComponent(threshold=10)
    ),

    "storm drone": actor.Actor(
        char="x",
        color=(0, 127, 0),
        name="Storm Drone",
        ai_cls=HostileAI(),
        equipment=Equipment(),
        fighter=Fighter(hp=1),
        attack_comp=AttackComponent(Attack('zap', [5])),
        attributes=Attributes(base_ac=-20, base_strength=10),
        inventory=Inventory(capacity=0),
        level=Level(current_level=4, xp_given=55),
        energy=EnergyComponent(threshold=8)
    ),

    "spider drone": actor.Actor(
        char="s",
        color=tcod.silver,
        name="Spider Drone",
        ai_cls=HostileAI(),
        equipment=Equipment(),
        fighter=Fighter(hp=4),
        attack_comp=AttackComponent(Attack('claw', [3])),
        attributes=Attributes(base_ac=7, base_strength=3),
        inventory=Inventory(capacity=0),
        level=Level(xp_given=35),
        energy=EnergyComponent(threshold=13)
    ),

    "med school dropout": actor.Actor(
        char="@",
        color=tcod.dark_gray,
        name="Med-School Dropout",
        ai_cls=HostileAI(),
        equipment=Equipment(),
        fighter=Fighter(hp=6),
        attack_comp=AttackComponent(Attack('kick', [5])),
        attributes=Attributes(base_ac=6, base_strength=8),
        inventory=Inventory(capacity=0),
        level=Level(xp_given=55),
        energy=EnergyComponent(threshold=12)
    ),

    "cyber cat": actor.Actor(
        char="f",
        color=tcod.dark_blue,
        name="Cyber Cat",
        ai_cls=HostileAI(),
        equipment=Equipment(),
        fighter=Fighter(hp=6),
        attack_comp=AttackComponent(Attack('claw', [6])),
        attributes=Attributes(base_ac=3, base_strength=8),
        inventory=Inventory(capacity=0),
        level=Level(xp_given=55),
        energy=EnergyComponent(threshold=7)
    ),

    "giant leech": actor.Actor(
        char="L",
        color=tcod.light_green,
        name="Giant Leech",
        ai_cls=HostileAI(),
        equipment=Equipment(),
        fighter=Fighter(hp=11),
        attack_comp=AttackComponent(Attack('suck', [6])),
        attributes=Attributes(base_ac=-2, base_strength=10),
        inventory=Inventory(capacity=0),
        level=Level(current_level=4, xp_given=100),
        energy=EnergyComponent(threshold=16)
    ),

    "orc": actor.Actor(
        char="o",
        color=(63, 127, 63),
        name="Orc",
        ai_cls=HostileAI(),
        equipment=Equipment(),
        fighter=Fighter(hp=4),
        attack_comp=AttackComponent(Attack('hit', [3])),
        attributes=Attributes(base_ac=7, base_strength=3),
        inventory=Inventory(capacity=0),
        level=Level(xp_given=35),
        energy=EnergyComponent(threshold=13)
    ),

    "troll": actor.Actor(
        char="T",
        color=(0, 127, 0),
        name="Troll",
        ai_cls=HostileAI(),
        equipment=Equipment(),
        fighter=Fighter(hp=11),
        attack_comp=AttackComponent(Attack('bites', [6])),
        attributes=Attributes(base_ac=-2, base_strength=10),
        inventory=Inventory(capacity=0),
        level=Level(current_level=4, xp_given=100),
        energy=EnergyComponent(threshold=16)
    ),
}

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
        attack_comp=attack_cmp.AttackComponent(Attack('dagger', [3])),
    ),
)

riot_baton = item.Item(
    char="/",
    color=(0, 191, 255),
    name="Riot Baton",
    equippable=equippable.Weapon(
        attack_comp=attack_cmp.AttackComponent(Attack('baton', [8])),
    ),
)

scalpal = item.Item(
    char="/",
    color=(0, 191, 255),
    name="Scalpal",
    equippable=equippable.Weapon(
        attack_comp=attack_cmp.AttackComponent(Attack('scalpal', [4])),
    ),
)

police_baton = item.Item(
    char="/",
    color=(0, 191, 255),
    name="Police Baton",
    equippable=equippable.Weapon(
        attack_comp=attack_cmp.AttackComponent(Attack('club', [4])),
    ),
)

golf_club = item.Item(
    char="/",
    color=(0, 191, 255),
    name="Golf Club",
    equippable=equippable.Weapon(
        attack_comp=attack_cmp.AttackComponent(Attack('club', [5])),
    ),
)

tennis_racket = item.Item(
    char="/",
    color=(0, 191, 255),
    name="Tennis Racket",
    equippable=equippable.Weapon(
        attack_comp=attack_cmp.AttackComponent(Attack('club', [5])),
    ),
)

frying_pan = item.Item(
    char="/",
    color=(0, 191, 255),
    name="Frying Pan",
    equippable=equippable.Weapon(
        attack_comp=attack_cmp.AttackComponent(Attack('club', [7])),
    ),
)

hammer = item.Item(
    char="/",
    color=(0, 191, 255),
    name="Hammer",
    equippable=equippable.Weapon(
        attack_comp=attack_cmp.AttackComponent(Attack('club', [4])),
    ),
)

metal_pipe = item.Item(
    char="/",
    color=(0, 191, 255),
    name="Metal Pipe",
    equippable=equippable.Weapon(
        attack_comp=attack_cmp.AttackComponent(Attack('club', [5])),
    ),
)

big_crowbar = item.Item(
    char="/",
    color=(0, 191, 255),
    name="Big Crowbar",
    equippable=equippable.Weapon(
        attack_comp=attack_cmp.AttackComponent(Attack('club', [6])),
    ),
)

plunger = item.Item(
    char="/",
    color=(0, 191, 255),
    name="Plunger",
    equippable=equippable.Weapon(
        attack_comp=attack_cmp.AttackComponent(Attack('club', [2])),
    ),
)

rebar_pipe = item.Item(
    char="/",
    color=(0, 191, 255),
    name="Rebar Pipe",
    equippable=equippable.Weapon(
        attack_comp=attack_cmp.AttackComponent(Attack('club', [6])),
    ),
)

sledgehammer = item.Item(
    char="/",
    color=(0, 191, 255),
    name="Sledgehammer",
    equippable=equippable.Weapon(
        attack_comp=attack_cmp.AttackComponent(Attack('club', [10])),
    ),
)

wooden_stick = item.Item(
    char="/",
    color=(0, 191, 255),
    name="Wooden Stick",
    equippable=equippable.Weapon(
        attack_comp=attack_cmp.AttackComponent(Attack('club', [4])),
    ),
)

gr_light_saber = item.Item(
    char="/",
    color=(0, 191, 255),
    name="Green lightsaber",
    equippable=equippable.Weapon(
        attack_comp=attack_cmp.AttackComponent(Attack('lightsaber', [3, 9])),
    ),
)

bl_light_saber = item.Item(
    char="/",
    color=(0, 191, 255),
    name="Blue lightsaber",
    equippable=equippable.Weapon(
        attack_comp=attack_cmp.AttackComponent(Attack('lightsaber', [5, 8])),
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
    0: [("grid bug", 40), ("spider drone", 80)],
    3: [("giant leech", 15), ("med school dropout", 25)],
    5: [("giant leech", 30), ("cyber cat", 35)],
    7: [("giant leech", 60), ("cyber cat", 40)],
}


def get_max_value_for_floor(weighted_chances_by_floor, floor):
    current_value = 0

    for floor_minimum, value in weighted_chances_by_floor:
        if floor_minimum > floor:
            break
        else:
            current_value = value

    return current_value


def get_entities_at_random(weighted_chances_by_floor, number_of_entities, floor):
    """ This function goes through they keys (floor numbers) and values (list of
        weighted entities), stopping when the key is higher than the given floor
        number. It sets up a dictionary of the weights for each entity, based on
        which floor the player is currently on. So if we were trying to get the
        weights for floor 6, entity_weighted_chances would look like this:
            { orc: 80, troll: 30 }.

        Then, we get both the keys and values in list format, so that they can
        be passed to random.choices (it accepts choices and weights as lists).
        k represents the number of items that random.choices should pick, so we
        can simply pass the number of entities we’ve decided to generate. Finally,
        we return the list of chosen entities.
    """
    entity_weighted_chances = {}

    for key, values in weighted_chances_by_floor.items():
        if key > floor:
            break
        else:
            for value in values:
                entity = value[0]
                weighted_chance = value[1]

                entity_weighted_chances[entity] = weighted_chance

    entities = list(entity_weighted_chances.keys())
    entity_weighted_chance_values = list(entity_weighted_chances.values())

    chosen_entities = random.choices(
        entities, weights=entity_weighted_chance_values, k=number_of_entities
    )

    return chosen_entities


def place_items(new_room, dungeon, floor_number):
    number_of_items = random.randint(
        0, get_max_value_for_floor(settings.max_items_by_floor, floor_number)
    )

    items = get_entities_at_random(
        item_chances, number_of_items, floor_number
    )

    for entity in items:
        x, y = new_room.random_point_inside()
        # We don't care if they stack on the map
        entity.spawn(dungeon, x, y)


def place_monsters(new_room, dungeon, floor_number):
    number_of_monsters = random.randint(
        0, get_max_value_for_floor(settings.max_monsters_by_floor, floor_number)
    )

    monsters = get_entities_at_random(
        enemy_chances, number_of_monsters, floor_number
    )

    for entity in monsters:
        x = random.randint(new_room.x1 + 1, new_room.x2 - 2)
        y = random.randint(new_room.y1 + 1, new_room.y2 - 2)

        # Don't spawn them on top of each other.
        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            make(entity).spawn(dungeon, x, y)


def populate_map(new_map, current_floor):
    for r in new_map.rooms:
        # Populate the room with monsters and items
        place_monsters(r, new_map, current_floor)
        place_items(r, new_map, current_floor)
