from handlers.eventhandler import EventHandler
from handlers.maingame import MainGameHandler
from src import color
from src import exceptions
from src import logger
from src import rendering
from src import settings
from src.input_keys import MOVE_KEYS, CURSOR_Y_KEYS, CONFIRM_KEYS
import actions.actions
import actions.bump_action
import actions.downstairs_action
import actions.upstairs_action
import actions.drop_action
import actions.equip_action
import actions.pickup_action
import actions.wait_action
import actions.search_action
import os
import tcod
import tcod.event

log = logger.setup_logger(__name__)


class GameOverHandler(EventHandler):
    def on_quit(self):
        """Handle exiting out of a finished game."""
        if os.path.exists("../savegame.sav"):
            os.remove("../savegame.sav")  # Deletes the active save file.

        raise exceptions.QuitWithoutSaving()  # Avoid saving a finished game.

    def ev_quit(self, event):
        self.on_quit()

    def ev_keydown(self, event):
        key = event.sym

        if event.sym == tcod.event.K_ESCAPE:
            self.on_quit()

        # Still can view history on death
        elif key == tcod.event.K_v:
            return HistoryHandler(self.engine)


class HistoryHandler(EventHandler):
    """Print the history on a larger window which can be navigated."""

    def __init__(self, engine):
        super().__init__(engine)
        self.log_length = len(engine.msglog.messages)
        self.cursor = self.log_length - 1

    def on_render(self, renderer):
        super().on_render(renderer)  # Draw the main state as the background.
        rendering.render_history(
            console=renderer.root,
            title="┤Message history├",
            cursor=self.cursor,
            msglog=self.engine.msglog

        )

    def ev_keydown(self, event):
        # Fancy conditional movement to make it feel right.
        if event.sym in CURSOR_Y_KEYS:
            adjust = CURSOR_Y_KEYS[event.sym]

            if adjust < 0 and self.cursor == 0:
                # Only move from the top to the bottom when you're on the edge.
                self.cursor = self.log_length - 1
            elif adjust > 0 and self.cursor == self.log_length - 1:
                # Same with bottom to top movement.
                self.cursor = 0
            else:
                # Otherwise move while staying clamped to the bounds of the history log.
                self.cursor = max(0, min(self.cursor + adjust, self.log_length - 1))

        elif event.sym == tcod.event.K_HOME:
            self.cursor = 0  # Move directly to the top message.
        elif event.sym == tcod.event.K_END:
            self.cursor = self.log_length - 1  # Move directly to the last message.
        else:
            # Any other key moves back to the previous game state.

            # First, Check if the player is dead...
            if not self.engine.player.is_alive:
                return GameOverHandler(self.engine)

            return MainGameHandler(self.engine)
        return None


class AskUserHandler(EventHandler):
    """Handles user input for actions which require special input.
         by default, just exits itself when any key is pressed, besides one of
         the “modifier” keys (shift, control, and alt). It also exits when
         clicking the mouse.
    """

    def ev_keydown(self, event):
        """By default any key exits this input handler."""
        if event.sym in {  # Ignore modifier keys.
            tcod.event.K_LSHIFT,
            tcod.event.K_RSHIFT,
            tcod.event.K_LCTRL,
            tcod.event.K_RCTRL,
            tcod.event.K_LALT,
            tcod.event.K_RALT,
        }:
            return None
        return self.on_exit()

    def ev_mousebuttondown(self, event):
        """By default any mouse click exits this input handler."""
        return self.on_exit()

    def on_exit(self):
        """Called when the user is trying to exit or cancel an action.

        By default this returns to the main event handler.
        """
        return MainGameHandler(self.engine)


class InventoryHandler(AskUserHandler):
    """ This handler lets the user select an item.
        What happens then depends on the subclass.
    """

    TITLE = "<missing title>"

    def on_render(self, renderer):
        """ Render an inventory menu, which displays the items in the inventory, and the letter to select them.
            Will move to a different position based on where the player is located, so the player can always see where
            they are.
            If there’s nothing in the inventory, it just prints “Empty”.
        """
        super().on_render(renderer)
        rendering.render_inv(renderer.root, self.engine, self.TITLE)

    def ev_keydown(self, event):
        # takes the user’s input, from letters a - z, and associates that with
        # an index in the inventory.
        player = self.engine.player
        modifier = event.mod
        try:
            key = chr(event.sym)  # Get letter the player selected
        except ValueError:
            return

        if modifier & (tcod.event.KMOD_LSHIFT | tcod.event.KMOD_RSHIFT):

            # if key == tcod.event.K_4:
            # if key == tcod.event.K_KP_4:
            # if key == tcod.event.K_DOLLAR:  # event.sym 52
            if key == '4':
                key = '$'
            else:
                key = key.upper()

        # Workaround until we can figure out how to get the dollar sign input working.
        if key == tcod.event.K_4:
            key = '$'

        if key in player.inventory.item_dict:
            try:
                # selected_item = player.inventory.items[index]
                selected_item = player.inventory.item_dict.get(key)
            except IndexError:
                self.engine.msglog.add_message("Invalid entry.", color.invalid)
                return None
            return self.on_item_selected(selected_item)
        return super().ev_keydown(event)

    def on_item_selected(self, item):
        """Called when the user selects a valid item."""
        raise NotImplementedError()


class InventoryActivateHandler(InventoryHandler):
    """Handle using an inventory item."""

    TITLE = "Select an item to use"

    def on_item_selected(self, item):
        """Return the action for the selected item."""
        if item.consumable:
            # Return the action for the selected item.
            return item.consumable.get_action(self.engine.player)
        elif item.equippable:
            return actions.equip_action.EquipAction(self.engine.player, item)
        else:
            return None


class InventoryDropHandler(InventoryHandler):
    """ Handle dropping an inventory item."""

    TITLE = "Select an item to drop"

    def on_item_selected(self, item):
        """ Drop this item."""
        return actions.drop_action.DropAction(self.engine.player, item)


class SelectIndexHandler(AskUserHandler):
    """ Handles asking the user for an index on the map.
        what we’ll use when we want to select a tile on the map.
    """

    def __init__(self, engine):
        """ Sets the cursor to the player when this handler is constructed."""

        super().__init__(engine)
        player = self.engine.player
        # engine.mouse_location = player.x, player.y

        # Hack to fix the msg_panel offset.
        engine.mouse_location = player.x, player.y + settings.msg_panel_height

    def on_render(self, renderer):
        """ Highlight the tile under the cursor.
            render the console as normal, by calling super().on_render, but it
            also adds a cursor on top, that can be used to show where the current
            cursor position is. This is especially useful if the player is
            navigating around with the keyboard.
         """

        super().on_render(renderer)
        x, y = self.engine.mouse_location
        rendering.highlight_cursor(renderer.root, x, y)

    def ev_keydown(self, event):
        """ Check for key movement or confirmation keys.
            gives us a way to move the cursor we’re drawing around using the
            keyboard instead of the mouse (using the mouse is still possible).
            By using the same movement keys we use to move the player around,
            we can move the cursor around, with a few extra options. By holding,
            shift, control, or alt while pressing a movement key, the cursor will
            move around faster by skipping over a few spaces. This could be very
            helpful if you plan on making your map larger. If the user presses a
            “confirm” key, the method returns the current cursor’s location.
        """
        key = event.sym

        if key in MOVE_KEYS:
            modifier = 1  # Holding modifier keys will speed up key movement.
            if event.mod & (tcod.event.KMOD_LSHIFT | tcod.event.KMOD_RSHIFT):
                modifier *= 5
            if event.mod & (tcod.event.KMOD_LCTRL | tcod.event.KMOD_RCTRL):
                modifier *= 10
            if event.mod & (tcod.event.KMOD_LALT | tcod.event.KMOD_RALT):
                modifier *= 20

            x, y = self.engine.mouse_location
            dx, dy = MOVE_KEYS[key]
            x += dx * modifier
            y += dy * modifier
            # Clamp the cursor index to the map size.
            x = max(0, min(x, self.engine.game_map.width - 1))

            # y = max(0, min(y, self.engine.game_map.height - 1))
            # Hack to fix msg_panel offset
            y = max(
                settings.msg_panel_height,
                min(y, self.engine.game_map.height - 1 + settings.msg_panel_height)
            )
            self.engine.mouse_location = x, y
            return None
        elif key in CONFIRM_KEYS:
            return self.on_index_selected(*self.engine.mouse_location)
        return super().ev_keydown(event)

    def ev_mousebuttondown(self, event):
        """ Left click confirms a selection.
             also returns the location, if the clicked space is within the map boundaries.
        """
        if self.engine.game_map.in_bounds(*event.tile):
            if event.button == 1:
                return self.on_index_selected(*event.tile)
        return super().ev_mousebuttondown(event)

    def on_index_selected(self, x, y):
        """ Called when an index is selected."""
        raise NotImplementedError()


class LookHandler(SelectIndexHandler):
    """ Lets the player look around using the keyboard."""

    def on_index_selected(self, x, y):
        """ Returns to main handler when it receives a confirmation key."""
        return MainGameHandler(self.engine)


class SingleRangedAttackHandler(SelectIndexHandler):
    """Handles targeting a single enemy. Only the enemy selected will be affected."""

    def __init__(self, engine, callback):
        super().__init__(engine)

        # activates when the user selects a target.
        self.callback = callback

    def on_index_selected(self, x, y):
        # return self.callback((x, y))

        # Hack to fix the msg_panel offset.
        return self.callback((x, y - 5))


class AreaRangedAttackHandler(SelectIndexHandler):
    """Handles targeting an area within a given radius. Any entity within the area will be affected."""

    def __init__(self, engine, radius, callback):
        # callback: Callable[[Tuple[int, int]], Optional[Action]]
        super().__init__(engine)

        self.radius = radius
        self.callback = callback

    def on_render(self, renderer):
        """Highlight the tile under the cursor."""
        super().on_render(renderer)

        x, y = self.engine.mouse_location
        # rendering.draw_rect(renderer.root, x, y, self.radius)
        rendering.hilite_radius(renderer.root, x, y, self.radius)

    def on_index_selected(self, x, y):
        # same as the one we defined for SingleRangedAttackHandler.
        # return self.callback((x, y))

        # Hack to fix the msg_panel offset.
        return self.callback((x, y - 5))


class CharacterScreenHandler(AskUserHandler):
    TITLE = "Character Information"

    def on_render(self, renderer):
        super().on_render(renderer)
        rendering.render_character_stats(renderer.root, self.engine, self.TITLE)


class HelpHandler(HistoryHandler):
    """Print the help info on a larger window which can be navigated."""

    def __init__(self, engine):
        super().__init__(engine)
        self.log_length = len(engine.helplog.messages)
        self.cursor = self.log_length - 1

    def on_render(self, renderer):
        super().on_render(renderer)  # Draw the main state as the background.
        rendering.render_history(
            console=renderer.root,
            title="┤Command Help├",
            cursor=self.cursor,
            msglog=self.engine.helplog
        )

    def ev_keydown(self, event):
        # Fancy conditional movement to make it feel right.
        if event.sym in CURSOR_Y_KEYS:
            adjust = CURSOR_Y_KEYS[event.sym]

            if adjust < 0 and self.cursor == 0:
                # Only move from the top to the bottom when you're on the edge.
                self.cursor = self.log_length - 1
            elif adjust > 0 and self.cursor == self.log_length - 1:
                # Same with bottom to top movement.
                self.cursor = 0
            else:
                # Otherwise move while staying clamped to the bounds of the history log.
                self.cursor = max(0, min(self.cursor + adjust, self.log_length - 1))

        elif event.sym == tcod.event.K_HOME:
            self.cursor = 0  # Move directly to the top message.
        elif event.sym == tcod.event.K_END:
            self.cursor = self.log_length - 1  # Move directly to the last message.
        else:
            # Any other key moves back to the previous game state.

            # First, Check if the player is dead...
            if not self.engine.player.is_alive:
                return GameOverHandler(self.engine)

            return MainGameHandler(self.engine)
        return None



