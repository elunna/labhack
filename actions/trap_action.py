from actions.actions import Action


class TrapAction(Action):
    def __init__(self, entity, trap, target_xy=None):
        super().__init__(entity)
        self.trap = trap
        if not target_xy:
            target_xy = entity.x, entity.y
        self.target_xy = target_xy

    @property
    def target_actor(self):
        """Return the actor at this actions destination."""
        return self.entity.gamemap.get_actor_at(*self.target_xy)

    def perform(self):
        """Invoke the items ability, this action will be given to provide context."""
        if self.trap.consumable:
            # TODO: Get msg
            return self.trap.consumable.activate(self)