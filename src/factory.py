import math
from . import settings, tiles
from . import db
import copy
import random
from .actor import Actor
from .entity import Entity
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
        """Adds monsters, items, traps, and features to the map."""
        new_map = self.dungeon.get_map(dlevel)
        for r in new_map.rooms:
            # Populate the room with monsters and items

            self.place_monsters(new_map, r)

            if random.random() < .50:
                # 50% chance of each room having items.
                self.place_items(new_map, r)

            if random.random() < .25:
                # 25% for each new room to have a trap
                self.place_traps(new_map, r)

            # place secrets

            self.place_money(new_map, r)

    def place_items(self, new_map, new_room):
        """Places a random amount of items in the new room."""
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
        """Places a random amount of monsters in the new room."""
        new_monster = self.difficulty_specific_monster(
            self.dungeon.dlevel,
            self.player.level.current_level
        )
        x, y = new_room.random_point_inside()

        # Don't spawn them on top of each other.
        not_occupied = not new_map.get_actor_at(x, y)
        not_upstairs = new_map.upstairs_location != (x, y)
        if not_occupied and not_upstairs:
            spawn(new_monster, new_map, x, y)

    def place_traps(self, new_map, new_room):
        """Places a random amount of traps in the new room."""
        x, y = new_room.random_point_inside()

        # No traps on stairs!
        if not new_map.tiles[x][y] in [tiles.up_stairs, tiles.down_stairs]:
            # Choose a random dungeon feature/trap
            new_trap = make(random.choice(list(db.dungeon_features.keys())))
            new_map.place(new_trap, x, y)

    def place_money(self, new_map, new_room):
        """Places a random amount of money in the new room."""
        x, y = new_room.random_point_inside()
        # 1d10 * level for the amount of the pile?
        money_pile = make("money")
        money_max = (self.dungeon.dlevel ** 2) * 10
        money_min = int(money_max * .1)
        money_pile.stackable.size = random.randint(money_min, money_max)

        new_map.place(money_pile, x, y)


def make(entity_name):
    """Generates entities from the db.py database of entities."""
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
    if entity_name in db.dungeon_features:
        components = db.dungeon_features.get(entity_name)
        components['name'] = entity_name
        return copy.deepcopy(Entity(**components))

    if entity_name == "money":
        m = copy.deepcopy(Item(**db.money))
        # This is a crude hack, but it should work to make the inventory character always $
        m.item.last_letter = "$"
        return m

    raise ValueError(f"'{entity_name}' is not a valid Entity!")


def spawn(entity_name, gamemap, x, y):
    """Spawn a copy of the entity at the given map and location.
    Returns the instance of the entity.
    """
    e = make(entity_name)
    gamemap.place(e, x, y)
    return e


def get_max_value_for_floor(weighted_chances_by_floor, floor):
    """Uses the weighted chances table to calculate the maximum number of entities to generate
    (per room) for the current floor."""
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
