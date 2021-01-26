import traceback
import tcod

import src.input_handlers
from src import color, exceptions, input_handlers, settings


def main():
    # Specify font for tileset
    tileset = tcod.tileset.load_tilesheet(
        path=settings.tileset,
        columns=32,
        rows=8,
        charmap=tcod.tileset.CHARMAP_TCOD
    )

    # Our first event handler is the Main Menu handler.
    handler = src.input_handlers.MainMenuHandler()

    # Create the screen
    # Good info on how to use this:
    # https://python-tcod.readthedocs.io/en/latest/tcod/context.html
    with tcod.context.new_terminal(
        settings.screen_width,
        settings.screen_height,
        tileset=tileset,
        title=settings.title,
        vsync=True,
        renderer=tcod.RENDERER_SDL2,  # Fix green lines on Windows
    ) as context:
        # The "order" argument affects the order of our x and y variables in
        # numpy (an underlying library that tcod uses). By default, numpy
        # accesses 2D arrays in [y, x] order, which is fairly unintuitive. By
        # setting order="F", we can change this to be [x, y] instead.
        root_console = tcod.Console(settings.screen_width, settings.screen_height, order="F")

        # Game loop
        while True:
            root_console.clear()

            # on_render just tells the Engine class to call its render method, using the given console.
            handler.on_render(console=root_console)

            # Draw the screen
            context.present(root_console)

            try:
                for event in tcod.event.wait():
                    context.convert_event(event)
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
        handler.engine.save_as(filename)
        print("Game saved.")


if __name__ == "__main__":
    main()
