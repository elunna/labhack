from components.ai import ApproachAI, HeroControllerAI, StationaryAI, GridMoveAI
from components import equippable
from components.energy import EnergyMeter
from components import consumable
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
import actors
import bestiary
import items
import item_db
import random
import settings
import tcod


def mk_actor(monster_name):
    return actors.Actor(
        char=bestiary.monsters[monster_name]['char'],
        color=bestiary.monsters[monster_name]['color'],
        name=monster_name,
        ai_cls=bestiary.monsters[monster_name]['ai_cls'],
        equipment=bestiary.monsters[monster_name]['equipment'],
        fighter=bestiary.monsters[monster_name]['fighter'],
        inventory=bestiary.monsters[monster_name]['inventory'],
        level=bestiary.monsters[monster_name]['level'],
        energymeter=bestiary.monsters[monster_name]['energymeter'],
    )

# Build a dict of monster names and Actors
monsters = {m: mk_actor(m) for m in bestiary.monsters}

def mk_item(item_name):
    return items.Item(
        char=item_db.items[item_name].get('char'),
        color=item_db.items[item_name].get('color'),
        name=item_db.items[item_name].get('name'),
        consumable=item_db.items[item_name].get('consumable'),
        equippable=item_db.items[item_name].get('equippable'),
    )


item_dict = {i: mk_item(i) for i in item_db.items}


def get_monster(self, name):
    return monsters[name]


def get_item(self, name):
    return item_dict[name]


def corpse_generator(actor):
    corpse = items.Item(
        x=actor.x,
        y=actor.y,
        char="%",
        color=actor.color,
        name=f'{actor.name} corpse',
    )
    corpse.render_order = settings.RenderOrder.CORPSE
    return corpse


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
    # TODO: Reduce this to only return one random entity...
    # TODO: Turn this into a more functional object - EntityChooser...
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


player = actors.Actor(
    char="@",
    color=(255, 255, 255),
    name="Player",
    ai_cls=HeroControllerAI,
    equipment=Equipment(),
    fighter=Fighter(hp=30, base_defense=1, base_power=2),

    # Original inventory capacity is 26 because we have 26 lowercase letters.
    inventory=Inventory(capacity=26),
    level=Level(level_up_base=200),
    energymeter=EnergyMeter(threshold=settings.normal),
)

