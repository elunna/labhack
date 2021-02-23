from . import factory
from . import gamemap
from . import rect
from . import settings
from . import tiles
import math
import numpy as np
import random
import tcod


def connect_2_doors(new_map, door1, door2):
    # To connect the doors, we have to connect the closets!
    x1, y1 = door1.closet()
    x2, y2 = door2.closet()

    # Choose a method of creating the tunnel:
    path = get_L_path((x1, y1), (x2, y2))

    # Draw a diagonal
    # path = diagonal_tunnel(start, end):

    for x, y in path:
        # Stop drawing if we run into room corners.
        if new_map.tiles[x, y] in tiles.room_corners:
            return False

        # Do not draw over inner room floors
        if new_map.tiles[x, y] == tiles.room_floor:
            return False

    # Dig out a tunnel between this room and the previous one.
    for x, y in path:
        new_map.tiles[x, y] = tiles.floor

    return True


def connect_room_to_room(new_map, room1, room2):
    connected = False
    # Find all the pairs of doors that face eachother.
    facing_doors = room1.match_facing_doors(room2)
    door1, door2 = None, None

    if facing_doors:
        closest_pair = get_closest_pair_of_doors(facing_doors)

        pair = get_valid_pair_of_doors(facing_doors)
        if not pair:
            pair = closest_pair

        door1, door2 = pair
        connected = connect_2_doors(new_map, door1, door2)

    if not connected:
        # Either: we don't have facing doors, or the first connector didn't work.

        # We'll allow a lot of tries before we give up
        tries = 0
        while not connected and tries < 100:
            tries += 1

            # Get a random set of doors
            door1 = rect.Door(room1, *room1.random_door_loc())
            door2 = rect.Door(room2, *room2.random_door_loc())

            if not new_map.valid_door_location(room1, door1.x, door1.y):
                continue
            if not new_map.valid_door_location(room2, door2.x, door2.y):
                continue

            connected = dig_Astar_path(new_map, door1, door2)

    if connected:
        # Dig out adjacent doors
        if distance(door1.x, door1.y, door2.x, door2.y) == 1:
            # If the doors are next to eachother, just leave it as floor.
            new_map.tiles[door1.x, door1.y] = tiles.floor
            new_map.tiles[door2.x, door2.y] = tiles.floor
        else:
            new_map.doors.append(door1)
            new_map.doors.append(door2)

        # Add the rooms to each-other's list of connections
        room1.connections.append(room2.label)
        room2.connections.append(room1.label)


def connecting_algorithm(new_map):
    # First connect rooms with a minimum spanning tree.
    edges = min_spanning_tree_for_rooms(new_map.rooms)
    for room1, room2 in edges:
        connect_room_to_room(new_map, room1, room2)

    # We'll perform a second round of connections to make the map easier to traverse.
    # Try to add 1/2 of the room count as extra connections.
    extra_connections = len(new_map.rooms) // 2

    for i in range(extra_connections):
        room1 = random.choice(new_map.rooms)
        room2 = get_nearest_unconnected_room(new_map, room1)
        connect_room_to_room(new_map, room1, room2)


def dig_Astar_path(new_map, door1, door2):
    # Get the closets outside the doors
    x1, y1 = door1.closet()
    x2, y2 = door2.closet()

    # A* path
    path = get_path_to(new_map, x1, y1, x2, y2)
    # If there is only a single point - the path is not able to complete
    if len(path) == 1:
        return False

    # Chck the path
    for point in path:
        x, y = point

        # We won't allow drawing over room walls or doors.
        if new_map.tiles[x, y] in tiles.room_walls:
            return False

    # Draw the path
    for point in path:
        new_map.tiles[point] = tiles.floor
    return True


def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def draw_doors(new_map):
    """ Drawing doors needs to be a separate activity done last after corridors, because if it's combined with
    corridor drawing, there are conflicts in where doors and floor appear.
    """
    for d in new_map.doors:
        valid_door = True
        for direction in settings.CARDINAL_DIR.values():
            dx, dy = direction

            # Check around for other doors.
            if new_map.tiles[d.x + dx][d.y + dy] == tiles.door:
                # Oh no, a door is adjacent! Abort mission!
                valid_door = False
                continue

        if valid_door:
            new_map.tiles[d.x, d.y] = tiles.door

            # Is the closet wall yet?
            closet_x, closet_y = d.closet()
            if new_map.tiles[closet_x, closet_y] == tiles.wall:
                # Dig out the closet
                new_map.tiles[closet_x, closet_y] = tiles.floor


def generate_map(max_rooms, room_min_size, room_max_size, map_width, map_height, engine):
    """Generate a new dungeon map with rooms, corridors, and stairs.."""
    new_map = gamemap.GameMap(engine, map_width, map_height)

    # Create all the rects for the rooms
    generate_rooms(new_map, max_rooms, room_min_size, room_max_size)

    # Create the room coordinates for easy reference.
    new_map.room_coords = new_map.room_coordinates()

    # Connect the rooms with corridors
    connecting_algorithm(new_map)

    # Place doors
    draw_doors(new_map)

    # Put the upstair in the first room generated
    center_of_first_room = new_map.rooms[0].center
    new_map.tiles[center_of_first_room] = tiles.up_stairs
    new_map.upstairs_location = center_of_first_room

    # Put the downstair in the last room generated
    center_of_last_room = new_map.rooms[-1].center
    new_map.tiles[center_of_last_room] = tiles.down_stairs
    new_map.downstairs_location = center_of_last_room
    return new_map


def generate_random_room(map_width, map_height, min_size, max_size):
    room_width = random.randint(min_size, max_size)
    room_height = random.randint(min_size, max_size)

    x = random.randint(0, map_width - room_width - 1)
    y = random.randint(0, map_height - room_height - 1)

    return rect.Rect(x, y, room_width, room_height)


def generate_rooms(new_map, max_rooms, room_min_size, room_max_size):
    for r in range(max_rooms):
        new_room = generate_random_room(
            map_width=new_map.width,
            map_height=new_map.height,
            min_size=room_min_size,
            max_size=room_max_size
        )

        # Run through the other rooms and see if they intersect with this one.
        if any(new_room.intersects(other_room) for other_room in new_map.rooms):
            continue  # This room intersects, so go to the next attempt.

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

        # Label the room to match it's index in new_map.rooms
        label = len(new_map.rooms)
        new_room.label = label

        # Add this room to the map's list.
        new_map.rooms.append(new_room)


def get_valid_pair_of_doors(matches):
    """ Iterates through a list of facing doors and picks until we find a valid choice.
    """
    while matches:
        pair = random.choice(matches)
        matches.remove(pair)
        door1, door2 = pair

        # We have to check that these are not lined up so that the closets are over-extended
        x_diff = abs(door1.x - door2.x)
        y_diff = abs(door1.y - door2.y)

        # Hopefully we only have to test one door to see if they are facing vertically or horizontally.
        # This is okay:
        # |    |   ---||---
        # --+---      ++
        # --+---      ||
        # |    |   ---||---

        # We don't want this
        # |    |   ---||---
        # --+---      +|
        # ---+--      |+
        # |    |   ---||---

        if door1.facing in ['S', 'N'] and y_diff == 1:
            # Vertical facing: If the y-difference is 1, the x-difference has to be 0 (aligned)
            if x_diff == 0:
                return pair
            continue

        if door1.facing in ['E', 'W'] and x_diff == 1:
            # Horizontal facing: If the x-difference is 1, the y-difference has to be 0 (aligned)
            if x_diff == 0:
                return pair
            continue

        # If the pair passes the above tests, it should be okay.
        return pair


def get_closest_pair_of_doors(matches):
    # Find the pair of doors that are the closest in distance.
    closest_pair = None
    record = 1000000  # Unlikely we'll see a distance larger than this...
    for pair in matches:
        door1, door2 = pair
        dist_between = distance(door1.x, door1.y, door2.x, door2.y)
        if dist_between < record:
            record = dist_between
            closest_pair = pair
    return closest_pair


def get_nearest_unconnected_room(new_map, room):
    # Use tiles_around to look for a tiles that belong to rooms.
    # Keep pushing outward until we find a room that is not connected to this room.
    x, y = room.center

    min_radius = 3  # Required to create the minimum sized Rect.

    for r in range(min_radius, new_map.height):
        # Get all the tiles in the new radius
        surrounding_tiles = new_map.tiles_around(x, y, r)

        for st in surrounding_tiles:
            # Check each tile and see if it belongs to a room.
            result = new_map.room_coords.get(st)
            if not result:
                continue
            # Make sure it's not the same room we are looking out from.
            if room.label == result.label:
                continue
            # Make sure it's not connected to this room already.
            if result.label in room.connections:
                continue

            # Passed all checks!
            return result


# noinspection PyTypeChecker
def get_L_path(start, end, twist=0):
    """ Return an L-shaped tunnel between these two points.
        If the lines are on the same x-axis or y-axis it will simply draw a straight line.
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
    # line-of-sight module: draws Bresenham lines.
    coordinates = []
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        coordinates.append((x, y))

    # There will be a duplicate value from the corner point, we want to remove this!
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist()[1:]:
        coordinates.append((x, y))
    return coordinates


def get_diagonal_path(start, end):
    # Generate the coordinates for this tunnel.
    # line-of-sight module: draws Bresenham lines.
    x1, y1 = start
    x2, y2 = end
    coordinates = []
    for x, y in tcod.los.bresenham((x1, y1), (x2, y2)).tolist():
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


def get_path_to(_map, start_x, start_y, dest_x, dest_y):
    """ Compute and return a path to the target position.
        If there is no valid path then returns an empty list.
        See components.ai.BaseAI.get_path_to for full comments.
    """
    cost = np.array(_map.tiles["diggable"], dtype=np.int8)

    # Create a graph from the cost array and pass that graph to a new pathfinder.
    graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=0)
    pathfinder = tcod.path.Pathfinder(graph)

    pathfinder.add_root((start_x, start_y))  # Start position.

    # Compute the path to the destination (remove starting point.)
    # path = pathfinder.path_to((dest_x, dest_y))[1:-1].tolist()
    path = pathfinder.path_to((dest_x, dest_y)).tolist()

    # Convert from List[List[int]] to List[Tuple[int, int]].
    # noinspection PyTypeChecker
    return [(index[0], index[1]) for index in path]


def min_spanning_tree_for_rooms(rooms):
    """ Connects all the rooms by using Prim's Algorithm
    :return: A list of all the edges (room to room connections)
    """
    edges = []
    visited = []
    unvisited = rooms[:]   # Copy all vertices to this list.

    # Random start point.
    start = unvisited[0]
    visited.append(start)
    unvisited.pop(0)  # Remove the start point from the unvisited list.

    while len(unvisited) > 0:
        record = 100000   # A very high number, maybe even max
        r_match = None
        u_match = None

        for r in visited:
            for u in unvisited:
                x1, y1 = r.center
                x2, y2 = u.center
                dist = distance(x1, y1, x2, y2)

                if dist < record:
                    record = dist
                    r_match = r
                    u_match = u

        edges.append((r_match, u_match))

        # Take the u_match out of unvisited and put it into visited.
        visited.append(u_match)
        unvisited.remove(u_match)

    return edges



def place_items(room, dungeon, floor_number):
    number_of_items = random.randint(
        0, get_max_value_for_floor(settings.max_items_by_floor, floor_number)
    )

    items = get_entities_at_random(
        factory.item_chances, number_of_items, floor_number
    )

    for entity in items:
        x, y = room.random_point_inside()
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


def populate_map(new_map, engine):
    for room in new_map.rooms:
        # Populate the room with monsters and items
        place_monsters(room, new_map, engine.game_world.current_floor)
        place_items(room, new_map, engine.game_world.current_floor)
