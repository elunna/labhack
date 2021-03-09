from src import rendering, settings
from src.base_handler import BaseEventHandler
from src.handlers import MainGameHandler, PopupMsgHandler, MapDebugHandler
from src.setup_game import load_game, new_game
import tcod
import traceback


class MainMenuHandler(BaseEventHandler):
    """Handle the main menu rendering and input."""

    def on_render(self, renderer):
        """Render the main menu on a background image."""
        rendering.render_main_menu(renderer.root)

    def ev_keydown(self, event):
        # Event handler for main menu.

        if event.sym in (tcod.event.K_q, tcod.event.K_ESCAPE):
            raise SystemExit()
        elif event.sym == tcod.event.K_c:
            try:
                return MainGameHandler(
                    load_game(settings.save_file)
                )
            except FileNotFoundError:
                return PopupMsgHandler(
                    self,
                    "No saved game to load."
                )
            except Exception as exc:
                traceback.print_exc()  # Print to stderr.
                return PopupMsgHandler(
                    self,
                    f"Failed to load save:\n{exc}"
                )

        elif event.sym == tcod.event.K_n:
            return MainGameHandler(new_game())
        elif event.sym == tcod.event.K_g:
            # Generate random maps
            return MapDebugHandler(self)

        return None