import traceback
import tcod

from handlers import eventhandler
from handlers import mainmenu_handler
from src import color
from src import exceptions
from src import rendering
from src import settings


def main():
    # Our first event handler is the Main Menu handler.
    handler = mainmenu_handler.MainMenuHandler()
    renderer = rendering.Renderer()

    # Game loop
    while True:
        renderer.root.clear()

        # on_render just tells the Engine class to call its render method, using the given console.
        handler.on_render(renderer=renderer)

        # Draw the screen
        renderer.context.present(renderer.root)

        try:
            for event in tcod.event.wait():
                renderer.context.convert_event(event)
                handler = handler.handle_events(event)

        except exceptions.QuitWithoutSaving:
            raise
        except SystemExit:  # Save and Quit
            save_game(handler, settings.save_file)
            raise
        except Exception:  # Handle exceptions in game.
            traceback.print_exc()  # Print error to stderr.

            # Then print the error to the message log.
            if isinstance(handler, eventhandler.EventHandler):
                handler.engine.msglog.add_message(
                    traceback.format_exc(), color.error
                )
        except BaseException:  # Save on any other unexpected exception
            save_game(handler, settings.save_file)
            raise


def save_game(handler, filename):
    """If the current event handler has an active Engine then save it."""
    if isinstance(handler, eventhandler.EventHandler):
        handler.engine.save_as(filename)
        print("Game saved.")


if __name__ == "__main__":
    main()
