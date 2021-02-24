from .actions import Action


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
        # return self.engine.game_map.blocking_entity_at(*self.dest_xy)
        # TODO: Make sure this doesn't breakstuff!
        return self.entity.gamemap.blocking_entity_at(*self.dest_xy)

    @property
    def target_actor(self):
        """Return the actor at this actions destination."""
        # return self.engine.game_map.get_actor_at(*self.dest_xy)
        # TODO: Make sure this doesn't breakstuff!
        return self.entity.gamemap.get_actor_at(*self.dest_xy)

    def perform(self):
        raise NotImplementedError()