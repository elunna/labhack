""" Database of entities for the project. """
import tcod

from components import consumable, equippable, attack_cmp
from components.ai import HostileAI
from components.attack import Attack
from components.attack_cmp import AttackComponent
from components.attributes import Attributes
from components.energy import EnergyComponent
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level


actor_dict = {
    "player": {
        "char": "@",
        "color": (255, 255, 255),
        "ai_cls": HostileAI(),
        "equipment": Equipment(),
        "fighter": Fighter(hp=30),
        "attack_comp": AttackComponent(Attack('punch', [2])),
        "attributes": Attributes(base_ac=10, base_strength=5),
        # Original inventory capacity is 26 because we have 26 lowercase letters.
        "inventory": Inventory(capacity=26),
        "level": Level(level_up_base=20),
        "energy": EnergyComponent(threshold=10)
    },

    "grid bug": {
        "char": "x",
        "color": tcod.purple,
        "ai_cls": HostileAI(),
        "equipment": Equipment(),
        "fighter": Fighter(hp=1),
        "attack_comp": AttackComponent(Attack('zap', [1])),
        "attributes": Attributes(base_ac=1, base_strength=1),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=1),
        "energy": EnergyComponent(threshold=10)
    },

    "storm drone": {
        "char": "x",
        "color": (0, 127, 0),
        "ai_cls": HostileAI(),
        "equipment": Equipment(),
        "fighter": Fighter(hp=1),
        "attack_comp": AttackComponent(Attack('zap', [5])),
        "attributes": Attributes(base_ac=-20, base_strength=10),
        "inventory": Inventory(capacity=0),
        "level": Level(current_level=4, xp_given=55),
        "energy": EnergyComponent(threshold=8)
    },

    "spider drone": {
        "char": "s",
        "color": tcod.silver,
        "ai_cls": HostileAI(),
        "equipment": Equipment(),
        "fighter": Fighter(hp=4),
        "attack_comp": AttackComponent(Attack('claw', [3])),
        "attributes": Attributes(base_ac=7, base_strength=3),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=35),
        "energy": EnergyComponent(threshold=13)
    },

    "med school dropout": {
        "char": "@",
        "color": tcod.dark_gray,
        "ai_cls": HostileAI(),
        "equipment": Equipment(),
        "fighter": Fighter(hp=6),
        "attack_comp": AttackComponent(Attack('kick', [5])),
        "attributes": Attributes(base_ac=6, base_strength=8),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=55),
        "energy": EnergyComponent(threshold=12)
    },

    "henchman": {
        "char": "@",
        "color": tcod.dark_gray,
        "ai_cls": HostileAI(),
        "equipment": Equipment(),
        "fighter": Fighter(hp=6),
        "attack_comp": AttackComponent(Attack('punch', [5])),
        "attributes": Attributes(base_ac=6, base_strength=8),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=55),
        "energy": EnergyComponent(threshold=12)
    },

    "cyber cat": {
        "char": "f",
        "color": tcod.dark_blue,
        "ai_cls": HostileAI(),
        "equipment": Equipment(),
        "fighter": Fighter(hp=6),
        "attack_comp": AttackComponent(Attack('claw', [6])),
        "attributes": Attributes(base_ac=3, base_strength=8),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=55),
        "energy": EnergyComponent(threshold=7)
    },

    "giant leech": {
        "char": "L",
        "color": tcod.light_green,
        "ai_cls": HostileAI(),
        "equipment": Equipment(),
        "fighter": Fighter(hp=11),
        "attack_comp": AttackComponent(Attack('suck', [6])),
        "attributes": Attributes(base_ac=-2, base_strength=10),
        "inventory": Inventory(capacity=0),
        "level": Level(current_level=4, xp_given=100),
        "energy": EnergyComponent(threshold=16),
    },
}


item_dict = {
    "health potion": {
        "char": "!",
        "color": (127, 0, 255),
        "consumable": consumable.HealConsumable(amount=5),
    },

    "lightning scroll": {
        "char": "~",
        "color": (255, 255, 0),
        "consumable": consumable.LightningDamageConsumable(damage=20, maximum_range=5),
    },

    "confusion scroll": {
        "char": "~",
        "color": (207, 63, 255),
        "consumable": consumable.ConfusionConsumable(number_of_turns=10),
    },

    "fireball scroll": {
        "char": "~",
        "color": (255, 0, 0),
        "consumable": consumable.FireballDamageConsumable(damage=12, radius=3),
    },

    # WEAPONS

    "dagger": {
        "char": "/",
        "color": (0, 191, 255),
        "equippable": equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('dagger', [3])),
        ),
    },

    "riot baton": {
        "char": "/",
        "color": (0, 191, 255),
        "equippable": equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('baton', [8])),
        ),
    },

    "scalpal": {
        "char": "/",
        "color": (0, 191, 255),
        "equippable": equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('scalpal', [4])),
        ),
    },

    "police baton": {
        "char": "/",
        "color": (0, 191, 255),
        "equippable": equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('club', [4])),
        ),
    },

    "golf club": {
        "char": "/",
        "color": (0, 191, 255),
        "equippable": equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('club', [5])),
        ),
    },

    "tennis racket": {
        "char": "/",
        "color": (0, 191, 255),
        "equippable": equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('club', [5])),
        ),
    },

    "frying pan": {
        "char": "/",
        "color": (0, 191, 255),
        "equippable": equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('club', [7])),
        ),
    },

    "hammer": {
        "char": "/",
        "color": (0, 191, 255),
        "equippable": equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('club', [4])),
        ),
    },

    "metal pipe": {
        "char": "/",
        "color": (0, 191, 255),
        "equippable": equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('club', [5])),
        ),
    },

    "big crowbar": {
        "char": "/",
        "color": (0, 191, 255),
        "equippable": equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('club', [6])),
        ),
    },

    "plunger": {
        "char": "/",
        "color": (0, 191, 255),
        "equippable": equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('club', [2])),
        ),
    },

    "rebar pipe": {
        "char": "/",
        "color": (0, 191, 255),
        "equippable": equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('club', [6])),
        ),
    },

    "sledgehammer": {
        "char": "/",
        "color": (0, 191, 255),
        "equippable": equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('club', [10])),
        ),
    },

    "wooden stick": {
        "char": "/",
        "color": (0, 191, 255),
        "equippable": equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('club', [4])),
        ),
    },

    "green lightsaber": {
        "char": "/",
        "color": (0, 191, 255),
        "equippable": equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('lightsaber', [3, 9])),
        ),
    },

    "blue lightsaber": {
        "char": "/",
        "color": (0, 191, 255),
        "equippable": equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('lightsaber', [5, 8])),
        ),
    },

    # ARMOR

    "leather vest": {
       "char": "[",
       "color": tcod.dark_amber,
       "equippable": equippable.Armor(ac_bonus=-1),
    },

    "bulletproof vest": {
        "char": "[",
        "color": tcod.turquoise,
        "equippable": equippable.Armor(ac_bonus=-3),
    },

    "chain vest": {
        "char": "[",
        "color": tcod.dark_gray,
        "equippable": equippable.Armor(ac_bonus=-3),
    },

    "chest guard": {
        "char": "[",
        "color": tcod.cyan,
        "equippable": equippable.Armor(ac_bonus=-2),
    },

    "tactical vest": {
        "char": "[",
        "color": tcod.green,
        "equippable": equippable.Armor(ac_bonus=-2),
    },

    "riot armor": {
        "char": "[",
        "color": tcod.dark_blue,
        "equippable": equippable.Armor(ac_bonus=-4),
    },

    "power armor": {
        "char": "[",
        "color": tcod.flame,
        "equippable": equippable.Armor(ac_bonus=-5),
    },

    "fedora": {
        "char": "[",
        "color": tcod.dark_crimson,
        "equippable": equippable.Helmet(ac_bonus=0),
    },

    "bandana": {
        "char": "[",
        "color": tcod.light_green,
        "equippable": equippable.Helmet(ac_bonus=0),
    },

    "helmet": {
        "char": "[",
        "color": tcod.orange,
        "equippable": equippable.Helmet(ac_bonus=-1),
    },

    "visored helmet": {
        "char": "[",
        "color": tcod.orange,
        "equippable": equippable.Helmet(ac_bonus=-1),
    },

    "riot helmet": {
        "char": "[",
        "color": tcod.dark_blue,
        "equippable": equippable.Helmet(ac_bonus=-2),
    },

    "ballistic helmet": {
        "char": "[",
        "color": tcod.turquoise,
        "equippable": equippable.Helmet(ac_bonus=-3),
    },

    "power helmet": {
        "char": "[",
        "color": tcod.flame,
        "equippable": equippable.Helmet(ac_bonus=-4),
    },

    "rubber gloves": {
        "char": "[",
        "color": tcod.orange,
        "equippable": equippable.Gloves(ac_bonus=0),
    },

    "leather gloves": {
        "char": "[",
        "color": tcod.dark_amber,
        "equippable": equippable.Gloves(ac_bonus=-1),
    },

    "riot gloves": {
        "char": "[",
        "color": tcod.dark_blue,
        "equippable": equippable.Gloves(ac_bonus=-2),
    },

    "tactical boots": {
        "char": "[",
        "color": tcod.green,
        "equippable": equippable.Boots(ac_bonus=-1),
    },

    "combat boots": {
        "char": "[",
        "color": tcod.dark_green,
        "equippable": equippable.Boots(ac_bonus=-2),
    },

    "power boots": {
        "char": "[",
        "color": tcod.flame,
        "equippable": equippable.Boots(ac_bonus=-3),
    },

    "garbage can lid": {
        "char": "[",
        "color": tcod.light_gray,
        "equippable": equippable.Shield(ac_bonus=-1),
    },

    "riot shield": {
        "char": "[",
        "color": tcod.dark_blue,
        "equippable": equippable.Shield(ac_bonus=-2),
    },

    "ballistic shield": {
        "char": "[",
        "color": tcod.turquoise,
        "equippable": equippable.Shield(ac_bonus=-3),
    },

    "leather belt": {
        "char": "[",
        "color": tcod.dark_amber,
        "equippable": equippable.Belt(ac_bonus=-1),
    },

    "tactical belt": {
        "char": "[",
        "color": tcod.green,
        "equippable": equippable.Belt(ac_bonus=-2),
    },

    "power belt": {
        "char": "[",
        "color": tcod.flame,
        "equippable": equippable.Belt(ac_bonus=-3),
    },

    "leather wrists": {
        "char": "[",
        "color": tcod.dark_amber,
        "equippable": equippable.Arms(ac_bonus=-1),
    },

    "elbow pads": {
        "char": "[",
        "color": tcod.orange,
        "equippable": equippable.Arms(ac_bonus=-1),
    },

    "forearm guards": {
        "char": "[",
        "color": tcod.dark_gray,
        "equippable": equippable.Arms(ac_bonus=-2),
    },

    "power wrists": {
        "char": "[",
        "color": tcod.flame,
        "equippable": equippable.Arms(ac_bonus=-3),
    },
}

item_chances = {
    # keys in the dictionary represent the floor number,
    # and the value is a list of tuples.
    0: [
        ("health potion", 200),
        ("confusion scroll", 45),
        ("lightning scroll", 35),
        ("fireball scroll", 35),

        ("dagger", 3),
        ("riot baton", 3),
        ("scalpal", 3),
        ("police baton", 1),
        ("golf club", 2),
        ("hammer", 3),
        ("metal pipe", 3),
        ("big crowbar", 3),
        ("plunger", 3),
        ("rebar pipe", 3),
        ("sledgehammer", 1),
        ("wooden stick", 3),
        ("green lightsaber", 1),
        ("blue lightsaber", 1),
        ("tennis racket", 2),
        ("frying pan", 2),

        ("leather vest", 5),      # AC1
        ("chest guard", 5),       # AC2
        ("tactical vest", 5),     # AC2
        ("bulletproof vest", 3),  # AC3
        ("chain vest", 2),        # AC3
        ("riot armor", 2),        # AC4
        ("power armor", 1),       # AC5
        ("fedora", 1),            # AC0
        ("bandana", 2),           # AC0
        ("helmet", 5),            # AC1
        ("visored helmet", 3),    # AC1
        ("riot helmet", 5),       # AC2
        ("ballistic helmet", 2),  # AC3
        ("power helmet", 1),      # AC4
        ("rubber gloves", 3),     # AC0
        ("leather gloves", 6),    # AC1
        ("riot gloves", 1),       # AC2
        ("tactical boots", 5),    # AC1
        ("combat boots", 3),      # AC2
        ("power boots", 1),       # AC3
        ("garbage can lid", 5),   # AC1
        ("riot shield", 6),       # AC2
        ("ballistic shield", 1),  # AC3
        ("leather belt", 6),      # AC1
        ("tactical belt", 3),     # AC2
        ("power belt", 1),        # AC3
        ("elbow pads", 6),        # AC1
        ("leather wrists", 5),    # AC1
        ("forearm guards", 6),    # AC2
        ("power wrists", 1),      # AC3
    ],
}

enemy_chances = {
    0: [("grid bug", 40), ("spider drone", 80)],
    3: [("giant leech", 15), ("med school dropout", 25)],
    5: [("giant leech", 30), ("cyber cat", 35)],
    7: [("giant leech", 60), ("cyber cat", 40)],
}
