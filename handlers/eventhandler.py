from handlers.base_handler import BaseEventHandler
# from handlers.handlers import GameOverHandler, MainGameHandler  # Below to avoid circular import
from src import settings, logger

log = logger.setup_logger(__name__)


class EventHandler(BaseEventHandler):
    """ This takes in Actions and performs the appropriate game events.
        EventDispatch is a class that allows us to send an event to its proper
        method based on what type of event it is.
    """

    def __init__(self, engine):
        self.engine = engine

    def handle_events(self, event):
        """Handle events for input handlers with an engine."""
        action_or_state = self.dispatch(event)
        player = self.engine.player

        if isinstance(action_or_state, BaseEventHandler):
            return action_or_state

        if self.handle_action(action_or_state):
            # A valid action was performed.
            if not player.is_alive:
                # The player was killed sometime during or after the action.
                from handlers.handlers import GameOverHandler
                return GameOverHandler(self.engine)

            # If the player leveled up, handle it.
            self.engine.check_level()


            # Handle Behaviors/AI's
            while self.engine.player.ai:
                log.debug('Player AI Activated ----------------')

                if self.engine.player.ai.can_perform():
                    action = self.engine.player.ai.yield_action()

                    if not self.handle_action(action):
                        self.engine.player.ai = None
                        log.debug('Player AI OFF ----------------')

                else:
                    log.debug('Player AI OFF ----------------')

            # Handle auto-states
            while self.engine.player.states.autopilot:
                log.debug('Handling Player auto-states')
                action = self.engine.handle_auto_states(player)
                self.handle_action(action)

            from handlers.handlers import MainGameHandler
            return MainGameHandler(self.engine)  # Return to the main handler.
        return self

    def handle_action(self, action):
        """ Handle actions returned from event methods.
            Returns True if the action will advance a turn.
        """
        if self.engine.handle_action(action):  # Successful action completed.
            log.debug(f'########## TURN {self.engine.turns} COMPLETE ########## ')
            log.debug('')
            # Here - we will evaluate the player's energy
            # Use up a turn worth of energy
            self.engine.player.energymeter.burn_turn()

            self.engine.update_fov()

            # If the player doesn't have enough energy for another turn, we'll
            # run the enemy turns.
            if self.engine.player.energymeter.burned_out():
                # TODO: Move all this crap to an end_of_turn method in Engine

                # Handle end-of-turn states ..Decrease timeouts on states
                self.engine.reduce_timeouts()

                # Increment turns
                self.engine.turns += 1

                # All actors get an energy recharge every turn
                self.engine.add_energy()

                self.engine.handle_enemy_turns()

                # Random chance at summoning new dungeon monster.
                self.engine.generate_monster()

                # Check if player regenerates
                self.engine.player.regeneration.activate(self.engine.turns)

                return True
        return False

    def ev_mousemotion(self, event):
        # if self.engine.game_map.in_bounds(event.tile.x, event.tile.y):
            # self.engine.mouse_location = event.tile.x, event.tile.y

        # Correct for msg_panel offset
        if self.engine.game_map.in_bounds(event.tile.x, event.tile.y - settings.msg_panel_height):
            self.engine.mouse_location = event.tile.x, event.tile.y

    def on_render(self, renderer):
        # render_map(renderer, self.engine.game_map)
        self.engine.render(renderer)