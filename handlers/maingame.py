import tcod

import actions.bump_action
import actions.downstairs_action
import actions.pickup_action
import actions.search_action
import actions.upstairs_action
import actions.wait_action
from components import ai
from handlers.eventhandler import EventHandler
from handlers.handlers import CharacterScreenHandler, HistoryHandler, InventoryActivateHandler, \
    InventoryDropHandler, LookHandler

# from handlers.handlers import HelpHandler  # Below to avoid circular import

from src.input_keys import MOVE_KEYS, WAIT_KEYS


class MainGameHandler(EventHandler):
    """ For reference, these are the event codes for tcod.
        https://python-tcod.readthedocs.io/en/latest/tcod/event.html
    """
    def ev_keydown(self, event):
        # A key was pressed, determine which key and create an appropriate action.
        action = None
        player = self.engine.player
        key = event.sym
        modifier = event.mod  # modifier keys like control, alt, or shift.
        # Shift modifiers
        if modifier & (tcod.event.KMOD_LSHIFT | tcod.event.KMOD_RSHIFT):
            if key in MOVE_KEYS:
                # Create new run behavior
                player.add_comp(ai=ai.RunAI(direction=MOVE_KEYS[key]))

                # The first move/bump action should get handled below
                if self.engine.player.ai.can_perform():
                    return player.ai.yield_action()

            if key == tcod.event.K_PERIOD:  # > (Down stairs)
                return actions.downstairs_action.DownStairsAction(
                    entity=player,
                    dungeon=self.engine.dungeon
                )

            elif key == tcod.event.K_COMMA:  # < (Up stairs)
                return actions.upstairs_action.UpStairsAction(
                    entity=player,
                    dungeon=self.engine.dungeon
                )

            elif key == tcod.event.K_SLASH:   # ? (Help screen)
                from handlers.handlers import HelpHandler
                return HelpHandler(self.engine)

        if modifier & (tcod.event.KMOD_LCTRL | tcod.event.KMOD_RCTRL):
            # For users with numpad, they can also use Control + Move key to run.
            if key in MOVE_KEYS:
                # Create new run behavior
                player.add_comp(ai=ai.RunAI(direction=MOVE_KEYS[key]))

                # The first move/bump action should get handled below
                if self.engine.player.ai.can_perform():
                    return player.ai.yield_action()

            elif key == tcod.event.K_x:
                # Ctrl-X: Character Screen
                return CharacterScreenHandler(self.engine)

        if key in MOVE_KEYS:
            dx, dy = MOVE_KEYS[key]
            action = actions.bump_action.BumpAction(player, dx, dy)

        elif key in WAIT_KEYS:
            action = actions.wait_action.WaitAction(player)

        elif key == tcod.event.K_ESCAPE:
            raise SystemExit()

        elif key == tcod.event.K_v:
            return HistoryHandler(self.engine)

        elif key == tcod.event.K_COMMA:
            action = actions.pickup_action.PickupAction(player)

        elif key == tcod.event.K_i:
            return InventoryActivateHandler(self.engine)

        elif key == tcod.event.K_d:
            return InventoryDropHandler(self.engine)

        elif key == tcod.event.K_SLASH:
            return LookHandler(self.engine)

        elif key == tcod.event.K_s:
            action = actions.search_action.SearchAction(player)

        # No valid key was pressed
        return action