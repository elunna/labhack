class Action:
    """ The template for a game action. Every action has an entity that is performing it."""
    def __init__(self, entity):
        self.entity = entity
        self.msg = ''
        self.recompute_fov = False  # Use this for actions which require redrawing after.

    def __str__(self):
        """Returns the string representation of the action."""
        return self.__class__.__name__

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
    """Represents an Action that has a direction targets in any of the immediate 8 surrounding tiles."""
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
        dest_x, dest_y = self.dest_xy
        blockers = self.entity.gamemap.filter(
            x=dest_x, y=dest_y,
            blocks_movement=True
        )
        return blockers

    @property
    def target_actor(self):
        """Return the actor at this actions destination."""
        return self.entity.gamemap.get_actor_at(*self.dest_xy)

    def perform(self):
        """Invokes the actor to perform the action."""
        raise NotImplementedError()
