import numpy as np

from . import tiles
from . import factory
from . import gamemap
from . import rect
from . import settings
import random
import tcod

# Break up methods
# mk_rooms: Create a set of rooms and dig them out of a map
# tunnel_between
# Place entity?


def place_items(room, dungeon, floor_number):
    number_of_items = random.randint(
        0, get_max_value_for_floor(settings.max_items_by_floor, floor_number)
    )

    items = get_entities_at_random(
        factory.item_chances, number_of_items, floor_number
    )

    for entity in items:
        x, y = room.random_point_inside()
        # x = random.randint(room.x1 + 1, room.x2 - 2)
        # y = random.randint(room.y1 + 1, room.y2 - 2)
        # We don't care if they stack on the map
        entity.spawn(dungeon, x, y)


def place_monsters(room, dungeon, floor_number):
    number_of_monsters = random.randint(
        0, get_max_value_for_floor(settings.max_monsters_by_floor, floor_number)
    )

    monsters = get_entities_at_random(
        factory.enemy_chances, number_of_monsters, floor_number
    )

    for entity in monsters:
        x = random.randint(room.x1 + 1, room.x2 - 2)
        y = random.randint(room.y1 + 1, room.y2 - 2)

        # Don't spawn them on top of each other.
        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            entity.spawn(dungeon, x, y)


def generate_map(max_rooms, room_min_size, room_max_size, map_width, map_height, engine):
    """Generate a new dungeon map with rooms, corridors, and stairs.."""
    new_map = gamemap.GameMap(engine, map_width, map_height)

    # Create all the rects for the rooms
    generate_rooms(new_map, max_rooms, room_min_size, room_max_size)

    # Use some algorithm to connect the rooms.
    # Requirement: All rooms must be connected somehow and reachable by some means.
    connecting_algorithm_1(new_map)

    # Put the upstair in the first room generated
    center_of_first_room = new_map.rooms[0].center
    new_map.tiles[center_of_first_room] = tiles.up_stairs
    new_map.upstairs_location = center_of_first_room

    # Put the downstair in the last room generated
    center_of_last_room = new_map.rooms[-1].center
    new_map.tiles[center_of_last_room] = tiles.down_stairs
    new_map.downstairs_location = center_of_last_room
    return new_map


def connecting_algorithm_1(new_map):
    # Connect all the rooms with corridors
    for i, room in enumerate(new_map.rooms):
        if i > 0:  # All rooms after the first.
            # Dig out a tunnel between this room and the previous one.
            for x, y in tunnel_between(new_map.rooms[i - 1].center, room.center):
                # Don't draw over room floor tiles
                if new_map.tiles[x, y] != tiles.room_floor:
                    new_map.tiles[x, y] = tiles.floor


def populate_map(new_map, engine):
    # Place entities
    for room in new_map.rooms:
        # Populate the room with monsters and items
        place_monsters(room, new_map, engine.game_world.current_floor)
        place_items(room, new_map, engine.game_world.current_floor)


def generate_rooms(new_map, max_rooms, room_min_size, room_max_size):
    for r in range(max_rooms):
        new_room = mk_room(new_map, room_min_size, room_max_size)

        # Run through the other rooms and see if they intersect with this one.
        if any(new_room.intersects(other_room) for other_room in new_map.rooms):
            continue  # This room intersects, so go to the next attempt.

        # If there are no intersections then the room is valid.

        # Dig out this rooms inner area.
        new_map.tiles[new_room.inner] = tiles.room_floor

        # Draw walls
        for point in new_room.horz_walls():
            new_map.tiles[point] = tiles.room_horz_wall
        for point in new_room.vert_walls():
            new_map.tiles[point] = tiles.room_vert_wall

        # Draw corners (must be ordered after walls)
        new_map.tiles[new_room.ne_corner] = tiles.room_ne_corner
        new_map.tiles[new_room.nw_corner] = tiles.room_nw_corner
        new_map.tiles[new_room.se_corner] = tiles.room_se_corner
        new_map.tiles[new_room.sw_corner] = tiles.room_sw_corner

        # Add this room to the map's list.
        new_map.rooms.append(new_room)


def mk_room(new_map, min_size, max_size):
    room_width = random.randint(min_size, max_size)
    room_height = random.randint(min_size, max_size)

    x = random.randint(0, new_map.width - room_width - 1)
    y = random.randint(0, new_map.height - room_height - 1)

    return rect.Rect(x, y, room_width, room_height)


def tunnel_between(start, end, twist=0):
    """ Return an L-shaped tunnel between these two points.
        start: Tuple[int, int],
        end: Tuple[int, int]
        returns Iterator[Tuple[int, int]]:
    """
    x1, y1 = start
    x2, y2 = end

    if twist == 0:
        twist = random.randint(1, 2)

    if twist == 1:  # 50% chance.
        corner_x, corner_y = x2, y1  # Move horizontally, then vertically.
    else:
        corner_x, corner_y = x1, y2  # Move vertically, then horizontally.

    # Generate the coordinates for this tunnel.
    # tcod includes a function in its line-of-sight module to draw Bresenham
    # lines. While we’re not working with line-of-sight in this case, it
    # still proves useful to get a line from one point to another. In this case,
    # we get one line, then another, to create an “L” shaped tunnel. .tolist()
    # converts the points in the line into, as you might have already guessed,
    # a list.

    coordinates = []
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        coordinates.append((x, y))
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        coordinates.append((x, y))
    return coordinates


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
