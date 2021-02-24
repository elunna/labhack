class Action:
    """ The template for a game action that affects gameplay."""
    def __init__(self, entity):
        super().__init__()
        self.entity = entity
        self.msg = ''

    @property
    def engine(self):
        """Return the engine this action belongs to."""
        return self.entity.gamemap.engine

    def perform(self):
        """ Perform this action with the objects needed to determine its scope.

            `self.engine` is the scope this action is being performed in.
            `self.entity` is the object performing the action.

            This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class ActionWithDirection(Action):
    def __init__(self, entity, dx, dy):
        super().__init__(entity)
        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self):
        """Returns this actions destination as Tuple[int, int]."""
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self):
        """Return the blocking entity at this actions destination.."""
        return self.entity.gamemap.blocking_entity_at(*self.dest_xy)

    @property
    def target_actor(self):
        """Return the actor at this actions destination."""
        return self.entity.gamemap.get_actor_at(*self.dest_xy)

    def perform(self):
        raise NotImplementedError()