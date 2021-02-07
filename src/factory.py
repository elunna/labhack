from components import consumable
from components import equippable
from components.ai import HostileAI
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from . import actor
from . import item

player = actor.Actor(
    char="@",
    color=(255, 255, 255),
    name="Player",
    ai_cls=HostileAI,
    equipment=Equipment(),
    fighter=Fighter(hp=30, base_ac=2, base_power=5),

    # Original inventory capacity is 26 because we have 26 lowercase letters.
    inventory=Inventory(capacity=26),
    level=Level(level_up_base=200),
)

orc = actor.Actor(
    char="o",
    color=(63, 127, 63),
    name="Orc",
    ai_cls=HostileAI,
    equipment=Equipment(),
    fighter=Fighter(hp=10, base_ac=0, base_power=6),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
)

troll = actor.Actor(
    char="T",
    color=(0, 127, 0),
    name="Troll",
    ai_cls=HostileAI,
    equipment=Equipment(),
    fighter=Fighter(hp=16, base_ac=1, base_power=10),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=100),
)

health_potion = item.Item(
    char="!",
    color=(127, 0, 255),
    name="Health Potion",
    consumable=consumable.HealingConsumable(amount=4),
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
    equippable=equippable.Dagger()
)

sword = item.Item(
    char="/",
    color=(0, 191, 255),
    name="Sword",
    equippable=equippable.Sword()
)

leather_armor = item.Item(
   char="[",
   color=(139, 69, 19),
   name="Leather Armor",
   equippable=equippable.LeatherArmor(),
)

chain_mail = item.Item(
    char="[",
    color=(139, 69, 19),
    name="Chain Mail",
    equippable=equippable.ChainMail()
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
