import tcod

from handlers.handlers import AskUserHandler
from src import rendering, color


class LevelUpHandler(AskUserHandler):
    """ PAUSED: For now this function is on hold until a more advanced skill tree
        is developed. When a level up is triggered, we will instead give a boost
        to a random stat.
    """
    TITLE = "Level Up"

    def on_render(self, renderer):
        super().on_render(renderer)
        rendering.render_levelup_menu(renderer.root, self.engine, self.TITLE)

    def ev_keydown(self, event):
        player = self.engine.player
        key = event.sym
        index = key - tcod.event.K_a

        if 0 <= index <= 2:
            if index == 0:
                player.level.increase_max_hp()
            elif index == 1:
                player.level.increase_strength()
            else:
                player.level.increase_ac()
        else:
            self.engine.msglog.add_message("Invalid entry.", color.invalid)

            return None

        return super().ev_keydown(event)

    def ev_mousebuttondown(self, event):
        """ Don't allow the player to click to exit the menu, like normal.  """
        return None