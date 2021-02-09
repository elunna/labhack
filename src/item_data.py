from components import consumable, equippable, attacks
from src import item

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
