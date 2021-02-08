from actions.actions import Action
from src import exceptions


class TakeStairsAction(Action):
    def perform(self):
        """ Take the stairs, if any exist at the entity's location. """
        if (self.entity.x, self.entity.y) == self.engine.game_map.downstairs_location:
            self.engine.game_world.generate_floor()

            self.msg = "You descend the staircase."
        else:
            raise exceptions.Impossible("There are no stairs here.")