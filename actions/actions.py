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
