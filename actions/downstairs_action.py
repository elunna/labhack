from actions.actions import Action
from src import exceptions


class DownStairsAction(Action):
    def __init__(self, entity, dungeon):
        super().__init__(entity)
        self.dungeon = dungeon

    def perform(self):
        """ Take the stairs, if any exist at the entity's location. """
        player_location = (self.entity.x, self.entity.y)
        stair_location = self.dungeon.current_map.downstairs_location

        if player_location == stair_location:
            self.dungeon.move_downstairs()
            self.msg = "You descend the stairs."
        else:
            raise exceptions.Impossible("There are no stairs here.")
