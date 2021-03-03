from src.entity import Entity

NO_LIMIT = -1


class EntityManager:
    """ Manages all the tasks involved with entities:
        * adding, removing, and querying
        The purpose of this class is to be inherited by something that works with entities, but
        has other responsibilities: like the GameMap, Inventory, or a container like a Chest.
    """
    def __init__(self, required_comp=None, capacity=NO_LIMIT):
        self.entities = set()
        # REQUIRED_COMPONENTS: item for items, fighter for fighters, etc.
        self.required_comp = required_comp

        # Capacity lets us define a limit to the number of entities allowed in the set.
        # A value of 0 dicates no limit!
        self.capacity = capacity

    def __contains__(self, item):
        """ Tells us if the item is in the set of entities."""
        return self.has_entity(item)

    def __len__(self):
        """ Tells us the number of entities in the set."""
        return len(self.entities)

    @property
    def actors(self):
        """ Iterate over this maps living actors."""
        yield from (e for e in self.has_comp("fighter") if e.is_alive)

    @property
    def items(self):
        """ Iterate over this maps items."""
        yield from (e for e in self.has_comp("item"))

    def add_entity(self, e: Entity) -> bool:
        """ Takes an Entity and adds it to the set of entities.
            If an entity is stackable, it will be handled a bit differently by the add_stackable method.
            We cannot add if the capacity is at full.
            If the EntityManager was initialized with a required component (like "item"), we'll check to make
            sure only those entities are added. We also will not add identical entities to the set.

        :param e: The Entity to add.
        :return: True if addition was successful, False otherwise.
        """
        # Stackables can bypass the capacity if they have a match.
        if "stackable" in e:
            if self.add_stackable(e):
                return True

        if self.is_full():
            return False
        if self.required_comp and self.required_comp not in e:
            raise ValueError(f'EntityManager requires {self.required_comp} component for entities!')
        if e in self.entities:
            return False

        e.parent = self  # Set the parent

        self.entities.add(e)
        return True

    def add_entities(self, *args):
        """ Adds a variable number of entities to the set."""
        for e in args:
            self.add_entity(e)

    def add_stackable(self, e):
        """ Adds a stackable entity to the set."""
        # Is there a matching entity?
        for f in self.entities:
            if f.is_similar(e):
                # Found match we can add the stack to
                return f.stackable.merge_stack(e)

        # If it is Non-stackable, or it doesn't have another stack to join, just add like normal.
        # Return false and let the add_entity function do it's work.
        return False

    def place(self, e, x, y):
        """ Wrapper for add_entity with coordinates."""
        if self.add_entity(e):
            e.x, e.y = x, y
            return True
        return False

    def rm_entity(self, e, qty=1):
        """ Removes an entity from the set. """
        if e in self.entities:
            if "stackable" in e:
                return self.rm_stackable(e, qty)
            elif qty > 1:
                raise ValueError("rm_entity received qty greater than 1 but without stackable!")
            self.entities.remove(e)
            e.parent = None
            return e
        return None

    def rm_entities(self, *args):
        """ Removes a variable amount of entities from the set."""
        for e in args:
            self.rm_entity(e)

    def rm_stackable(self, e, qty=1):
        """ Removes a stackable entity from the set - we can also specify a quantity
        to remove.
        """
        for f in self.entities:
            if f.is_similar(e):
                # Split the stack
                result = f.stackable.split_stack(qty)

                if e.stackable.size == 0:  # If the stack is empty, remove it.
                    self.entities.remove(e)

                # Return the resulting new stack
                return result
        return None

    def has_entity(self, e):
        """ Returns True if the entity is in the set, False if not."""
        return e in self.entities

    def get_by_name(self, name):
        """ Searches for an entity by name and returns a set of entities that match."""
        # Returns a set of entities that match the specified name
        return {e for e in self.entities if e.name == name}

    def has_comp(self, comp):
        """Searches for entities that contain the specified component and returns a set. """
        # Returns a set of entities that contain the component
        return {e for e in self.entities if comp in e}

    # def has_comps(self, *args):

    def filter(self, *args, **kwargs):
        """Returns a set of entities that contain specific components and component/value pairs.
        Filters out any entities that do not contain the components with the values.

        Example usage: filter("fighter", x=1, y=5)
            Returns all entities that are fighters that are at coordinates (1, 5)
        """
        entities_copy = self.entities.copy()

        for e in self.entities:
            # Check the component/value pairs passed in as **kwargs
            if not e.has_compval(**kwargs):
                entities_copy.remove(e)
                continue

            # Check the components passed in *args
            for comp in args:
                if comp not in e:
                    entities_copy.remove(e)
                    continue

        return entities_copy

    def is_empty(self):
        """ Returns True if the set of entities is empty, False if not."""
        return len(self) == 0

    def is_full(self):
        """ Returns True if the set of entities is full, False if not.
            If the capacity was initialized to NO_LIMIT (-1), this will always be False.
        """

        if self.capacity == NO_LIMIT:
            return False  # Never full if there is no limit
        return len(self) == self.capacity

    def get_similar(self, e):
        """ Searches for entities that match most of the components and values of the given entity.
            The purpose of this method is mostly for finding matching stackable items.

        :param e: The entity we want to match.
        :return: The first matching entity we find.
        """
        for f in self.entities:
            if f.is_similar(e):
                return e
        return None

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
