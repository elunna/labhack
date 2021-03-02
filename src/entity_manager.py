from src.entity import Entity

NO_LIMIT = 0


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
        return self.capacity == NO_LIMIT or len(self) == self.capacity
