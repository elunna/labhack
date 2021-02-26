import copy
import math
from components.component import Component
from src import utils


class Entity(object):
    """ A generic object to represent players, enemies, items, etc. An Entity is composed of Components.
        The Entity also makes sure that each Component's parent is correctly set to the Entity it is added
        to and unset when it is removed. We use a dictionary to manage the entity's Components.
    """
    def __init__(self, **kwargs):
        self.components = {}
        self.add_comp(**kwargs)  # Add any components that were passed in at creation

        # Every Entity should have a parent component included.
        self.add_comp(parent=None)

    def __str__(self):
        if 'name' in self:
            return self.name
        return 'Unnamed'

    def __contains__(self, component):
        return component in self.components

    def __getattr__(self, name):
        if name in self.components:
            return self.components[name]

        raise AttributeError('Entity has no component with attribute {}'.format(name))

    def __setattr__(self, key, value):
        if key == 'components':
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

    @property
    def gamemap(self):
        return self.parent.gamemap

    def add_comp(self, **kwargs):
        for k, v in kwargs.items():
            self.components[k] = v

            # Set the components parent!
            if isinstance(v, Component):
                v.parent = self

    def rm_comp(self, component):
        if component in self.components:
            self.components.pop(component)

            # Unset the components parent!
            if isinstance(component, Component):
                component.parent = None

            return True
        return False

    def move(self, dx, dy):
        # Move the entity by a given amount
        self.x += dx
        self.y += dy

    def distance(self, x, y):
        """Return the distance between the current entity and the given (x, y) coordinate.
        """
        return utils.distance(self.x, self.y, x, y)
