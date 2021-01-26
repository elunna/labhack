import copy
import math
from .settings import RenderOrder


class Entity:
    """ A generic object to represent players, enemies, items, etc."""
    # parent: GameMap
    # parent = None

    def __init__(
            self,
            parent=None,  # Should be GameMap
            x=0,
            y=0,
            char='?',
            color=(255, 255, 255),
            name='<Unnamed>',
            blocks_movement=False,
            render_order=RenderOrder.CORPSE,
    ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color  # color is a tuple
        self.name = name
        self.blocks_movement = blocks_movement
        self.render_order = render_order

        if parent:
            # If parent isn't provided now then than will be set later.
            self.parent = parent
            parent.entities.add(self)

    @property
    def gamemap(self):
        return self.parent.gamemap

    def move(self, dx, dy):
        # Move the entity by a given amount
        self.x += dx
        self.y += dy

    def spawn(self, gamemap, x, y):
        """Spawn a copy of this instance at the given location."""
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.parent = gamemap
        gamemap.entities.add(clone)
        return clone

    def place(self, x, y, gamemap=None):
        """Place this entity at a new location.  Handles moving across GameMaps."""
        self.x, self.y = x, y

        if gamemap:
            if hasattr(self, "parent"):  # Possibly uninitialized.
                if self.parent is self.gamemap:
                    self.gamemap.entities.remove(self)
            self.parent = gamemap
            gamemap.entities.add(self)

    def distance(self, x, y):
        """Return the distance between the current entity and the given (x, y) coordinate.
            Return as a float value.
        """
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
