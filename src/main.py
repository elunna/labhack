import traceback
import tcod
from src import color
from src import exceptions
from src import input_handlers
from src import settings
from src import setup_game


class Renderer:
    """ Handle all the rendering details that the engine requires."""
    def __init__(self):
        # Specify font for tileset
        tileset = tcod.tileset.load_tilesheet(
            path=settings.tileset,
            columns=32,
            rows=8,
            charmap=tcod.tileset.CHARMAP_TCOD
        )

        # Create the screen
        # Good info on how to use this:
        # https://python-tcod.readthedocs.io/en/latest/tcod/context.html

        # To make this easier to put into a class, I removed the with/as context usage - Erik
        self.context = tcod.context.new_terminal(
            settings.screen_width,
            settings.screen_height,
            tileset=tileset,
            title=settings.title,
            vsync=True,
            renderer=tcod.RENDERER_SDL2,  # Fix green lines on Windows
        )

        # The "order" argument affects the order of our x and y variables in
        # numpy (an underlying library that tcod uses). By default, numpy
        # accesses 2D arrays in [y, x] order, which is fairly unintuitive. By
        # setting order="F", we can change this to be [x, y] instead.
        self.root = tcod.Console(
            settings.screen_width,
            settings.screen_height,
            order="F"
        )

        # Define separate panels for the map, messages, and stats.
        self.msg_panel = tcod.Console(
            width=settings.screen_width,
            height=settings.msg_panel_height
        )
        self.map_panel = tcod.Console(
            width=settings.map_width,
            height=settings.map_height,
            order="F",
        )
        self.stat_panel = tcod.Console(
            width=settings.screen_width,
            height=settings.stat_panel_height
        )


def main():
    renderer = Renderer()

    # Our first event handler is the Main Menu handler.
    handler = input_handlers.MainMenuHandler()

    # Game loop
    while True:
        renderer.root.clear()
        # root_console.clear()

        # on_render just tells the Engine class to call its render method, using the given renderer.
        handler.on_render(renderer=renderer)

        # Draw the screen
        renderer.context.present(renderer.root)

        try:
            for event in tcod.event.wait():
                renderer.context.convert_event(event)
                handler = handler.handle_events(event)

        except Exception:  # Handle exceptions in game.
            # TODO: Check that this doesn't go at the end of the block
            traceback.print_exc()  # Print error to stderr.

            # Then print the error to the message log.
            if isinstance(handler, input_handlers.EventHandler):
                handler.engine.message_log.add_message(
                    traceback.format_exc(), color.error
                )

        except exceptions.QuitWithoutSaving:
            raise
        except SystemExit:  # Save and Quit
            save_game(handler, settings.save_file)
            raise
        except BaseException:  # Save on any other unexpected exception
            save_game(handler, settings.save_file)
            raise


def save_game(handler, filename):
    """If the current event handler has an active Engine then save it."""
    if isinstance(handler, input_handlers.EventHandler):
        setup_game.save_as(handler.engine, filename)
        # handler.engine.save_as(filename)
        print("Game saved.")


if __name__ == "__main__":
    main()
