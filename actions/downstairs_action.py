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
            new_level_generated = False

            # Do we have a level below us yet?
            if self.dungeon.dlevel == len(self.dungeon.map_list):
                # Generate a new level and add it to the map_list
                self.dungeon.generate_floor()
                new_level_generated = True

            self.dungeon.move_downstairs(self.entity)

            if new_level_generated:
                # This solves the annoying problem of the player appearing on top of other monsters.
                # We have to populate after placing the player.
                self.dungeon.populate_map(self.dungeon.dlevel)

            self.msg = "You descend the stairs."
        else:
            raise exceptions.Impossible("There are no stairs here.")
