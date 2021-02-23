from . import factory
from . import gamemap
from . import room
from . import settings
from . import tiles
import math
import numpy as np
import random
import tcod


def dig_path(new_map, path):
    # Dig out a pre-determined path
    for x, y in path:
        new_map.tiles[x, y] = tiles.floor


def door_distance_dict(room1, room2):
    """Create a dict of door pairs (keys) and their distances apart (values) """
    pair_dict = {}
    for a in room1.get_all_possible_doors():
        for b in room2.get_all_possible_doors():
            dist_between = distance(a.x, a.y, b.x, b.y)
            pair_dict[(a, b)] = dist_between
    return pair_dict


def draw_doors(new_map):
    """ Drawing doors needs to be a separate activity done last after corridors, because if it's combined with
    corridor drawing, there are conflicts in where doors and floor appear.
    """
    for d in new_map.doors:
        if new_map.valid_door_neighbors(d.room, d.x, d.y):
            new_map.tiles[d.x, d.y] = tiles.door

            # Has the closet been drawn yet?
            closet_x, closet_y = d.closet()
            if new_map.tiles[closet_x, closet_y] == tiles.wall:
                # Dig out the closet
                new_map.tiles[closet_x, closet_y] = tiles.floor


def draw_room(new_map, new_room):
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


def connect_room_to_room(new_map, room1, room2):
    """ Connects two rooms by choosing a pair of doors and connecting their closets with a path.
        Returns True if the room was connected successfully, False otherwise.
    """
    print("---------------------------------------------------------------")
    # First, find a pair of doors that is suitable for connecting.
    # Start with a list of all the possible door pairs between room1 and room2
    # Create a dict with distances as values
    door_pairs = door_distance_dict(room1, room2)

    # Thin them down with any non-valid pairs (edge of map, adjacent)
    door_pairs = {
        k: y for k, y in door_pairs.items()
        if valid_pair_of_doors(new_map, k[0], k[1])
    }

    # Create a sub-dict of facing pairs.
    facing_pairs = {k: y for k, y in door_pairs.items() if k[0].facing_other(k[1])}

    door1, door2 = None, None  # prevents annoying Pycharm warning.
    path = []  # prevents annoying Pycharm warning.
    # Loop until we discover a connected set of doors or we exhaust all of the door pairs.
    connected = False
    tries = 0
    while not connected and door_pairs:
        tries += 1
        if facing_pairs:
            # 20% of the time, use the closest facing pair.
            if random.random() < .2:
                # Use the most direct pair by default.
                next_pair = min(facing_pairs, key=facing_pairs.get)

            # The other 80%, get a random facing pair.
            else:
                next_pair = random.choice(list(facing_pairs.keys()))

            # Remove the pair from both dicts
            facing_pairs.pop(next_pair)
            door_pairs.pop(next_pair)

        else:
            # A* is our backup in case the facing doors don't exist.
            print('No facing pairs...')
            # Choose a random pair.
            next_pair = random.choice(list(door_pairs.keys()))

            # Remove the pair from the dict
            door_pairs.pop(next_pair)

        # We have a set of doors to work with
        door1, door2 = next_pair

        # To connect the doors, we have to connect the closets!
        closet1_x, closet1_y = door1.closet()
        closet2_x, closet2_y = door2.closet()

        # Try easiest path first.
        path = create_L_path((closet1_x, closet1_y), (closet2_x, closet2_y))
        connected = valid_path(new_map, path)

        if not connected:
            print(f'A* tunnel! {room1.label} to {room2.label}')
            # first connector didn't work.
            path = create_Astar_path_to(new_map, closet1_x, closet1_y, closet2_x, closet2_y)
            connected = valid_path(new_map, path)
        else:
            print(f'L tunnel! {room1.label} to {room2.label}')

    if connected:
        # Dig out the path
        dig_path(new_map, path)

        # Special case for doors that are right next to each other
        # TODO: We might be able to move this to draw_doors later...
        if distance(door1.x, door1.y, door2.x, door2.y) == 1:
            # Dig out as floor.
            new_map.tiles[door1.x, door1.y] = tiles.floor
            new_map.tiles[door2.x, door2.y] = tiles.floor
        else:
            new_map.doors.append(door1)
            new_map.doors.append(door2)

        # Add the rooms to each-other's list of connections
        room1.connections.append(room2.label)
        room2.connections.append(room1.label)
        print(f'{tries} tries')
        return True

    print("Could not connect rooms!")
    return False


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
        room2 = new_map.get_nearest_unconnected_room(room1)
        connect_room_to_room(new_map, room1, room2)


def create_Astar_path_to(_map, start_x, start_y, dest_x, dest_y):
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


def create_diagonal_path(start, end):
    # Generate the coordinates for this tunnel.
    # line-of-sight module: draws Bresenham lines.
    x1, y1 = start
    x2, y2 = end
    coordinates = []
    for x, y in tcod.los.bresenham((x1, y1), (x2, y2)).tolist():
        coordinates.append((x, y))
    return coordinates


# noinspection PyTypeChecker
def create_L_path(start, end, twist=0):
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


def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def generate_map(max_rooms, room_min_size, room_max_size, map_width, map_height, engine):
    """Generate a new dungeon map with rooms, corridors, and stairs.."""
    new_map = gamemap.GameMap(engine, map_width, map_height)

    # Create all the rooms
    generate_rooms(new_map, max_rooms, room_min_size, room_max_size)

    # Draw the rooms
    for r in new_map.rooms:
        draw_room(new_map, r)

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

    return room.Room(x, y, room_width, room_height)


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

        # Label the room to match it's index in new_map.rooms
        label = len(new_map.rooms)
        new_room.label = label

        # Add this room to the map's list.
        new_map.rooms.append(new_room)




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


def place_items(new_room, dungeon, floor_number):
    number_of_items = random.randint(
        0, get_max_value_for_floor(settings.max_items_by_floor, floor_number)
    )

    items = get_entities_at_random(
        factory.item_chances, number_of_items, floor_number
    )

    for entity in items:
        x, y = new_room.random_point_inside()
        # We don't care if they stack on the map
        entity.spawn(dungeon, x, y)


def place_monsters(new_room, dungeon, floor_number):
    number_of_monsters = random.randint(
        0, get_max_value_for_floor(settings.max_monsters_by_floor, floor_number)
    )

    monsters = get_entities_at_random(
        factory.enemy_chances, number_of_monsters, floor_number
    )

    for entity in monsters:
        x = random.randint(new_room.x1 + 1, new_room.x2 - 2)
        y = random.randint(new_room.y1 + 1, new_room.y2 - 2)

        # Don't spawn them on top of each other.
        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            entity.spawn(dungeon, x, y)


def populate_map(new_map, engine):
    for r in new_map.rooms:
        # Populate the room with monsters and items
        place_monsters(r, new_map, engine.game_world.current_floor)
        place_items(r, new_map, engine.game_world.current_floor)


def valid_pair_of_doors(new_map, door1, door2):
    """ This is a preliminary check to see if a pair of doors will work together.
        GameMap has a further check for surrounding tiles, but that is for post-corridor drawing.
        This checks that each door is not on the map edge, because then a closet would not be possible -
        or it would overrun to the opposite side of the map.
        This also checks that the alignment of the doors will not cause closet problems.

        This does NOT check the spaces around or next to the door.
    """

    # It can't be at the edge of the map
    if new_map.on_edge_of_map(door1.x, door1.y):
        return False
    if new_map.on_edge_of_map(door2.x, door2.y):
        return False

    # We have to check that these are not lined up (this results in closets that are over-extended)
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
            return True
        return False

    if door1.facing in ['E', 'W'] and x_diff == 1:
        # Horizontal facing: If the x-difference is 1, the y-difference has to be 0 (aligned)
        if y_diff == 0:
            return True
        return False

    # If it passed the above tests, it should be okay
    return True


def valid_path(new_map, path):
    """ Walks along a path and makes sure it doesn't dig out anything important.
    """
    # This takes care of A* paths that are only 1 sq long.
    if len(path) == 1:
        return False

    for x, y in path:
        # Stop drawing if we run into room corners.
        if new_map.tiles[x, y] in tiles.room_corners:
            return False

        # Do not draw over inner room floors
        if new_map.tiles[x, y] == tiles.room_floor:
            return False
    return True
