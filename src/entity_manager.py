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
        for e in args:
            self.add_entity(e)

    def add_stackable(self, e):
        # Option: Allow passing in qty?
        # Assume that the entity already has the desired stack size?
        # Requires stacks to be split before they are added.

        # Is there a matching entity?
        for f in self.entities:
            if f.is_similar(e):
                # Found twin
                return f.stackable.merge_stack(e)

        # If it is Non-stackable, or it doesn't have another stack to join, just add like normal.
        # Return false and let the add_entity function do it's work?
        return False

    def rm_entity(self, e):
        if e in self.entities:
            if "stackable" in e:
                self.rm_stackable(e)
                return

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



    def rm_stackable(self, e, qty):
        # Verify is it stackable? (already checked in rm_entity?)
        # Is the the entity in there?  (confirmed in rm_entity?)

        #       Split the stack
        #       result = e.item.split_stack(qty)

        #       If the stack is empty, we'll remove it from the set.
        #       if e.item.size == 0:
        #           self.entities.remove(e)

        #       return result  # Return the resulting new stack

        # If it is not stackable, or if the qty would wipe out the stack, handle it normally?
        #   self.entities.remove(e)
        #   e.x, e.y = -1, -1  # Update coordinates (-1 is unlatched since it's not a valid map index)
        #   e.parent = None  # Update the parent before ditching it.
        #   return e  # Return the entity

        # return None   # If the operation failed, return nothing.
        pass
