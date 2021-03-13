from . import settings, utils
from . import tiles
from .entity import Entity
from .entity_manager import EntityManager
from .room import Room
import numpy as np
import random


class GameMap(EntityManager):
    """ Manages the tiles and rooms in a map. Also keeps track of important map info like the stairs,
    doors, rooms, and room coordinates.
    """
    def __init__(self, width, height, fill_tile=tiles.wall, dlevel=1):
        super().__init__()
        self.engine = None  # This can be set later if needed
        self.width, self.height = width, height
        self.rooms = []  # Start with an empty list of rooms.
        self.doors = []  # Empty list of doors, helps in map generation.
        self.downstairs_location = (-1, -1)
        self.upstairs_location = (-1, -1)
        self.room_coords = None
        self.dlevel = dlevel  # difficulty level

        # create a 2D array, filled with the same values: walls.
        self.tiles = np.full((width, height), fill_value=fill_tile, order="F")

        # Tiles the player can currently see
        self.visible = np.full((width, height), fill_value=False, order="F")

        # Tiles the player has seen before
        self.explored = np.full((width, height), fill_value=False, order="F")

        # Track which tiles are light
        self.lit = np.full((width, height), fill_value=False, order="F")

        self.lighters = {}  # Tracks floor tiles which "light up" adjacent walls.

    @property
    def gamemap(self):
        """Direct reference to self. Other Entities will use this via their parent referene.

        :return: A reference to this map.
        """
        return self

    @property
    def actors(self):
        """ Iterate over this maps living actors."""
        yield from (e for e in self.has_comp("fighter") if e.is_alive)

    @property
    def items(self):
        """ Iterate over this maps items."""
        yield from (e for e in self.has_comp("item"))

    def in_bounds(self, x, y):
        """Returns True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def get_names_at(self, x, y):
        """ Returns a string of all the names of entities at the given location.
        We filter out hidden entities so the player cannot cheat with tooltips.
        We also format the list so be sorted, capitalized, and separated by commas.

        :param x: The x coordinate
        :param y: The y coordinate
        :return: A list of entity names.
        """
        if not self.in_bounds(x, y) or not self.visible[x, y]:
            return ""
        # Filter out hidden
        entities = [e for e in self.entities if e.x == x and e.y == y]
        names = [str(e) for e in entities if "hidden" not in e]

        # Testig this...
        # names = [str(e) for e in self.filter(x=x, y=y) if "hidden" not in e]

        # Format nicely, the sort makes it easier to test.
        sorted_names = sorted(n.capitalize() for n in names)
        return ", ".join(sorted_names)

    def walkable(self, x, y):
        """ Lets us know if the given location on the map is walkable by actors (ie: floor)

        :param x: The x coordinate
        :param y: The y coordinate
        :return: True if the tile is walkable, False if not.
        """
        return self.in_bounds(x, y) and self.tiles["walkable"][x, y]

    def room_coordinates(self):
        """ Creates a dict of coordinate keys and room values so we have an easy reference
            to see what coordinates belong to a room - and a quick check to see if they don't.
        """
        return {p: r for r in self.rooms for p in r.all_coords()}

    @staticmethod
    def tiles_around(x, y, radius):
        """ Returns a set of the coordinates around the given location, at a distance of radius.

        :param x: The x coordinate of the location
        :param y: The y coordinate of the location
        :param radius: How far out from the location we want the tile "perimeter" to be.
        :return: A set of coordinates.

        ex: radius 2 at (2, 2) - returns all the coordinates marked by x
        # 0 1 2 3 4 5
        0 x x x x x
        1 x . . . x
        2 x . @ . x
        3 x . . . x
        4 x x x x x
        """
        length = (radius * 2) + 1
        # Create a helper Rect so we can use it's perimeter.
        temp_rect = Room(x - radius, y - radius, length, length)
        return temp_rect.perimeter()

    def get_entities_within(self, x, y, radius):
        """Returns all visible actors within a radius from x, y"""
        actors = set()
        for actor in self.actors:
            visible = self.visible[actor.x, actor.y]
            close = utils.distance(actor.x, actor.y, x, y) <= radius
            if close and visible:
                actors.add(actor)
        return actors

    def valid_door_neighbors(self, room, x, y):
        """ Checks if the tiles around the point allow for placing a door (and more importantly, a closet)
            If valid, returns the coordinates for the closet space outside the door.
        """
        # First obvious check that the door will occupy part of the perimeter (but not a corner)
        if not room.valid_door_loc(x, y):
            return False

        facing = room.direction_facing(x, y)

        # Is it flanked by room walls to east and west (if facing north or south)?
        if facing in ['N', 'S']:
            # east
            dx, dy = settings.CARDINAL_DIR['E']
            if self.tiles[x + dx][y + dy] not in tiles.room_walls:
                return False
            # west
            dx, dy = settings.CARDINAL_DIR['W']
            if self.tiles[x + dx][y + dy] not in tiles.room_walls:
                return False

        # Is it flanked by room walls to north and south (if facing east or west)?
        elif facing in ['E', 'W']:
            # north
            dx, dy = settings.CARDINAL_DIR['N']
            if self.tiles[x + dx][y + dy] not in tiles.room_walls:
                return False
            # south
            dx, dy = settings.CARDINAL_DIR['S']
            if self.tiles[x + dx][y + dy] not in tiles.room_walls:
                return False

        # Does it have a "closet" space outside directly outside of the door that is not part of another room?
        dx, dy = settings.CARDINAL_DIR[facing]
        closet_x, closet_y = x + dx, y + dy

        # Is this a valid tile?
        if not self.in_bounds(closet_x, closet_y):
            return False

        # Is it wall or floor (both are valid)
        if not self.tiles[closet_x][closet_y] in [tiles.wall, tiles.floor]:
            return False
        return True

    def get_nearest_unconnected_room(self, room):
        """ Searches from the center of a room to find the next nearest room. Only returns
        the found room if it is unconnected to the source room. Uses tiles_around to look
        for a tiles that belong to rooms and keeps pushing outward until we find a room that
        is not connected to this room.

        :param room: The room to start searching from
        :return: A room if we are able to find one, or None.
        """
        x, y = room.center

        min_radius = 3  # Required to create the minimum sized Rect.

        for r in range(min_radius, self.height):
            # Get all the tiles in the new radius
            surrounding_tiles = self.tiles_around(x, y, r)

            for st in surrounding_tiles:
                # Check each tile and see if it belongs to a room.
                result = self.room_coords.get(st)
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

    def on_edge_of_map(self, x, y):
        """ Checks if a coordinate is on the edge of the map perimeter.
        returns True if it is, False otherwise.
        """
        if x == 0 or y == 0:
            return True
        elif x == (self.width - 1) or y == (self.height - 1):
            return True

        return False

    def get_random_unoccupied_tile(self):
        """ Attempts to find a tile on the map that is open for an actor to occupy - so it must
        be walkable and non-occupied by any other actors or blocking entities.

        :return: The coordinates of the open tile, or None if nothing was open.
        """
        # Get every walkable tile, choose a random one until one is found.
        floors = [(x, y) for x in range(self.width)
                  for y in range(self.height) if self.walkable(x, y)]

        while floors:
            result = random.choice(floors)
            if not self.get_actor_at(*result):
                return result
            floors.remove(result)
        return None

    def get_all_tiles_of(self, tiletype):
        """ Returns a list of coordinates for all tiles which map the given tile."""
        return [(x, y) for x in range(self.width)
                for y in range(self.height)
                if self.tiles[x, y] == tiletype]

    def get_actor_at(self, x, y):
        """ Looks for an actor at the given coordinates and returns it if it exists. """
        # Returns an ALIVE actor at the specified location.
        for a in self.actors:
            if a.x == x and a.y == y:
                return a
        return None

    def get_trap_at(self, x, y):
        """ Looks for an trap at the given coordinates and returns it if it exists. """
        traps = self.filter("trap", x=x, y=y)
        if traps:
            return traps.pop()
        return None

    def place(self, e: Entity, x: int, y: int):
        """ Wrapper for add_entity with coordinates."""
        e.x, e.y = x, y
        if self.add_entity(e):
            return True
        return False

    def get_visible_tiles(self):
        return {(x, y) for x in range(self.width) for y in range(self.height) if self.visible[x, y]}
