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
        """ Returns the string representation of the entity.
            If the entity is stackable, it will check if there is more than one and return
            a plural version, otherwise it will just be the name.
        """
        if 'name' in self:
            # Money is a strange exception to formatting.
            # TODO: Maybe entities can have a formatting method?
            if self.name == "money":
                return f"${self.stackable.size}"

            if "stackable" in self and self.stackable.size > 1:
                return f"{self.stackable.size} {self.name}s"
            return self.name
        return 'Unnamed'

    def __contains__(self, component):
        """Returns True if the entity contains the component, False otherwise."""
        return self.has_comp(component)

    def __getattr__(self, name):
        """Returns the value of the specified component."""
        if name in self.components:
            return self.components[name]

        raise AttributeError('Entity has no component with attribute {}'.format(name))

    def __setattr__(self, key, value):
        """Sets a component to a value. This should also set the parent of the component."""
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

    def is_similar(self, other):
        """Compares another entity to this one to see if their components and values match.
        The purpose of this method is to enable easy identfication of entities that can stack together so
        we ignore stackable because stack sizes might be different, but objects are still the same.

        Ignore parent because stackable might have a parent that is the GameMap that wants to go into
        an Inventory, and we don't want to exclude them on that basis.
        """
        return self.name == other.name
        # for k, v in self.components.items():
        #     if k in ["stackable", "parent"]:
        #         continue
        #     if other.components.get(k) != self.components.get(k):
        #         return False
        # return True

    @property
    def gamemap(self):
        """Returns a reference to this entity's parent's gamemap."""
        return self.parent.gamemap

    def add_comp(self, **kwargs):
        """Adds a set of component/value pairs to the collection of components.
            If the component is a valid Component - we also set the parent.
        """
        for k, v in kwargs.items():
            self.components[k] = v

            # Set the components parent!
            if isinstance(v, Component):
                v.parent = self

    def rm_comp(self, component):
        """Removes the specified component from the entity. If it is a valid Component, it also resets the parent.
            Returns True if the operation succeeded, False otherwise.
        """
        if component in self.components:
            self.components.pop(component)

            # Unset the components parent!
            if isinstance(component, Component):
                component.parent = None

            return True
        return False

    def has_comp(self, component):
        """Returns True if the entity has the specified component, False otherwise. """
        return component in self.components

    def has_compval(self, **kwargs):
        for k, v in kwargs.items():
            if self.components.get(k) != v:
                return False
        return True

    def move(self, dx, dy):
        # Move the entity by a given amount
        self.x += dx
        self.y += dy

    def distance(self, x, y):
        """Return the distance between the current entity and the given (x, y) coordinate.
        """
        return utils.distance(self.x, self.y, x, y)

    def is_player(self):
        """Returns True if this entity represents the player, otherwise returns False. """
        return self.has_comp("player")
