import settings
import tcod
from components.ai import ApproachAI, StationaryAI, GridMoveAI
from components.energy import EnergyMeter
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level


monsters = {
    "cleaning robot": {
        "char": "R",
        "color": tcod.light_green,
        "ai_cls": ApproachAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=3, base_defense=1, base_power=1),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=4),
        "energymeter": EnergyMeter(threshold=settings.very_slow)
    },

    "grid bug": {
        "char": "x",
        "color": tcod.magenta,
        "ai_cls": GridMoveAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=1, base_defense=1, base_power=1),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=1),
        "energymeter": EnergyMeter(threshold=settings.normal)
    },

    "mouse": {
        "char": "r",
        "color": tcod.gray,
        "ai_cls": ApproachAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=2, base_defense=1, base_power=1),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=2),
        "energymeter": EnergyMeter(threshold=settings.normal)
    },

    "broken robot": {
        "char": "R",
        "color": tcod.black,
        "ai_cls": StationaryAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=8, base_defense=1, base_power=1),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=5),
        "energymeter": EnergyMeter(threshold=settings.normal)
    },

    "drone zapper": {
        "char": "R",
        "color": tcod.blue,
        "ai_cls": ApproachAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=4, base_defense=1, base_power=2),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=12),
        "energymeter": EnergyMeter(threshold=settings.normal)
    },

    "jumping spider": {
        "char": "s",
        "color": tcod.yellow,
        "ai_cls": ApproachAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=2, base_defense=1, base_power=4),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=10),
        "energymeter": EnergyMeter(threshold=settings.fast)
    },

    "med-school dropout": {
        "char": "@",
        "color": tcod.white,
        "ai_cls": ApproachAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=6, base_defense=1, base_power=2),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=13),
        "energymeter": EnergyMeter(threshold=settings.slow)
    },

    "rabbit": {
        "char": "r",
        "color": tcod.white,
        "ai_cls": ApproachAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=2, base_defense=1, base_power=2),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=7),
        "energymeter": EnergyMeter(threshold=settings.fast)
    },

    "venus fly trap": {
        "char": "P",
        "color": tcod.green,
        "ai_cls": StationaryAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=5, base_defense=1, base_power=2),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=8),
        "energymeter": EnergyMeter(threshold=settings.normal)
    },

    "face-sucker": {
        "char": "Q",
        "color": tcod.blue,
        "ai_cls": ApproachAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=5, base_defense=1, base_power=2),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=27),
        "energymeter": EnergyMeter(threshold=settings.very_fast)
    },

    "giant tick": {
        "char": "a",
        "color": tcod.gray,
        "ai_cls": ApproachAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=3, base_defense=1, base_power=5),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=21),
        "energymeter": EnergyMeter(threshold=settings.fast)
    },

    "giant leech": {
        "char": "L",
        "color": tcod.dark_green,
        "ai_cls": ApproachAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=8, base_defense=1, base_power=5),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=33),
        "energymeter": EnergyMeter(threshold=settings.slow)
    },

    "spiked drone": {
        "char": "R",
        "color": tcod.brass,
        "ai_cls": ApproachAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=5, base_defense=1, base_power=5),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=25),
        "energymeter": EnergyMeter(threshold=settings.normal)
    },

    "defense turret": {
        "char": "T",
        "color": tcod.light_blue,
        "ai_cls": StationaryAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=10, base_defense=1, base_power=2),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=45),
        "energymeter": EnergyMeter(threshold=settings.fast)
    },

    "rookie agent": {
        "char": "@",
        "color": tcod.dark_gray,
        "ai_cls": ApproachAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=2, base_defense=1, base_power=2),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=35),
        "energymeter": EnergyMeter(threshold=settings.fast)
    },

    "squealer": {
        "char": "Q",
        "color": tcod.light_purple,
        "ai_cls": ApproachAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=6, base_defense=1, base_power=3),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=55),
        "energymeter": EnergyMeter(threshold=settings.very_fast)
    },

    "henchman": {
        "char": "@",
        "color": tcod.gray,
        "ai_cls": ApproachAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=6, base_defense=1, base_power=6),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=65),
        "energymeter": EnergyMeter(threshold=settings.slow)
    },

    "mangler": {
        "char": "Q",
        "color": tcod.fuchsia,
        "ai_cls": ApproachAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=6, base_defense=1, base_power=3),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=75),
        "energymeter": EnergyMeter(threshold=settings.very_fast)
    },

    "scramper": {
        "char": "Q",
        "color": tcod.light_green,
        "ai_cls": ApproachAI,
        "equipment": Equipment(),
        "fighter": Fighter(hp=3, base_defense=1, base_power=6),
        "inventory": Inventory(capacity=0),
        "level": Level(xp_given=80),
        "energymeter": EnergyMeter(threshold=settings.very_fast)
    },
}
