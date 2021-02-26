from . import settings
from .db import actor_dict, item_dict, item_chances, enemy_chances
import copy
import random


def make(entity_name):
    # Returns a new copy of the specified entity.
    if entity_name in actor_dict:
        return copy.deepcopy(actor_dict[entity_name])
    if entity_name in item_dict:
        return copy.deepcopy(item_dict[entity_name])
    raise ValueError(f'{entity_name} is not a valid Entity!')


def spawn(entity_name, gamemap, x, y):
    """Spawn a copy of the entity at the given map and location.
    Returns the instance of the entity.
    """
    e = make(entity_name)
    gamemap.add_entity(e, x, y)
    return e


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


def place_items(new_room, dungeon, floor_number):
    number_of_items = random.randint(
        0, get_max_value_for_floor(settings.max_items_by_floor, floor_number)
    )

    items = get_entities_at_random(
        item_chances, number_of_items, floor_number
    )

    for entity in items:
        x, y = new_room.random_point_inside()
        # We don't care if they stack on the map
        # entity.spawn(dungeon, x, y)
        spawn(entity, dungeon, x, y)


def place_monsters(new_room, dungeon, floor_number):
    number_of_monsters = random.randint(
        0, get_max_value_for_floor(settings.max_monsters_by_floor, floor_number)
    )

    monsters = get_entities_at_random(
        enemy_chances, number_of_monsters, floor_number
    )

    for entity in monsters:
        x = random.randint(new_room.x1 + 1, new_room.x2 - 2)
        y = random.randint(new_room.y1 + 1, new_room.y2 - 2)

        # Don't spawn them on top of each other.
        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            spawn(entity, dungeon, x, y)


def populate_map(new_map, current_floor):
    for r in new_map.rooms:
        # Populate the room with monsters and items
        place_monsters(r, new_map, current_floor)
        place_items(r, new_map, current_floor)
        # place traps
        # place secrets
