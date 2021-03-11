import traceback
import tcod
import time
from src import color, logger
from src import exceptions
from src import handlers
from src import rendering
from src import settings

log = logger.setup_logger(__name__)


def main():
    # Our first event handler is the Main Menu handler.
    handler = handlers.MainMenuHandler()
    renderer = rendering.Renderer()

    # Game loop
    while True:
        renderer.root.clear()

        # on_render just tells the Engine class to call its render method, using the given console.
        handler.on_render(renderer=renderer)

        # Draw the screen
        renderer.context.present(renderer.root)

        try:
            engine = getattr(handler, "engine", None)
            if engine:
                # Handle Behaviors/AI's
                if engine.player.ai:
                    handle_ai(engine, handler)
                    continue  # Skip the input and present.

                # Handle auto-states
                if engine.player.states.autopilot:
                    log.debug('Player Auto-State Activated ----------------')
                    action = engine.handle_auto_states(engine.player)
                    handler.handle_action(action)
                    time.sleep(settings.AUTO_DELAY)
                    continue  # Skip the input and present.

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
            if isinstance(handler, handlers.EventHandler):
                handler.engine.msglog.add_message(
                    traceback.format_exc(), color.error
                )
        except BaseException:  # Save on any other unexpected exception
            save_game(handler, settings.save_file)
            raise


def handle_ai(engine, handler):
    log.debug('Player AI Activated ----------------')
    if engine.player.ai.can_perform():
        # time.sleep(settings.AUTO_DELAY)
        action = engine.player.ai.yield_action()

        if not handler.handle_action(action):
            engine.player.ai = None
            log.debug('Player AI OFF ----------------')
    else:
        log.debug('Player AI OFF ----------------')
        engine.player.ai = None


def save_game(handler, filename):
    """If the current event handler has an active Engine then save it."""
    if isinstance(handler, handlers.EventHandler):
        handler.engine.save_as(filename)
        print("Game saved.")


if __name__ == "__main__":
    main()
