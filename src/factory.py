import math

import src.db
from . import settings, tiles
from . import db
import copy
import random
from .actor import Actor
from .item import Item


class EntityFactory:
    """ Builds a database of all the Entities in db.py -
    Let's us get a monster appropriate in level for the players current XP level and dungeon level.
    # TODO: Contains
    # TODO: Needs Player and Dungeon to work properly.
    """
    def __init__(self, entity_dict, dungeon=None, player=None):
        # We'll create a dict of names and their Entities for easy accessibility
        self.entities = {k: make(k) for k in entity_dict}
        # Don't include the player
        if "player" in self.entities:
            self.entities.pop('player')

        self.dungeon = dungeon
        self.player = player

    def difficulty_specific_monster(self, dlevel, player_level):
        """Finds monster that is appropriate for the player level and the dungeon level
            Returns the entity
        """
        max_difficulty = math.ceil((dlevel + player_level) / 2)
        min_difficulty = math.floor(dlevel / 6)
        qualifiers = []
        for name, entity in self.entities.items():
            if min_difficulty <= entity.level.difficulty <= max_difficulty:
                qualifiers.append(name)

        if len(qualifiers) == 0:
            raise Exception('No valid monsters for difficulty!')

        choice = random.choice(qualifiers)
        # return make(choice)
        return choice

    def populate_level(self, dlevel):
        new_map = self.dungeon.get_map(dlevel)
        for r in new_map.rooms:
            # Populate the room with monsters and items
            if random.random() > .50:
                # 33% for each new room to have monsters
                self.place_monsters(new_map, r)

            self.place_items(new_map, r)
            # place traps
            self.place_traps(new_map, r)
            # place secrets

    def place_items(self, new_map, new_room):
        max_items = get_max_value_for_floor(settings.max_items_by_floor, self.dungeon.dlevel)
        number_of_items = random.randint(0, max_items)

        items = get_entities_at_random(
            db.item_chances, number_of_items, self.dungeon.dlevel
        )

        for entity in items:
            x, y = new_room.random_point_inside()
            # We don't care if they stack on the map
            spawn(entity, new_map, x, y)

    def place_monsters(self, new_map, new_room):
        new_monster = self.difficulty_specific_monster(
            self.dungeon.dlevel,
            self.player.level.current_level
        )
        x = random.randint(new_room.x1 + 1, new_room.x2 - 2)
        y = random.randint(new_room.y1 + 1, new_room.y2 - 2)

        # Don't spawn them on top of each other.
        if not new_map.get_actor_at(x, y):
            spawn(new_monster, new_map, x, y)

    def place_traps(self, new_map, new_room):
        x = random.randint(new_room.x1 + 1, new_room.x2 - 2)
        y = random.randint(new_room.y1 + 1, new_room.y2 - 2)

        # No traps on stairs!
        if not new_map.tiles[x][y] in [tiles.up_stairs, tiles.down_stairs]:
            new_trap = copy.deepcopy(src.db.bear_trap)
            new_map.add_entity(new_trap, x, y)


def make(entity_name):
    # Returns a new copy of the specified entity.
    if entity_name in db.actor_dict:
        # Create an Actor entity
        components = db.actor_dict.get(entity_name)
        components['name'] = entity_name
        return copy.deepcopy(Actor(**components))

        # Add the components common to all actors
        # components.update(db.actor_components)
        # Add the name component
        # components['name'] = entity_name
        # return Entity(**components)
        # return copy.deepcopy(db.actor_dict[entity_name])

    if entity_name in db.item_dict:
        # Create an Item entity
        components = db.item_dict.get(entity_name)
        components['name'] = entity_name
        return copy.deepcopy(Item(**components))

        # return copy.deepcopy(db.item_dict[entity_name])

    raise ValueError(f"'{entity_name}' is not a valid Entity!")


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