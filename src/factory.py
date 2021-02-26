from . import settings
from .db import actor_dict, item_dict
import copy
import random


def make(entity_name):
    if entity_name in actor_dict:
        return copy.deepcopy(actor_dict[entity_name])
    if entity_name in item_dict:
        return copy.deepcopy(item_dict[entity_name])

    return None


item_chances = {
    # keys in the dictionary represent the floor number,
    # and the value is a list of tuples.
    0: [
        ("health_potion", 200),
        ("confusion_scroll", 45),
        ("lightning_scroll", 35),
        ("fireball_scroll", 35),

        ("dagger", 3),
        ("riot_baton", 3),
        ("scalpal", 3),
        ("police_baton", 1),
        ("golf_club", 2),
        ("hammer", 3),
        ("metal_pipe", 3),
        ("big_crowbar", 3),
        ("plunger", 3),
        ("rebar_pipe", 3),
        ("sledgehammer", 1),
        ("wooden_stick", 3),
        ("gr_light_saber", 1),
        ("bl_light_saber", 1),
        ("tennis_racket", 2),
        ("frying_pan", 2),

        ("leather_vest", 5),      # AC1
        ("chest_guard", 5),       # AC2
        ("tactical_vest", 5),     # AC2
        ("bulletproof_vest", 3),  # AC3
        ("chain_vest", 2),        # AC3
        ("riot_armor", 2),        # AC4
        ("power_armor", 1),       # AC5
        ("fedora", 1),            # AC0
        ("bandana", 2),           # AC0
        ("helmet", 5),            # AC1
        ("visored_helmet", 3),    # AC1
        ("riot_helmet", 5),       # AC2
        ("ballistic_helmet", 2),  # AC3
        ("power_helmet", 1),      # AC4
        ("rubber_gloves", 3),     # AC0
        ("leather_gloves", 6),    # AC1
        ("riot_gloves", 1),       # AC2
        ("tactical_boots", 5),    # AC1
        ("combat_boots", 3),      # AC2
        ("power_boots", 1),       # AC3
        ("garbage_lid", 5),       # AC1
        ("riot_shield", 6),       # AC2
        ("ballistic_shield", 1),  # AC3
        ("leather_belt", 6),      # AC1
        ("tactical_belt", 3),     # AC2
        ("power_belt", 1),        # AC3
        ("elbow_pads", 6),        # AC1
        ("leather_wrists", 5),    # AC1
        ("forearm_guards", 6),    # AC2
        ("power_wrists", 1),      # AC3
    ],
}

enemy_chances = {
    0: [("grid bug", 40), ("spider drone", 80)],
    3: [("giant leech", 15), ("med school dropout", 25)],
    5: [("giant leech", 30), ("cyber cat", 35)],
    7: [("giant leech", 60), ("cyber cat", 40)],
}


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
        make(entity).spawn(dungeon, x, y)


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
            make(entity).spawn(dungeon, x, y)


def populate_map(new_map, current_floor):
    for r in new_map.rooms:
        # Populate the room with monsters and items
        place_monsters(r, new_map, current_floor)
        place_items(r, new_map, current_floor)
