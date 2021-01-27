from components.ai import HostileEnemy, HeroControllerAI, StationaryAI
from components import consumable, equippable
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from .item import Item
from .actor import Actor
from src.settings import RenderOrder
import tcod


def corpse_generator(actor):
    corpse = Item(
        x=actor.x,
        y=actor.y,
        char="%",
        color=actor.color,
        name=f'{actor.name} corpse',
    )
    corpse.render_order = RenderOrder.CORPSE
    return corpse

player = Actor(
    char="@",
    color=(255, 255, 255),
    name="Player",
    ai_cls=HeroControllerAI,
    equipment=Equipment(),
    fighter=Fighter(hp=30, base_defense=1, base_power=2),

    # Original inventory capacity is 26 because we have 26 lowercase letters.
    inventory=Inventory(capacity=26),
    level=Level(level_up_base=200),
)

gas_spore = Actor(
    char="e",
    color=tcod.gray,
    name="gas spore",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=8, base_defense=1, base_power=5),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=20),
)

yellow_light = Actor(
    char="e",
    color=tcod.yellow,
    name="yellow light",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=1, base_defense=1, base_power=2),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=20),
)

black_light = Actor(
    char="e",
    color=tcod.purple,
    name="black light",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=1, base_defense=1, base_power=2),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=20),
)

flaming_sphere = Actor(
    char="e",
    color=tcod.red,
    name="flaming sphere",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=2, base_defense=1, base_power=10),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=20),
)

freezing_sphere = Actor(
    char="e",
    color=tcod.blue,
    name="freezing sphere",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=2, base_defense=1, base_power=10),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=20),
)

shocking_sphere = Actor(
    char="e",
    color=tcod.azure,
    name="shocking sphere",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=2, base_defense=1, base_power=10),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=20),
)

jiggling_blob = Actor(
    char="b",
    color=tcod.magenta,
    name="jiggling blob",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=11, base_defense=3, base_power=3),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=20),
)

lava_blob = Actor(
    char="b",
    color=tcod.red,
    name="lava blob",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=11, base_defense=3, base_power=3),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=20),
)

static_blob = Actor(
    char="b",
    color=tcod.violet,
    name="static blob",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=11, base_defense=3, base_power=3),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=20),
)

burbling_blob = Actor(
    char="b",
    color=tcod.dark_gray,
    name="burbling blob",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=11, base_defense=3, base_power=3),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=20),
)

quivering_blob = Actor(
    char="b",
    color=tcod.white,
    name="quivering blob",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=6, base_defense=1, base_power=2),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=20),
)

gelatinous_cube = Actor(
    char="b",
    color=tcod.light_blue,
    name="gelatinous cube",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=30, base_defense=5, base_power=15),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=20),
)

acid_blob = Actor(
    char="b",
    color=tcod.light_green,
    name="acid blob",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=8, base_defense=2, base_power=4),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=20),
)

lichen = Actor(
    char="F",
    color=tcod.light_green,
    name="Lichen",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=1, base_defense=1, base_power=1),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
)

brown_mold = Actor(
    char="F",
    color=tcod.amber,
    name="Brown Mold",
    ai_cls=StationaryAI,
    equipment=Equipment(),
    fighter=Fighter(hp=1, base_defense=1, base_power=2),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
)

yellow_mold = Actor(
    char="F",
    color=tcod.yellow,
    name="Yellow Mold",
    ai_cls=StationaryAI,
    equipment=Equipment(),
    fighter=Fighter(hp=1, base_defense=1, base_power=2),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
)

green_mold = Actor(
    char="F",
    color=tcod.dark_green,
    name="Green Mold",
    ai_cls=StationaryAI,
    equipment=Equipment(),
    fighter=Fighter(hp=1, base_defense=1, base_power=2),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
)

red_mold = Actor(
    char="F",
    color=tcod.red,
    name="Red Mold",
    ai_cls=StationaryAI,
    equipment=Equipment(),
    fighter=Fighter(hp=1, base_defense=1, base_power=2),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
)

shrieker = Actor(
    char="F",
    color=tcod.purple,
    name="Shrieker",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=1, base_defense=1, base_power=2),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
)

violet_fungus = Actor(
    char="F",
    color=tcod.violet,
    name="Violet Fungus",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=1, base_defense=1, base_power=2),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
)

disgusting_mold = Actor(
    char="F",
    color=tcod.cyan,
    name="Disgusting Mold",
    ai_cls=StationaryAI,
    equipment=Equipment(),
    fighter=Fighter(hp=8, base_defense=2, base_power=8),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
)

black_mold = Actor(
    char="F",
    color=tcod.darkest_gray,
    name="Black Mold",
    ai_cls=StationaryAI,
    equipment=Equipment(),
    fighter=Fighter(hp=10, base_defense=4, base_power=16),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
)

grid_bug = Actor(
    char="x",
    color=tcod.magenta,
    name="Grid Bug",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=1, base_defense=1, base_power=2),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
)

spark_bug = Actor(
    char="x",
    color=tcod.violet,
    name="Spark Bug",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=2, base_defense=2, base_power=2),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
)

arc_bug = Actor(
    char="x",
    color=tcod.orange,
    name="Arc Bug",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=4, base_defense=4, base_power=4),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
)

lightning_bug = Actor(
    char="x",
    color=tcod.light_yellow,
    name="Lightning Bug",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=8, base_defense=8, base_power=8),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
)

firefly = Actor(
    char="x",
    color=tcod.light_red,
    name="Fire Fly",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=4, base_defense=1, base_power=1),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
)

orc = Actor(
    char="o",
    color=tcod.yellow,
    name="Orc",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=10, base_defense=0, base_power=4),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
)

troll = Actor(
    char="T",
    color=tcod.amber,
    name="Troll",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=16, base_defense=2, base_power=6),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=100),
)

health_potion = Item(
    char="!",
    color=tcod.blue,
    name="Health Potion",
    consumable=consumable.HealingConsumable(amount=4),
)

confusion_potion = Item(
    char="!",
    color=tcod.yellow,
    name="Potion of Confusion",
    consumable=consumable.ConfusionPotionConsumable(number_of_turns=8),
)

paralysis_potion = Item(
    char="!",
    color=tcod.red,
    name="Potion of Paralysis",
    consumable=consumable.ParalysisConsumable(number_of_turns=5),
)

lightning_scroll = Item(
    char="~",
    color=(255, 255, 0),
    name="Lightning Scroll",
    consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
)

confusion_scroll = Item(
    char="~",
    color=(207, 63, 255),
    name="Confusion Scroll",
    consumable=consumable.ConfusionConsumable(number_of_turns=10),
)

fireball_scroll = Item(
    char="~",
    color=(255, 0, 0),
    name="Fireball Scroll",
    consumable=consumable.FireballDamageConsumable(damage=12, radius=3),
)

dagger = Item(
    char="/",
    color=(0, 191, 255),
    name="Dagger",
    equippable=equippable.Dagger()
)

sword = Item(
    char="/",
    color=(0, 191, 255),
    name="Sword",
    equippable=equippable.Sword()
)

leather_armor = Item(
   char="[",
   color=(139, 69, 19),
   name="Leather Armor",
   equippable=equippable.LeatherArmor(),
)

chain_mail = Item(
    char="[",
    color=(139, 69, 19),
    name="Chain Mail",
    equippable=equippable.ChainMail()
)

item_chances = {
    # keys in the dictionary represent the floor number,
    # and the value is a list of tuples.
    # 0: [(health_potion, 35), (confusion_potion, 35)],
    0: [(health_potion, 35), (paralysis_potion, 35)],
    2: [(confusion_scroll, 10), (leather_armor, 5), (dagger, 5)],
    4: [(lightning_scroll, 25), (chain_mail, 5), (sword, 5), (fireball_scroll, 25)],
}

enemy_chances = {
    0: [
        (brown_mold, 5),
        (yellow_mold, 5),
        (green_mold, 5),
        (red_mold, 5),
        (shrieker, 5),
        (violet_fungus, 5),
        (lichen, 5),
        (grid_bug, 5),
        (firefly, 5),
    ],
    2: [
        (troll, 15),
        (gas_spore, 10),
        (yellow_light, 10),
        (black_light, 10),
        (flaming_sphere, 10),
        (freezing_sphere, 10),
        (shocking_sphere, 10),
        (spark_bug, 10),
        (orc, 10),
    ],
    3: [
        (jiggling_blob, 20),
        (lava_blob, 20),
        (static_blob, 20),
        (burbling_blob, 20),
        (quivering_blob, 20),
        (arc_bug, 20),
        (acid_blob, 20),
    ],
    4: [
        (gelatinous_cube, 50),
        (disgusting_mold, 50),
        (black_mold, 50),
        (lightning_bug, 50),
    ],
}


list_of_monsters = [
    ### low level 1
    brown_mold,
    yellow_mold,
    green_mold,
    red_mold,
    shrieker,
    violet_fungus,
    lichen,
    grid_bug,
    firefly,

    ### level 2
    gas_spore,
    yellow_light,
    black_light,
    flaming_sphere,
    freezing_sphere,
    shocking_sphere,
    spark_bug,
    troll,
    orc,

    ### Level 3
    jiggling_blob,
    lava_blob,
    static_blob,
    burbling_blob,
    quivering_blob,
    arc_bug,
    acid_blob,

    ###Level 4
    gelatinous_cube,
    disgusting_mold,
    black_mold,
    lightning_bug,
]
