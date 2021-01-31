import exceptions
import input_handlers
import logger
import render_functions
import settings
import setup_game
import tcod
import traceback

log = logger.get_logger(__name__)


def main():
    renderer = render_functions.Renderer()

    # Our first event handler is the Main Menu handler.
    handler = input_handlers.MainMenuHandler()
    log.debug('Created first handler: MainMenuHandler')

    # Game loop
    log.debug('Entering game loop')
    while True:
        renderer.root.clear()
        # root_console.clear()

        # on_render just tells the Engine class to call its render method, using the given renderer.
        handler.on_render(renderer=renderer)

        # Draw the screen
        renderer.context.present(renderer.root)

        """ Finally, applications should wrap a try/except block around the main
            application code to send any exceptions through the logging interface
            instead of just to stderr.  This is known as a global try catch handler.
            It should not be where you handle all your exception logging, you should
            continue to plan for exceptions in try catch blocks at necessary points
            in your code as a rule of thumb.
        """
        try:
            for event in tcod.event.wait():
                renderer.context.convert_event(event)
                handler = handler.handle_events(event)

        except Exception:  # Handle exceptions in game.
            # TODO: Check that this doesn't go at the end of the block
            traceback.print_exc()  # Print error to stderr.
            log.debug(traceback.format_exc())

            # Then print the error to the message log.
            if isinstance(handler, input_handlers.EventHandler):
                handler.engine.msg_log.add_message(traceback.format_exc())

        except exceptions.QuitWithoutSaving:
            log.debug('exceptions.QuitWithoutSaving')
            raise
        except SystemExit:  # Save and Quit
            log.debug('exceptions.SystemExit')
            save_game(handler, settings.save_file)
            raise
        except BaseException:  # Save on any other unexpected exception
            log.debug('exceptions.BaseException')
            save_game(handler, settings.save_file)
            raise


def save_game(handler, filename):
    # TODO: Remove this function? Is it needed?
    """If the current event handler has an active Engine then save it."""
    if isinstance(handler, input_handlers.EventHandler):
        setup_game.save_as(handler.engine, filename)
        # handler.engine.save_as(filename)
        log.info("Game saved.")


if __name__ == "__main__":
    main()
