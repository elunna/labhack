from actions.actions import Action
from src import exceptions


class TakeStairsAction(Action):
    def perform(self):
        """ Take the stairs, if any exist at the entity's location. """
        player_location = (self.entity.x, self.entity.y)
        stair_location = self.engine.game_map.downstairs_location

        if player_location == stair_location:

            # Currently procgen.generate_map takes care of this...
            # self.engine.game_map.entities.remove(self.entity)

            # Remove player from current map
            self.engine.game_map.player = None

            self.engine.game_world.generate_floor()

            self.msg = "You descend the staircase."
        else:
            raise exceptions.Impossible("There are no stairs here.")
