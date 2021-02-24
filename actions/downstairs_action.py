from actions.actions import Action
from src import exceptions


class DownStairsAction(Action):
    def perform(self):
        """ Take the stairs, if any exist at the entity's location. """
        player_location = (self.entity.x, self.entity.y)
        stair_location = self.engine.game_map.downstairs_location

        if player_location == stair_location:
            # TODO: This logic should go in Dungeon

            # Remove the player from the map entities
            # self.engine.game_map.entities.remove(self.entity)  # place does this

            # Remove player reference from the map
            self.engine.game_map.player = None

            self.engine.dungeon.generate_floor()

            # Place the player on the new floor
            new_map = self.engine.game_map
            # new_map.entities.add(self.entity)  # place does this

            # Place player on upstair.
            # TODO: Replace this place function
            self.entity.place(*new_map.upstairs_location, new_map)
            new_map.player = self.entity

            self.msg = "You descend the staircase."
        else:
            raise exceptions.Impossible("There are no stairs here.")
