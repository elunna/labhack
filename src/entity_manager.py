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

    def add_entity(self, e: Entity) -> bool:
        """ Takes an Entity and adds it to the set of entities. If the EntityManager was initialized with a
        required component (like "item"), we'll check to make sure only those entities are added. We also
        will not add identical entities to the set.

        :param e: The Entity to add.
        :return: True if addition was successful, False otherwise.
        """
        # Validation
        if self.required_comp and self.required_comp not in e:
            raise ValueError(f'EntityManager requires {self.required_comp} component for entities!')

        if "stackable" in e:
            return self.add_item(e)

        if self.is_full():  # Can't add if the container is full
            return False

        elif e in self.entities:  # Not desirable to add a duplicate item to a set...
            print(f"{e.name} already in EM.")
            return False

        e.parent = self  # Set the parent

        self.entities.add(e)
        return True

    def add_item(self, e: Entity, qty: int = 0):
        # if "item" not in e:
        #     raise ValueError(f'add_item requires item component for entities!')

        if self.required_comp and self.required_comp not in e:
            raise ValueError(f'EntityManager requires {self.required_comp} component for entities!')

        if qty < 0:
            raise ValueError("add_entity requires qty to have positive integer!")

        # Stackables can bypass the capacity if they have a match.
        if "stackable" in e:
            if qty == 0:  # use full stack size
                qty = e.stackable.size

            # Is there a matching entity?
            twin = self.get_similar(e)

            if twin:  # Found match we can add the stack to
                twin.stackable.merge_stack(e, qty)
                if e.stackable.size == 0:
                    e = twin  # If e was depleted, we'll chance it's reference to the stack it merged into
                return True

            # If full, return False
            if self.is_full():
                return False

            # No match
            if qty == e.stackable.size:
                # Full stack: Just add the reference
                e.parent = self  # Set the parent
                self.entities.add(e)  # Add the new stack to the inventory.
                return True

            # Split the source stack according to the qty
            print('split stack')
            add_me = e.stackable.split_stack(qty)
            add_me.parent = self  # Set the parent
            self.entities.add(add_me)  # Add the new stack to the inventory.
            return True

        if self.is_full():  # Can't add if the container is full
            return False

        # Not stackable, just add the item as normal.
        e.parent = self  # Set the parent

        self.entities.add(e)
        return True

    def add_entities(self, *args):
        """ Adds a variable number of entities to the set."""
        for e in args:
            self.add_entity(e)

    def rm_entity(self, e: Entity):
        """ Removes an entity from the set. """
        if e in self.entities:
            self.entities.remove(e)
            e.parent = None
            return e
        return None

    def rm_item(self, e: Entity, qty: int = 0):
        if qty < 0:
            raise ValueError("rm_entity requires qty 0 or greater (0 = full stack for stackables)")

        if "stackable" in e:
            if qty > e.stackable.size:
                raise ValueError("rm_entity received qty greater than the entitys stack size!")

            twin = self.get_similar(e)
            if twin:  # Found match we can add the stack to
                if qty == 0 or qty == twin.stackable.size:
                    # Just return the same object
                    self.entities.remove(twin)
                    twin.parent = None  # Reset parent.
                    return twin

                # No twin, and it's a partial split.
                result = twin.stackable.split_stack(qty)

                if twin.stackable.size == 0:  # If the stack is empty, remove it.
                    self.entities.remove(twin)

                result.parent = None  # Reset parent.
                return result
            return None

        # Non stackable item was passed in
        if qty > 1:
            raise ValueError("rm_entity received qty greater than the entitys stack size!")

        return self.rm_entity(e)  # Just handle it as a regular entity

    def rm_entities(self, *args):
        """ Removes a variable amount of entities from the set."""
        for e in args:
            self.rm_entity(e)

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
        # optional x, y args for locating items at coordinates?
        # raise NotImplementedError()
        """ Searches for entities that match most of the components and values of the given entity.
            The purpose of this method is mostly for finding matching stackable items.

        :param e: The entity we want to match.
        :return: The first matching entity we find.
        """
        for f in self.entities:
            # Needs to match name and coordinates to be similar
            if f.name == e.name:
                if f.x == e.x and f.y == e.y:
                    return f
        return None
