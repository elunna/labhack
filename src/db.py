""" Database of entities for the project. """
import tcod

from components import consumable, equippable, attack_cmp
from components.ai import HostileAI, GridAI
from components.attack import Attack
from components.attack_cmp import AttackComponent
from components.attributes import Attributes
from components.energy import EnergyComponent
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import PlayerInventory
from components.item_comp import ItemComponent
from components.level import Level
from components.regeneration import Regeneration
from components.stackable import StackableComponent
from src.entity import Entity
from src.renderorder import RenderOrder

actor_dict = {
    "player": {
        "char": "@",
        "color": (255, 255, 255),
        "ai_cls": None,
        "equipment": Equipment(),
        "fighter": Fighter(max_hp=30, base_ac=10),
        "attack_comp": AttackComponent(Attack('punch', [2])),
        "attributes": Attributes(base_strength=5),
        # Original inventory capacity is 26 because we have 26 lowercase letters.
        "inventory": PlayerInventory(capacity=52),
        "level": Level(level_up_base=20, difficulty=0),
        "energy": EnergyComponent(threshold=10),
        "regeneration": Regeneration(),
    },

    "grid bug": {
        "char": "x",
        "color": tcod.purple,
        "ai_cls": GridAI(),
        "fighter": Fighter(max_hp=1, base_ac=10),
        "attack_comp": AttackComponent(Attack('zap', [1])),
        "level": Level(xp_given=1, difficulty=0),
        "energy": EnergyComponent(threshold=10)
    },

    "larva": {
        "char": "w",
        "color": tcod.white,
        "ai_cls": HostileAI(),
        "fighter": Fighter(max_hp=1, base_ac=9),
        "attack_comp": AttackComponent(Attack('bite', [2])),
        "level": Level(xp_given=8, difficulty=2),
        "energy": EnergyComponent(threshold=13)
    },

    "grasshopper": {
        "char": "a",
        "color": tcod.green,
        "ai_cls": HostileAI(),
        "fighter": Fighter(max_hp=2, base_ac=7),
        "attack_comp": AttackComponent(Attack('bite', [1])),
        "level": Level(xp_given=8, difficulty=1),
        "energy": EnergyComponent(threshold=7)
    },

    "maggot": {
        "char": "w",
        "color": tcod.white,
        "ai_cls": HostileAI(),
        "fighter": Fighter(max_hp=1, base_ac=9),
        "attack_comp": AttackComponent(Attack('bite', [3])),
        "level": Level(xp_given=17, difficulty=3),
        "energy": EnergyComponent(threshold=13)
    },

    "centipede": {
        "char": "s",
        "color": tcod.yellow,
        "ai_cls": HostileAI(),
        "fighter": Fighter(max_hp=1, base_ac=3),
        "attack_comp": AttackComponent(Attack('bite', [3])),  # Poisonous
        "level": Level(xp_given=19, difficulty=4),
        "energy": EnergyComponent(threshold=15)
    },

    "mouse": {
        "char": "r",
        "color": tcod.white,
        "ai_cls": HostileAI(),
        "fighter": Fighter(max_hp=2, base_ac=9),
        "attack_comp": AttackComponent(Attack('bite', [2])),
        "level": Level(xp_given=1, difficulty=1),
        "energy": EnergyComponent(threshold=9)
    },

    "black rat": {
        "char": "r",
        "color": tcod.dark_gray,
        "ai_cls": HostileAI(),
        "fighter": Fighter(max_hp=2, base_ac=10),
        "attack_comp": AttackComponent(Attack('bite', [3])),
        "level": Level(xp_given=1, difficulty=1),
        "energy": EnergyComponent(threshold=9)
    },

    "guinea pig": {
        "char": "r",
        "color": tcod.amber,
        "ai_cls": HostileAI(),
        "fighter": Fighter(max_hp=4, base_ac=9),
        "attack_comp": AttackComponent(Attack('bite', [4])),
        "level": Level(xp_given=8, difficulty=2),
        "energy": EnergyComponent(threshold=9)
    },

    "monkey": {
        "char": "Y",
        "color": tcod.gray,
        "ai_cls": HostileAI(),
        "fighter": Fighter(max_hp=2, base_ac=6),
        "attack_comp": AttackComponent(
            Attack('claw', [1]),
            Attack('bite', [3]),
        ),
        "level": Level(xp_given=1, difficulty=4),
        "energy": EnergyComponent(threshold=10)
    },

    "chimpanzee": {
        "char": "Y",
        "color": tcod.light_gray,
        "ai_cls": HostileAI(),
        "fighter": Fighter(max_hp=12, base_ac=4),
        "attack_comp": AttackComponent(
            Attack('claw', [2]),
            Attack('bite', [5]),
        ),
        "level": Level(xp_given=1, difficulty=6),
        "energy": EnergyComponent(threshold=7)
    },

    "chicken": {
        "char": "c",
        "color": tcod.white,
        "ai_cls": HostileAI(),
        "fighter": Fighter(max_hp=7, base_ac=8),
        "attack_comp": AttackComponent(Attack('bite', [3])),
        "level": Level(xp_given=20, difficulty=3),
        "energy": EnergyComponent(threshold=7)
    },

    "lamb": {
        "char": "q",
        "color": tcod.white,
        "ai_cls": HostileAI(),
        "fighter": Fighter(max_hp=12, base_ac=10),
        "attack_comp": AttackComponent(
            Attack('head butt', [2]),
            Attack('kick', [2]),
        ),
        "level": Level(xp_given=8, difficulty=3),
        "energy": EnergyComponent(threshold=8)
    },

    "sheep": {
        "char": "q",
        "color": tcod.white,
        "ai_cls": HostileAI(),
        "fighter": Fighter(max_hp=12, base_ac=10),
        "attack_comp": AttackComponent(
            Attack('head butt', [4]),
            Attack('kick', [3]),
        ),
        "level": Level(xp_given=28, difficulty=5),
        "energy": EnergyComponent(threshold=10)
    },

    "bat": {
        "char": "B",
        "color": tcod.orange,
        "ai_cls": HostileAI(),
        "fighter": Fighter(max_hp=4, base_ac=8),
        "attack_comp": AttackComponent(Attack('bite', [4])),
        "level": Level(xp_given=6, difficulty=3),
        "energy": EnergyComponent(threshold=4)
    },

    "spider drone": {
        "char": "s",
        "color": tcod.silver,
        "ai_cls": HostileAI(),
        "fighter": Fighter(max_hp=4, base_ac=7),
        "attack_comp": AttackComponent(Attack('claw', [3])),
        "level": Level(xp_given=35, difficulty=3),
        "energy": EnergyComponent(threshold=13)
    },

    "med school dropout": {
        "char": "@",
        "color": tcod.dark_gray,
        "ai_cls": HostileAI(),
        "fighter": Fighter(max_hp=6, base_ac=6),
        "attack_comp": AttackComponent(Attack('kick', [5])),
        "level": Level(xp_given=55, difficulty=3),
        "energy": EnergyComponent(threshold=12)
    },

    "giant leech": {
        "char": "L",
        "color": tcod.light_green,
        "ai_cls": HostileAI(),
        "fighter": Fighter(max_hp=11, base_ac=-2),
        "attack_comp": AttackComponent(Attack('suck', [6])),
        "level": Level(current_level=4, xp_given=100, difficulty=4),
        "energy": EnergyComponent(threshold=16),
    },

    "henchman": {
        "char": "@",
        "color": tcod.dark_gray,
        "ai_cls": HostileAI(),
        "fighter": Fighter(max_hp=6, base_ac=6),
        "attack_comp": AttackComponent(Attack('punch', [5])),
        "level": Level(xp_given=55, difficulty=4),
        "energy": EnergyComponent(threshold=12)
    },

    "cyber cat": {
        "char": "f",
        "color": tcod.dark_blue,
        "ai_cls": HostileAI(),
        "fighter": Fighter(max_hp=6, base_ac=3),
        "attack_comp": AttackComponent(Attack('claw', [6])),
        "level": Level(xp_given=55, difficulty=6),
        "energy": EnergyComponent(threshold=7)
    },

    "storm drone": {
        "char": "x",
        "color": (0, 127, 0),
        "ai_cls": HostileAI(),
        "fighter": Fighter(max_hp=1, base_ac=-20),
        "attack_comp": AttackComponent(Attack('zap', [5])),
        "level": Level(current_level=4, xp_given=55, difficulty=20),
        "energy": EnergyComponent(threshold=8)
    },
}

item_dict = {
    "healing vial": {
        "item": ItemComponent(),
        "stackable": StackableComponent(),
        "char": "!",
        "color": (127, 0, 255),
        "consumable": consumable.HealConsumable(amount=5),
    },

    "extra healing vial": {
        "item": ItemComponent(),
        "stackable": StackableComponent(),
        "char": "!",
        "color": (127, 0, 200),
        "consumable": consumable.HealConsumable(amount=15),
    },

    "poison vial": {
        "item": ItemComponent(),
        "stackable": StackableComponent(),
        "char": "!",
        "color": (255, 0, 0),
        "consumable": consumable.PoisonConsumable(amount=10),
    },

    "lightning scroll": {
        "item": ItemComponent(),
        "stackable": StackableComponent(),
        "char": "~",
        "color": (255, 255, 0),
        "consumable": consumable.LightningDamageConsumable(damage=20, maximum_range=5),
    },

    "confusion scroll": {
        "item": ItemComponent(),
        "stackable": StackableComponent(),
        "char": "~",
        "color": (207, 63, 255),
        "consumable": consumable.TargetedConfusionConsumable(number_of_turns=10),
    },

    "fireball scroll": {
        "item": ItemComponent(),
        "stackable": StackableComponent(),
        "char": "~",
        "color": (255, 0, 0),
        "consumable": consumable.FireballDamageConsumable(damage=12, radius=3),
    },

    # WEAPONS
    "dagger": {
        "item": ItemComponent(),
        "stackable": StackableComponent(),
        "char": "/",
        "color": (0, 191, 255),
        "equippable": equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('dagger', [3])),
        ),
    },

    "riot baton": {
        "item": ItemComponent(),
        "char": "/",
        "color": (0, 191, 255),
        "equippable": equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('baton', [8])),
        ),
    },

    "scalpal": {
        "item": ItemComponent(),
        "char": "/",
        "color": (0, 191, 255),
        "equippable": equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('scalpal', [4])),
        ),
    },

    "police baton": {
        "item": ItemComponent(),
        "char": "/",
        "color": (0, 191, 255),
        "equippable": equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('club', [4])),
        ),
    },

    "golf club": {
        "item": ItemComponent(),
        "char": "/",
        "color": (0, 191, 255),
        "equippable": equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('club', [5])),
        ),
    },

    "tennis racket": {
        "item": ItemComponent(),
        "char": "/",
        "color": (0, 191, 255),
        "equippable": equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('club', [5])),
        ),
    },

    "frying pan": {
        "item": ItemComponent(),
        "char": "/",
        "color": (0, 191, 255),
        "equippable": equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('club', [7])),
        ),
    },

    "hammer": {
        "item": ItemComponent(),
        "char": "/",
        "color": (0, 191, 255),
        "equippable": equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('club', [4])),
        ),
    },

    "metal pipe": {
        "item": ItemComponent(),
        "char": "/",
        "color": (0, 191, 255),
        "equippable": equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('club', [5])),
        ),
    },

    "big crowbar": {
        "item": ItemComponent(),
        "char": "/",
        "color": (0, 191, 255),
        "equippable": equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('club', [6])),
        ),
    },

    "plunger": {
        "item": ItemComponent(),
        "char": "/",
        "color": (0, 191, 255),
        "equippable": equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('club', [2])),
        ),
    },

    "rebar pipe": {
        "item": ItemComponent(),
        "char": "/",
        "color": (0, 191, 255),
        "equippable": equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('club', [6])),
        ),
    },

    "sledgehammer": {
        "item": ItemComponent(),
        "char": "/",
        "color": (0, 191, 255),
        "equippable": equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('club', [10])),
        ),
    },

    "wooden stick": {
        "item": ItemComponent(),
        "char": "/",
        "color": (0, 191, 255),
        "equippable": equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('club', [4])),
        ),
    },

    "green lightsaber": {
        "item": ItemComponent(),
        "char": "/",
        "color": (0, 191, 255),
        "equippable": equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('lightsaber', [3, 9])),
        ),
    },

    "blue lightsaber": {
        "item": ItemComponent(),
        "char": "/",
        "color": (0, 191, 255),
        "equippable": equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('lightsaber', [5, 8])),
        ),
    },

    # ARMOR

    "leather vest": {
        "item": ItemComponent(),
        "char": "[",
        "color": tcod.dark_amber,
        "equippable": equippable.Armor(ac_bonus=-1),
    },

    "bulletproof vest": {
        "item": ItemComponent(),
        "char": "[",
        "color": tcod.turquoise,
        "equippable": equippable.Armor(ac_bonus=-3),
    },

    "chain vest": {
        "item": ItemComponent(),
        "char": "[",
        "color": tcod.dark_gray,
        "equippable": equippable.Armor(ac_bonus=-3),
    },

    "chest guard": {
        "item": ItemComponent(),
        "char": "[",
        "color": tcod.cyan,
        "equippable": equippable.Armor(ac_bonus=-2),
    },

    "tactical vest": {
        "item": ItemComponent(),
        "char": "[",
        "color": tcod.green,
        "equippable": equippable.Armor(ac_bonus=-2),
    },

    "riot armor": {
        "item": ItemComponent(),
        "char": "[",
        "color": tcod.dark_blue,
        "equippable": equippable.Armor(ac_bonus=-4),
    },

    "power armor": {
        "item": ItemComponent(),
        "char": "[",
        "color": tcod.flame,
        "equippable": equippable.Armor(ac_bonus=-5),
    },

    "fedora": {
        "item": ItemComponent(),
        "char": "[",
        "color": tcod.dark_crimson,
        "equippable": equippable.Helmet(ac_bonus=0),
    },

    "bandana": {
        "item": ItemComponent(),
        "char": "[",
        "color": tcod.light_green,
        "equippable": equippable.Helmet(ac_bonus=0),
    },

    "helmet": {
        "item": ItemComponent(),
        "char": "[",
        "color": tcod.orange,
        "equippable": equippable.Helmet(ac_bonus=-1),
    },

    "visored helmet": {
        "item": ItemComponent(),
        "char": "[",
        "color": tcod.orange,
        "equippable": equippable.Helmet(ac_bonus=-1),
    },

    "riot helmet": {
        "item": ItemComponent(),
        "char": "[",
        "color": tcod.dark_blue,
        "equippable": equippable.Helmet(ac_bonus=-2),
    },

    "ballistic helmet": {
        "item": ItemComponent(),
        "char": "[",
        "color": tcod.turquoise,
        "equippable": equippable.Helmet(ac_bonus=-3),
    },

    "power helmet": {
        "item": ItemComponent(),
        "char": "[",
        "color": tcod.flame,
        "equippable": equippable.Helmet(ac_bonus=-4),
    },

    "rubber gloves": {
        "item": ItemComponent(),
        "char": "[",
        "color": tcod.orange,
        "equippable": equippable.Gloves(ac_bonus=0),
    },

    "leather gloves": {
        "item": ItemComponent(),
        "char": "[",
        "color": tcod.dark_amber,
        "equippable": equippable.Gloves(ac_bonus=-1),
    },

    "riot gloves": {
        "item": ItemComponent(),
        "char": "[",
        "color": tcod.dark_blue,
        "equippable": equippable.Gloves(ac_bonus=-2),
    },

    "tactical boots": {
        "item": ItemComponent(),
        "char": "[",
        "color": tcod.green,
        "equippable": equippable.Boots(ac_bonus=-1),
    },

    "combat boots": {
        "item": ItemComponent(),
        "char": "[",
        "color": tcod.dark_green,
        "equippable": equippable.Boots(ac_bonus=-2),
    },

    "power boots": {
        "item": ItemComponent(),
        "char": "[",
        "color": tcod.flame,
        "equippable": equippable.Boots(ac_bonus=-3),
    },

    "garbage can lid": {
        "item": ItemComponent(),
        "char": "[",
        "color": tcod.light_gray,
        "equippable": equippable.Shield(ac_bonus=-1),
    },

    "riot shield": {
        "item": ItemComponent(),
        "char": "[",
        "color": tcod.dark_blue,
        "equippable": equippable.Shield(ac_bonus=-2),
    },

    "ballistic shield": {
        "item": ItemComponent(),
        "char": "[",
        "color": tcod.turquoise,
        "equippable": equippable.Shield(ac_bonus=-3),
    },

    "leather belt": {
        "item": ItemComponent(),
        "char": "[",
        "color": tcod.dark_amber,
        "equippable": equippable.Belt(ac_bonus=-1),
    },

    "tactical belt": {
        "item": ItemComponent(),
        "char": "[",
        "color": tcod.green,
        "equippable": equippable.Belt(ac_bonus=-2),
    },

    "power belt": {
        "item": ItemComponent(),
        "char": "[",
        "color": tcod.flame,
        "equippable": equippable.Belt(ac_bonus=-3),
    },

    "leather wrists": {
        "item": ItemComponent(),
        "char": "[",
        "color": tcod.dark_amber,
        "equippable": equippable.Arms(ac_bonus=-1),
    },

    "elbow pads": {
        "item": ItemComponent(),
        "char": "[",
        "color": tcod.orange,
        "equippable": equippable.Arms(ac_bonus=-1),
    },

    "forearm guards": {
        "item": ItemComponent(),
        "char": "[",
        "color": tcod.dark_gray,
        "equippable": equippable.Arms(ac_bonus=-2),
    },

    "power wrists": {
        "item": ItemComponent(),
        "char": "[",
        "color": tcod.flame,
        "equippable": equippable.Arms(ac_bonus=-3),
    },
}

# Money
money = {
    "name": 'dollar',
    "char": '$',
    "color": tcod.gold,
    "stackable": StackableComponent(),
}


dungeon_features = {
    "bear trap": {
        "char": '^',
        "x": -1,
        "y": -1,
        "color": (0xFF, 0x0, 0x0),
        "render_order": RenderOrder.TRAP,
        "blocks_movement": False,
        "hidden": True,
        "trap": True,
        "consumable": consumable.BearTrapConsumable(damage=8, turns=20),
        "transparent": True,
    },

    "gas trap": {
        "char": '^',
        "x": -1,
        "y": -1,
        "color": tcod.green,
        "render_order": RenderOrder.TRAP,
        "blocks_movement": False,
        "hidden": True,
        "trap": True,
        "consumable": consumable.ConfusionTrapConsumable(number_of_turns=5),
        "transparent": True,
    },

    "nerve gas trap": {
        "char": '^',
        "x": -1,
        "y": -1,
        "color": tcod.purple,
        "render_order": RenderOrder.TRAP,
        "blocks_movement": False,
        "hidden": True,
        "trap": True,
        "consumable": consumable.ParalysisTrapConsumable(number_of_turns=10),
        "transparent": True,
    },

    "engraving": {
        "char": '.',
        "x": -1,
        "y": -1,
        "color": (200, 200, 200),
        "render_order": RenderOrder.TRAP,
        "blocks_movement": False,
        "hidden": True,
        "trap": True,
        "consumable": consumable.EngravingConsumable(),
        "transparent": True,
    },
}


hidden_corridor = Entity(
    name='hidden corridor',
    char=' ',
    x=-1,
    y=-1,
    color=(0xFF, 0x0, 0x0),
    render_order=RenderOrder.TRAP,
    blocks_movement=True,
    hidden=True,
    transparent=False,
)

hidden_door = Entity(
    name='hidden door',
    char='?',  # Will be replaced with camo-tile depending where on the wall it is.
    x=-1,
    y=-1,
    # color=tcod.white,
    color=(200, 200, 200),
    render_order=RenderOrder.TRAP,
    blocks_movement=True,
    transparent=True,
    # camo=True,
    hidden=True,
    trap=True,  # Just adding this so that it still disguises the door when out of sight.
)

item_chances = {
    # keys in the dictionary represent the floor number,
    # and the value is a list of tuples.
    0: [
        ("healing vial", 200),
        # ("poison vial", 200),
        ("extra healing vial", 35),

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
