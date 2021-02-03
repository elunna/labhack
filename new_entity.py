import copy
import math

class Entity(object):
    """ A generic object to represent players, enemies, items, etc.
        We use a dictionary to manage the entity's Components.
        A component must be of type: BaseComponent.
        All entities have some base info:
            x, y, char, name, color

        This structure with getattr and setattr allows us to access attributes
        of components easily from the entity, without subcalling the components
        all the time.
    """

    # parent: GameMap
    # parent = None

    def __init__(self, **kwargs):
        self.components = kwargs

    def __str__(self):
        if self.has_comp('name'):
            return self.name
        return 'Unnamed'

    def __getattr__(self, name):
        if name in self.components:
            return self.components[name]

        raise AttributeError('Entity has no component with attribute {}'.format(name))

    def __setattr__(self, key, value):
        if key == 'components':
            # self.components = value
            super().__setattr__('components', value)
        else:
            self.components[key] = value

    def __getstate__(self):
        """But if we try to pickle our d instance, we get RecursionError because
            of that __getattr__ which does the magic conversion of attribute
            access to key lookup. We can overcome that by providing the class
            with __getstate__ and __setstate__ methods.
            https://stackoverflow.com/questions/50156118/recursionerror-maximum-recursion-depth-exceeded-while-calling-a-python-object-w/50158865#50158865
        """
        return self.components

    def __setstate__(self, state):
        """See comment for __getstate__"""
        self.components = state

    def add_comp(self, **kwargs):
        for k, v in kwargs.items():
            self.components[k] = v

    def has_comp(self, component):
        if component in self.components:
            return True
        return False

    def rm_comp(self, component):
        if component in self.components:
            self.components.pop(component)
            return True
        return False


    @property
    def gamemap(self):
        # TODO: Deal with this, find reasonable usage or factor out.
        # Or check if parent is None first..
        return self.parent.gamemap

    def move(self, dx, dy):
        # Move the entity by a given amount
        self.x += dx
        self.y += dy

    def spawn(self, gamemap, x, y):
        """Spawn a copy of this instance at the given location."""
        # TODO: Move this to gamemap?
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.parent = gamemap
        gamemap.entities.add(clone)
        return clone

    def place(self, x, y, gamemap=None):
        """Place this entity at a new location.  Handles moving across GameMaps."""
        # TODO: Move this to gamemap?
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
        # TODO: Move this to gamemap?
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
