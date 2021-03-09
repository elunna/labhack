import copy

import components.consumable
from . import gamemap
from . import room
from . import tiles
from . import db
import numpy as np
import random
import tcod

from .utils import distance


def hide_corridors(new_map):
    # Add hidden corridors.
    # For now, we'll add x hidden corridors, where x is the number of rooms divided by 2.
    qty = len(new_map.rooms) // 2
    for i in range(qty):
        x, y = new_map.get_random_unoccupied_tile()  # Unpack an (x, y) tuple
        if new_map.tiles[x, y] == tiles.floor:
            new_map.place(copy.deepcopy(db.hidden_corridor), x, y)


def hide_doors(new_map):
    # Hide doors
    door_tiles = new_map.get_all_tiles_of(tiles.door)
    for x, y in door_tiles:
        # 10% of doors are hidden
        if random.random() > .10:
            continue
        # Hide all doors
        hidden_door = copy.deepcopy(db.hidden_door)
        new_map.place(hidden_door, x, y)  # Need to place it before adding the consumable!

        hidden_door.add_comp(consumable=components.consumable.CamoflaugeConsumable(hidden_door, x, y))


def add_closets(new_map):
    # Added random closets
    CLOSET_CHANCE = 10
    for r in new_map.rooms:
        if random.randint(1, CLOSET_CHANCE) == 1:
            all_doors = r.get_all_possible_doors()
            # Pick a random one. If it works, great, otherwise just skip.
            draw_door(new_map, random.choice(all_doors))


def dig_path(new_map, path):
    """Digs a preformed path in the map and converts all the coordinates in the path to floor tiles."""
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
        draw_door(new_map, d)


def draw_door(new_map, d):
    """Creates a single door in the map. First, verifies that the door has appropriate neighbor tiles,
    draws the door, then creates the closet outside the door.
    """
    if new_map.valid_door_neighbors(d.room, d.x, d.y):
        new_map.tiles[d.x, d.y] = tiles.door

        # Has the closet been drawn yet?
        closet_x, closet_y = d.closet()
        if new_map.tiles[closet_x, closet_y] == tiles.wall:
            # Dig out the closet
            new_map.tiles[closet_x, closet_y] = tiles.floor


def draw_room(new_map, new_room):
    """Draws all the tiles in a new room. Consists of the walls, corners, and inner floors.
    We also calculate if the the room will be lit or not and set the lit tiles as needed.
    """
    # Dig out this rooms inner area.
    new_map.tiles[new_room.inner] = tiles.room_floor

    # No dark rooms until level 5,
    # after level 5, chance of a dark room is (dlevel * 2%)
    dark_chance = new_map.dlevel * 2

    if new_map.dlevel < 5:
        new_map.lit[new_room.full_slice] = True

    elif random.randint(0, 100) > dark_chance:
        # light up the entire room
        new_map.lit[new_room.full_slice] = True

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
            # first connector didn't work.
            path = create_Astar_path_to(new_map, closet1_x, closet1_y, closet2_x, closet2_y)
            connected = valid_path(new_map, path)

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
        return True

    return False


def connecting_algorithm(new_map):
    """ Connects all the rooms in a map with a minimum spanning tree then performs an extra round
    of connections to make the  map easier to traverse.."""
    edges = min_spanning_tree_for_rooms(new_map.rooms)
    for room1, room2 in edges:
        connect_room_to_room(new_map, room1, room2)

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
    """Generates a diagonal path from one point to another on the map."""
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


def generate_map(max_rooms, room_min_size, room_max_size, map_width, map_height, max_distance, difficulty):
    """ Generate a new dungeon map with rooms, corridors, and stairs."""
    new_map = gamemap.GameMap(map_width, map_height, dlevel=difficulty)

    # Create all the rooms
    generate_rooms(
        new_map=new_map,
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        max_distance=max_distance,
    )

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

    # Closets, hidden stuff, traps, etc.
    hide_corridors(new_map)
    hide_doors(new_map)
    add_closets(new_map)

    return new_map


def generate_random_room(map_width, map_height, min_size, max_size):
    """Creates a room with random size and position."""
    room_width = random.randint(min_size, max_size)
    room_height = random.randint(min_size, max_size)

    x = random.randint(0, map_width - room_width - 1)
    y = random.randint(0, map_height - room_height - 1)

    return room.Room(x, y, room_width, room_height)


def generate_rooms(new_map, max_rooms, room_min_size, room_max_size, max_distance=50):
    """Generates a set of rooms for a new map. We will not allow overlapping of rooms so we will try
    max_tries times until we either have the full set of max_rooms or have exhausted our tries.
    """
    max_tries = 100
    tries = 0

    while tries < max_tries and len(new_map.rooms) < max_rooms:
        tries += 1
        new_room = generate_random_room(
            map_width=new_map.width,
            map_height=new_map.height,
            min_size=room_min_size,
            max_size=room_max_size
        )

        # Run through the other rooms and perform a few checks

        # Does this room intersect with another?
        if any(new_room.intersects(other_room) for other_room in new_map.rooms):
            continue  # This room intersects, so go to the next attempt.

        # Is the room further than the max distance allowed between rooms?
        if any(True for other in new_map.rooms
               if distance(*new_room.center, *other.center) > max_distance):  # Double unpacking FTW!
            continue

        # Label the room to match it's index in new_map.rooms
        label = len(new_map.rooms)
        new_room.label = label

        # Add this room to the map's list.
        new_map.rooms.append(new_room)


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
    """ Walks along a path and makes sure it doesn't dig out anything important. """
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
