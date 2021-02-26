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
from src import actor, item

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

    "henchman": actor.Actor(
        char="@",
        color=tcod.dark_gray,
        name="Henchman",
        ai_cls=HostileAI(),
        equipment=Equipment(),
        fighter=Fighter(hp=6),
        attack_comp=AttackComponent(Attack('punch', [5])),
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
}
item_dict = {
    "health_potion": item.Item(
        char="!",
        color=(127, 0, 255),
        name="Health Potion",
        consumable=consumable.HealConsumable(amount=5),
    ),

    "lightning_scroll": item.Item(
        char="~",
        color=(255, 255, 0),
        name="Lightning Scroll",
        consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
    ),

    "confusion_scroll": item.Item(
        char="~",
        color=(207, 63, 255),
        name="Confusion Scroll",
        consumable=consumable.ConfusionConsumable(number_of_turns=10),
    ),

    "fireball_scroll": item.Item(
        char="~",
        color=(255, 0, 0),
        name="Fireball Scroll",
        consumable=consumable.FireballDamageConsumable(damage=12, radius=3),
    ),

    # WEAPONS

    "dagger": item.Item(
        char="/",
        color=(0, 191, 255),
        name="Dagger",
        equippable=equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('dagger', [3])),
        ),
    ),

    "riot_baton": item.Item(
        char="/",
        color=(0, 191, 255),
        name="Riot Baton",
        equippable=equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('baton', [8])),
        ),
    ),

    "scalpal": item.Item(
        char="/",
        color=(0, 191, 255),
        name="Scalpal",
        equippable=equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('scalpal', [4])),
        ),
    ),

    "police_baton": item.Item(
        char="/",
        color=(0, 191, 255),
        name="Police Baton",
        equippable=equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('club', [4])),
        ),
    ),

    "golf_club": item.Item(
        char="/",
        color=(0, 191, 255),
        name="Golf Club",
        equippable=equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('club', [5])),
        ),
    ),

    "tennis_racket": item.Item(
        char="/",
        color=(0, 191, 255),
        name="Tennis Racket",
        equippable=equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('club', [5])),
        ),
    ),

    "frying_pan": item.Item(
        char="/",
        color=(0, 191, 255),
        name="Frying Pan",
        equippable=equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('club', [7])),
        ),
    ),

    "hammer": item.Item(
        char="/",
        color=(0, 191, 255),
        name="Hammer",
        equippable=equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('club', [4])),
        ),
    ),

    "metal_pipe": item.Item(
        char="/",
        color=(0, 191, 255),
        name="Metal Pipe",
        equippable=equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('club', [5])),
        ),
    ),

    "big_crowbar": item.Item(
        char="/",
        color=(0, 191, 255),
        name="Big Crowbar",
        equippable=equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('club', [6])),
        ),
    ),

    "plunger": item.Item(
        char="/",
        color=(0, 191, 255),
        name="Plunger",
        equippable=equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('club', [2])),
        ),
    ),

    "rebar_pipe": item.Item(
        char="/",
        color=(0, 191, 255),
        name="Rebar Pipe",
        equippable=equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('club', [6])),
        ),
    ),

    "sledgehammer": item.Item(
        char="/",
        color=(0, 191, 255),
        name="Sledgehammer",
        equippable=equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('club', [10])),
        ),
    ),

    "wooden_stick": item.Item(
        char="/",
        color=(0, 191, 255),
        name="Wooden Stick",
        equippable=equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('club', [4])),
        ),
    ),

    "gr_light_saber": item.Item(
        char="/",
        color=(0, 191, 255),
        name="Green lightsaber",
        equippable=equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('lightsaber', [3, 9])),
        ),
    ),

    "bl_light_saber": item.Item(
        char="/",
        color=(0, 191, 255),
        name="Blue lightsaber",
        equippable=equippable.Weapon(
            attack_comp=attack_cmp.AttackComponent(Attack('lightsaber', [5, 8])),
        ),
    ),

    # ARMOR

    "leather_vest": item.Item(
       char="[",
       color=tcod.dark_amber,
       name="Leather Vest",
       equippable=equippable.Armor(ac_bonus=-1),
    ),

    "bulletproof_vest": item.Item(
        char="[",
        color=tcod.turquoise,
        name="Bulletproof Vest",
        equippable=equippable.Armor(ac_bonus=-3),
    ),

    "chain_vest": item.Item(
        char="[",
        color=tcod.dark_gray,
        name="Chain Vest",
        equippable=equippable.Armor(ac_bonus=-3),
    ),

    "chest_guard": item.Item(
        char="[",
        color=tcod.cyan,
        name="Chest Guard",
        equippable=equippable.Armor(ac_bonus=-2),
    ),

    "tactical_vest": item.Item(
        char="[",
        color=tcod.green,
        name="Tactical Vest",
        equippable=equippable.Armor(ac_bonus=-2),
    ),

    "riot_armor": item.Item(
        char="[",
        color=tcod.dark_blue,
        name="Riot Armor",
        equippable=equippable.Armor(ac_bonus=-4),
    ),

    "power_armor": item.Item(
        char="[",
        color=tcod.flame,
        name="Power Armor",
        equippable=equippable.Armor(ac_bonus=-5),
    ),

    "fedora": item.Item(
        char="[",
        color=tcod.dark_crimson,
        name="Fedora",
        equippable=equippable.Helmet(ac_bonus=0),
    ),

    "bandana": item.Item(
        char="[",
        color=tcod.light_green,
        name="Bandana",
        equippable=equippable.Helmet(ac_bonus=0),
    ),

    "helmet": item.Item(
        char="[",
        color=tcod.orange,
        name="Helmet",
        equippable=equippable.Helmet(ac_bonus=-1),
    ),

    "visored_helmet": item.Item(
        char="[",
        color=tcod.orange,
        name="Visored Helmet",
        equippable=equippable.Helmet(ac_bonus=-1),
    ),

    "riot_helmet": item.Item(
        char="[",
        color=tcod.dark_blue,
        name="Riot Helmet",
        equippable=equippable.Helmet(ac_bonus=-2),
    ),

    "ballistic_helmet": item.Item(
        char="[",
        color=tcod.turquoise,
        name="Ballistic Helmet",
        equippable=equippable.Helmet(ac_bonus=-3),
    ),

    "power_helmet": item.Item(
        char="[",
        color=tcod.flame,
        name="Power Helmet",
        equippable=equippable.Helmet(ac_bonus=-4),
    ),

    "rubber_gloves": item.Item(
        char="[",
        color=tcod.orange,
        name="Rubber Gloves",
        equippable=equippable.Gloves(ac_bonus=0),
    ),

    "leather_gloves": item.Item(
        char="[",
        color=tcod.dark_amber,
        name="Leather Gloves",
        equippable=equippable.Gloves(ac_bonus=-1),
    ),

    "riot_gloves": item.Item(
        char="[",
        color=tcod.dark_blue,
        name="Riot Gloves",
        equippable=equippable.Gloves(ac_bonus=-2),
    ),

    "tactical_boots": item.Item(
        char="[",
        color=tcod.green,
        name="Tactical Boots",
        equippable=equippable.Boots(ac_bonus=-1),
    ),

    "combat_boots": item.Item(
        char="[",
        color=tcod.dark_green,
        name="Combat Boots",
        equippable=equippable.Boots(ac_bonus=-2),
    ),

    "power_boots": item.Item(
        char="[",
        color=tcod.flame,
        name="Power Boots",
        equippable=equippable.Boots(ac_bonus=-3),
    ),

    "garbage_lid": item.Item(
        char="[",
        color=tcod.light_gray,
        name="Garbage Can Lid",
        equippable=equippable.Shield(ac_bonus=-1),
    ),

    "riot_shield": item.Item(
        char="[",
        color=tcod.dark_blue,
        name="Riot Shield",
        equippable=equippable.Shield(ac_bonus=-2),
    ),

    "ballistic_shield": item.Item(
        char="[",
        color=tcod.turquoise,
        name="Ballistic Shield",
        equippable=equippable.Shield(ac_bonus=-3),
    ),

    "leather_belt": item.Item(
        char="[",
        color=tcod.dark_amber,
        name="Leather Belt",
        equippable=equippable.Belt(ac_bonus=-1),
    ),

    "tactical_belt": item.Item(
        char="[",
        color=tcod.green,
        name="Tactical Belt",
        equippable=equippable.Belt(ac_bonus=-2),
    ),

    "power_belt": item.Item(
        char="[",
        color=tcod.flame,
        name="Power Belt",
        equippable=equippable.Belt(ac_bonus=-3),
    ),

    "leather_wrists": item.Item(
        char="[",
        color=tcod.dark_amber,
        name="Leather Wrists",
        equippable=equippable.Arms(ac_bonus=-1),
    ),

    "elbow_pads": item.Item(
        char="[",
        color=tcod.orange,
        name="Elbow Pads",
        equippable=equippable.Arms(ac_bonus=-1),
    ),

    "forearm_guards": item.Item(
        char="[",
        color=tcod.dark_gray,
        name="Forearm Guards",
        equippable=equippable.Arms(ac_bonus=-2),
    ),

    "power_wrists": item.Item(
        char="[",
        color=tcod.flame,
        name="Power Wrists",
        equippable=equippable.Arms(ac_bonus=-3),
    ),
}