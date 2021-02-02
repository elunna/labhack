from settings import max_items_by_floor, max_monsters_by_floor
import factories
import game_map
import logger
import random
import rectangle
import tcod
import tile_types

log = logger.get_logger(__name__)


def generate_map(
        max_rooms,
        room_min_size,
        room_max_size,
        map_width,
        map_height,
        floor_number):
    """Generate a new dungeon map."""
    log.debug('Generating new game map...')

    # Create new GameMap, filled with walls
    new_map = game_map.GameMap(map_width, map_height)
    rooms = []

    center_of_last_room = (0, 0)

    for r in range(max_rooms):
        new_room = mk_room(new_map, room_min_size, room_max_size)

        # Run through the other rooms and see if they intersect with this one.
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue  # This room intersects, so go to the next attempt.

        # If there are no intersections then the room is valid.
        dig_room(new_map, new_room)

        if len(rooms) == 0:
            center_of_first_room = new_room.center

        else:  # All rooms after the first.
            # Dig out a tunnel between this room and the previous one.
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                new_map.tiles[x, y] = tile_types.floor

            center_of_last_room = new_room.center

        # Populate the room with monsters
        place_entities(new_room, new_map, floor_number)

        # Finally, append the new room to the list.
        rooms.append(new_room)

    # Put the upstair in the first room
    new_map.tiles[center_of_first_room] = tile_types.up_stairs
    new_map.upstairs_location = center_of_first_room

    # Put the downstair in the last room generated
    new_map.tiles[center_of_last_room] = tile_types.down_stairs
    new_map.downstairs_location = center_of_last_room

    return new_map


def mk_room(dungeon, room_min_size, room_max_size):
    room_width = random.randint(room_min_size, room_max_size)
    room_height = random.randint(room_min_size, room_max_size)

    x = random.randint(0, dungeon.width - room_width - 1)
    y = random.randint(0, dungeon.height - room_height - 1)

    return rectangle.Rectangle(x, y, room_width, room_height)


def dig_room(gamemap, new_room):
    # Dig out this rooms inner area.
    gamemap.tiles[new_room.inner] = tile_types.floor


def tunnel_between(start, end, twist=0):
    """ Return an L-shaped tunnel between these two points.
        start: Tuple[int, int],
        end: Tuple[int, int]
        turn=0: 50% chance of either vertical or horizontal turn first
        turn=1: Always move horizontally first
        turn=2: Always move vertical first

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
    # We can return generators to make this even better.

    # TODO: The angle corner is repeated, can we improve this?
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y


def place_entities(room, dungeon, floor_number):
    log.debug('Placing entities in room...')
    number_of_monsters = random.randint(
        0, factories.get_max_value_for_floor(max_monsters_by_floor, floor_number)
    )

    number_of_items = random.randint(
        0, factories.get_max_value_for_floor(max_items_by_floor, floor_number)
    )

    monsters = factories.get_entities_at_random(
        factories.enemy_chances, number_of_monsters, floor_number
    )
    items = factories.get_entities_at_random(
        factories.item_chances, number_of_items, floor_number
    )

    for entity in monsters:
        # -2 so that things don't get stuck in walls.
        x = random.randint(room.x1 + 1, room.x2 - 2)
        y = random.randint(room.y1 + 1, room.y2 - 2)

        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            factories.monsters[entity].spawn(dungeon, x, y)

    for entity in items:
        # -2 so that things don't get stuck in walls.
        x = random.randint(room.x1 + 1, room.x2 - 2)
        y = random.randint(room.y1 + 1, room.y2 - 2)

        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            entity.spawn(dungeon, x, y)

