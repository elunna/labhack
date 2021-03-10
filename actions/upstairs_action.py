from actions.actions import Action
from src import exceptions
from src.settings import DUNGEON_TOP_LEVEL


class UpStairsAction(Action):
    """Represents an entity moving from a upstair tile to the previous level."""

    def __init__(self, entity, dungeon):
        super().__init__(entity)
        self.dungeon = dungeon

    def perform(self):
        """ Take the stairs, if any exist at the entity's location. """
        player_location = (self.entity.x, self.entity.y)
        stair_location = self.dungeon.current_map.upstairs_location

        if player_location == stair_location:

            # Do we have a level above us?
            if self.dungeon.dlevel == DUNGEON_TOP_LEVEL:
                raise exceptions.Impossible("Cannot go upstairs at top of dungeon!")

            self.dungeon.move_upstairs(self.entity)
            self.msg = "You ascend the stairs."
        else:
            raise exceptions.Impossible("There are no stairs here.")
