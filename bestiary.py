import settings
import tcod
from components.ai import ApproachAI, StationaryAI, GridMoveAI
from components.energy import EnergyMeter
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level

monsters = {
    "gas spore": {
        "char": "e",
        "color": tcod.gray,
        "ai_cls": ApproachAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=8, base_defense=1, base_power=5),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=20),
        "energymeter": EnergyMeter(threshold=settings.slow)
    },

    "yellow light": {
        "char": "e",
        "color": tcod.yellow,
        "ai_cls": ApproachAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=1, base_defense=1, base_power=2),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=20),
        "energymeter": EnergyMeter(threshold=settings.fast)
    },

    "black light": {
        "char": "e",
        "color": tcod.purple,
        "ai_cls": ApproachAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=1, base_defense=1, base_power=2),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=20),
        "energymeter": EnergyMeter(threshold=settings.fast)
    },

    "flaming sphere": {
        "char": "e",
        "color": tcod.red,
        "ai_cls": ApproachAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=2, base_defense=1, base_power=10),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=20),
        "energymeter": EnergyMeter(threshold=settings.fast)
    },

    "freezing sphere": {
        "char": "e",
        "color": tcod.blue,
        "ai_cls": ApproachAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=2, base_defense=1, base_power=10),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=20),
        "energymeter": EnergyMeter(threshold=settings.fast)
    },

    "shocking sphere": {
        "char": "e",
        "color": tcod.azure,
        "ai_cls": ApproachAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=2, base_defense=1, base_power=10),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=20),
        "energymeter": EnergyMeter(threshold=settings.fast)
    },

    "jiggling blob": {
        "char": "b",
        "color": tcod.magenta,
        "ai_cls": ApproachAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=11, base_defense=3, base_power=3),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=20),
        "energymeter": EnergyMeter(threshold=settings.slow)
    },

    "lava blob": {
        "char": "b",
        "color": tcod.red,
        "ai_cls": ApproachAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=11, base_defense=3, base_power=3),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=20),
        "energymeter": EnergyMeter(threshold=settings.slow)
    },

    "static blob": {
        "char": "b",
        "color": tcod.violet,
        "ai_cls": ApproachAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=11, base_defense=3, base_power=3),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=20),
        "energymeter": EnergyMeter(threshold=settings.slow)
    },

    "burbling blob": {
        "char": "b",
        "color": tcod.dark_gray,
        "ai_cls": ApproachAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=11, base_defense=3, base_power=3),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=20),
        "energymeter": EnergyMeter(threshold=settings.slow)
    },

    "quivering blob": {
        "char": "b",
        "color": tcod.white,
        "ai_cls": ApproachAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=6, base_defense=1, base_power=2),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=20),
        "energymeter": EnergyMeter(threshold=settings.slow)
    },

    "gelatinous cube": {
        "char": "b",
        "color": tcod.light_blue,
        "ai_cls": ApproachAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=30, base_defense=5, base_power=15),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=20),
        "energymeter": EnergyMeter(threshold=settings.very_slow)
    },

    "acid blob": {
        "char": "b",
        "color": tcod.light_green,
        "ai_cls": ApproachAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=8, base_defense=2, base_power=4),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=20),
        "energymeter": EnergyMeter(threshold=settings.normal)
    },

    "lichen": {
        "char": "F",
        "color": tcod.light_green,
        "ai_cls": ApproachAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=1, base_defense=1, base_power=1),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=35),
        "energymeter": EnergyMeter(threshold=settings.very_slow)
    },

    "brown mold": {
        "char": "F",
        "color": tcod.amber,
        "ai_cls": StationaryAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=1, base_defense=1, base_power=2),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=35),
        "energymeter": EnergyMeter(threshold=settings.normal)
    },

    "yellow mold": {
        "char": "F",
        "color": tcod.yellow,
        "ai_cls": StationaryAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=1, base_defense=1, base_power=2),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=35),
        "energymeter": EnergyMeter(threshold=settings.normal)
    },

    "green mold": {
        "char": "F",
        "color": tcod.dark_green,
        "ai_cls": StationaryAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=1, base_defense=1, base_power=2),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=35),
        "energymeter": EnergyMeter(threshold=settings.normal)
    },

    "red mold": {
        "char": "F",
        "color": tcod.red,
        "ai_cls": StationaryAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=1, base_defense=1, base_power=2),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=35),
        "energymeter": EnergyMeter(threshold=settings.normal)
    },

    "shrieker": {
        "char": "F",
        "color": tcod.purple,
        "ai_cls": ApproachAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=1, base_defense=1, base_power=2),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=35),
        "energymeter": EnergyMeter(threshold=settings.very_slow)
    },

    "violet fungus": {
        "char": "F",
        "color": tcod.violet,
        "ai_cls": ApproachAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=1, base_defense=1, base_power=2),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=35),
        "energymeter": EnergyMeter(threshold=settings.very_slow)
    },

    "disgusting mold": {
        "char": "F",
        "color": tcod.cyan,
        "ai_cls": StationaryAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=8, base_defense=2, base_power=8),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=35),
        "energymeter": EnergyMeter(threshold=settings.normal)
    },

    "black mold": {
        "char": "F",
        "color": tcod.darkest_gray,
        "ai_cls": StationaryAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=10, base_defense=4, base_power=16),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=35),
        "energymeter": EnergyMeter(threshold=settings.normal)
    },

    "grid bug": {
        "char": "x",
        "color": tcod.magenta,
        "ai_cls": GridMoveAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=1, base_defense=1, base_power=2),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=35),
        "energymeter": EnergyMeter(threshold=settings.normal)
    },

    "spark bug": {
        "char": "x",
        "color": tcod.violet,
        "ai_cls": ApproachAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=2, base_defense=2, base_power=2),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=35),
        "energymeter": EnergyMeter(threshold=settings.normal)
    },

    "arc bug": {
        "char": "x",
        "color": tcod.orange,
        "ai_cls": ApproachAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=4, base_defense=4, base_power=4),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=35),
        "energymeter": EnergyMeter(threshold=settings.normal)
    },

    "lightning bug": {
        "char": "x",
        "color": tcod.light_yellow,
        "ai_cls": ApproachAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=8, base_defense=8, base_power=8),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=35),
        "energymeter": EnergyMeter(threshold=settings.normal)
    },

    "firefly": {
        "char": "x",
        "color": tcod.light_red,
        "ai_cls": ApproachAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=4, base_defense=1, base_power=1),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=35),
        "energymeter": EnergyMeter(threshold=settings.normal)
    },

    "orc": {
        "char": "o",
        "color": tcod.yellow,
        "ai_cls": ApproachAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=10, base_defense=0, base_power=4),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=35),
        "energymeter": EnergyMeter(threshold=settings.normal)
    },

    "troll": {
        "char": "T",
        "color": tcod.amber,
        "ai_cls": ApproachAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=16, base_defense=2, base_power=6),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=100),
        "energymeter": EnergyMeter(threshold=settings.fast)
    },
}
