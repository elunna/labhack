from actions.actions import Action


class ItemAction(Action):
    def __init__(self, entity, item, target_xy=None):
        super().__init__(entity)
        self.item = item
        if not target_xy:
            target_xy = entity.x, entity.y
        self.target_xy = target_xy

    @property
    def target_actor(self):
        """Return the actor at this actions destination."""
        # return self.engine.game_map.get_actor_at(*self.target_xy)
        return self.entity.gamemap.get_actor_at(*self.target_xy)

    def perform(self):
        """Invoke the items ability, this action will be given to provide context."""
        if self.item.consumable:
            # TODO: Get msg
            # self.item.consumable.activate(self)
            return self.item.consumable.activate(self)