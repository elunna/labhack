import tcod
from components import consumable
from components import equippable

items = {
    "health potion": {
        "char": "!",
        "color": tcod.blue,
        "name": "Health Potion",
        "consumable": consumable.HealingConsumable(amount=4),
    },

    "confusion potion": {
        "char": "!",
        "color": tcod.yellow,
        "name": "Potion of Confusion",
        "consumable": consumable.ConfusionPotionConsumable(number_of_turns=8),
    },

    "paralysis potion": {
        "char": "!",
        "color": tcod.red,
        "name": "Potion of Paralysis",
        "consumable": consumable.ParalysisConsumable(number_of_turns=5),
    },

    "lightning scroll": {
        "char": "~",
        "color": (255, 255, 0),
        "name": "Lightning Scroll",
        "consumable": consumable.LightningDamageConsumable(damage=20, maximum_range=5),
    },

    "confusion scroll": {
        "char": "~",
        "color": (207, 63, 255),
        "name": "Confusion Scroll",
        "consumable": consumable.ConfusionConsumable(number_of_turns=10),
    },

    "fireball scroll": {
        "char": "~",
        "color": (255, 0, 0),
        "name": "Fireball Scroll",
        "consumable": consumable.FireballDamageConsumable(damage=12, radius=3),
    },

    "dagger": {
        "char": "/",
        "color": (0, 191, 255),
        "name": "Dagger",
        "equippable": equippable.Dagger()
    },

    "sword": {
        "char": "/",
        "color": (0, 191, 255),
        "name": "Sword",
        "equippable": equippable.Sword()
    },

    "leather armor": {
        "char": "[",
        "color": (139, 69, 19),
        "name": "Leather Armor",
        "equippable": equippable.LeatherArmor(),
    },

    "chain mail": {
        "char": "[",
        "color": (139, 69, 19),
        "name": "Chain Mail",
        "equippable": equippable.ChainMail()
    },
}
