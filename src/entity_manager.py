from src.entity import Entity

NO_LIMIT = -1


class EntityManager:
    def __init__(self, required_comp=None, capacity=NO_LIMIT):
        self.entities = set()
        # REQUIRED_COMPONENTS: item for items, fighter for fighters, etc.
        self.required_comp = required_comp

        # Capacity lets us define a limit to the number of entities allowed in the set.
        # A value of 0 dicates no limit!
        self.capacity = capacity

    def __contains__(self, item):
        return self.has_entity(item)

    def __len__(self):
        return len(self.entities)

    def add_entity(self, e: Entity) -> bool:
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
        for e in args:
            self.add_entity(e)

    def add_stackable(self, e):
        # Should we allow passing in qty?  Harder...
        # Or should we assume that the entity already has the desired stack size? Easier...
        # Means that we will be splitting something else before passing it in.

        # Verify the entity is a stackable.
        # Stackables can bypass the capacity if they have a match.

        # Is there a matching entity?
        #       GameMap: same location?
        #       Inventory: location -1 -1?

        #       Add to the existing stackables stacksize.
        #       matching_item.stacksize += e.item.stacksize

        #       Erase the original stack? might not be necessary
        #       e.item.deplete_stack(e.item.stacksize)
        #       return True if it worked.

        # If it is Non-stackable, or it doesn't have another stack to join, just add like normal.
        # Return false and let the add_entity function do it's work?
        pass

    def rm_stackable(self, e, qty):
        # Verify is it stackable? (already checked in rm_entity?)
        # Is the the entity in there?  (confirmed in rm_entity?)

        #       Split the stack
        #       result = e.item.split_stack(qty)

        #       If the stack is empty, we'll remove it from the set.
        #       if e.item.stacksize == 0:
        #           self.entities.remove(e)

        #       return result  # Return the resulting new stack

        # If it is not stackable, or if the qty would wipe out the stack, handle it normally?
        #   self.entities.remove(e)
        #   e.x, e.y = -1, -1  # Update coordinates (-1 is unlatched since it's not a valid map index)
        #   e.parent = None  # Update the parent before ditching it.
        #   return e  # Return the entity

        # return None   # If the operation failed, return nothing.
        pass

    def rm_entity(self, e):
        if e in self.entities:
            self.entities.remove(e)
            e.parent = None
            return e
        return None

    def rm_entities(self, *args):
        for e in args:
            self.rm_entity(e)

    def has_entity(self, e):
        return e in self.entities

    def get_by_name(self, name):
        # Returns a set of entities that match the specified name
        return {e for e in self.entities if e.name == name}

    def has_comp(self, comp):
        # Returns a set of entities that contain the component
        return {e for e in self.entities if comp in e}

    # def has_comps(self, *args):

    def filter(self, **kwargs):
        """Returns a set of entities that contain specific components and values.
        Filters out any entities that do not contain the components with the values."""
        entities_copy = self.entities.copy()

        for e in self.entities:
            if not e.has_compval(**kwargs):
                entities_copy.remove(e)
        return entities_copy

    def is_empty(self):
        return len(self) == 0

    def is_full(self):
        if self.capacity == NO_LIMIT:
            return False  # Never full if there is no limit
        return len(self) == self.capacity
