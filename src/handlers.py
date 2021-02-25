from . import color
from . import exceptions
from . import rendering
from . import settings
from .input_keys import MOVE_KEYS, WAIT_KEYS, CURSOR_Y_KEYS, CONFIRM_KEYS
from .maze import Maze
from .setup_game import load_game, new_game
from src import procgen
from typing import Union
import actions.actions
import actions.bump_action
import actions.downstairs_action
import actions.upstairs_action
import actions.drop_action
import actions.equip_action
import actions.pickup_action
import actions.wait_action
import os
import tcod
import tcod.event
import traceback

ActionOrHandler = Union[actions.actions.Action, "BaseEventHandler"]
"""An event handler return value which can trigger an action or switch active handlers.

    If a handler is returned then it will become the active handler for future events.
    If an action is returned it will be attempted and if it's valid then
    MainGameEventHandler will become the active handler.
"""


class BaseEventHandler(tcod.event.EventDispatch[ActionOrHandler]):
    def handle_events(self, event):
        """Handle an event and return the next active event handler."""
        state = self.dispatch(event)

        if isinstance(state, BaseEventHandler):
            return state

        assert not isinstance(state, actions.actions.Action), f"{self!r} can not handle actions."
        return self

    def on_render(self, renderer):
        raise NotImplementedError()

    def ev_quit(self, event):
        raise SystemExit()


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

        if isinstance(action_or_state, BaseEventHandler):
            return action_or_state

        if self.handle_action(action_or_state):
            # A valid action was performed.
            if not self.engine.player.is_alive:
                # The player was killed sometime during or after the action.
                return GameOverHandler(self.engine)

            # If the player leveled up, handle it.
            self.engine.check_level()

            return MainGameHandler(self.engine)  # Return to the main handler.
        return self

    def handle_action(self, action):
        """ Handle actions returned from event methods.
            Returns True if the action will advance a turn.
        """
        if self.engine.handle_action(action):  # Successful action completed.
            # Here - we will evaluate the player's energy
            # Use up a turn worth of energy
            self.engine.player.energymeter.burn_turn()

            self.engine.update_fov()

            # If the player doesn't have enough energy for another turn, we'll
            # run the enemy turns.
            if self.engine.player.energymeter.burned_out():
                # Increment turns
                self.engine.turns += 1

                # All actors get an energy recharge every turn
                self.engine.add_energy()

                self.engine.handle_enemy_turns()
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


class MainGameHandler(EventHandler):
    """ For reference, these are the event codes for tcod.
        https://python-tcod.readthedocs.io/en/latest/tcod/event.html
    """
    def ev_keydown(self, event):
        # A key was pressed, determine which key and create an appropriate action.
        action = None

        key = event.sym

        # Used to tell us if a player is holding a modifier key like control,
        # alt, or shift.
        modifier = event.mod

        player = self.engine.player

        # Shift modifiers
        if modifier & (tcod.event.KMOD_LSHIFT | tcod.event.KMOD_RSHIFT):
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
                return HelpHandler(self.engine)

        # Ctrl-X: Character Screen
        if key == tcod.event.K_x and modifier & (
                tcod.event.KMOD_LCTRL | tcod.event.KMOD_RCTRL
        ):
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

        # No valid key was pressed
        return action


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
            engine=self.engine,
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
        key = chr(event.sym)  # Get letter the player selected

        if key in player.inventory.items:
            try:
                # selected_item = player.inventory.items[index]
                selected_item = player.inventory.items.get(key)
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


class PopupMsgHandler(BaseEventHandler):
    """Display a popup text window."""

    def __init__(self, parent_handler, text):
        self.parent = parent_handler
        self.text = text

    def on_render(self, renderer):
        """Render the parent and dim the result, then print the message on top."""
        self.parent.on_render(renderer)
        rendering.render_popup(renderer.root, self.text)

    def ev_keydown(self, event):
        """Any key returns to the parent handler."""
        return self.parent


class MapDebugHandler(BaseEventHandler):
    """Display a random from the generator."""

    def __init__(self, parent_handler):
        self.parent = parent_handler
        self.max_rooms = settings.max_rooms
        self.room_min_size = settings.room_min_size
        self.room_max_size = settings.room_max_size
        self.room_max_distance = 30
        self.maze_path_width = 1
        self.map_func = self.generate_map
        self.mode = ''
        self.map = self.map_func()  # Do this last!

    def generate_map(self):
        self.mode = "ROOMS & CORRIDORS"
        # Generate a new map
        return procgen.generate_map(
            max_rooms=self.max_rooms,
            room_min_size=self.room_min_size,
            room_max_size=self.room_max_size,
            map_width=settings.map_width,
            map_height=settings.map_height,
            max_distance=self.room_max_distance,
        )

    def generate_maze(self):
        self.mode = "MAZE"
        fitted_width, fitted_height = Maze.dimensions_to_fit(
            settings.map_width,
            settings.map_height,
            path_width=self.maze_path_width
        )
        m = Maze(width=fitted_width, height=fitted_height, path_width=self.maze_path_width)
        m.create_maze()
        return m.export_gamemap()

    def on_render(self, renderer):
        """Render the parent and dim the result, then print the message on top."""
        self.parent.on_render(renderer)

        # Set all tiles to visible
        self.map.visible[:] = True
        self.map.explored[:] = True

        rendering.render_map(renderer.root, self.map)
        # Render debug info
        rendering.render_map_debugger(
            console=renderer.root,
            mode=self.mode,
            max_rooms=self.max_rooms,
            min_size=self.room_min_size,
            max_size=self.room_max_size,
            max_dist=self.room_max_distance,
            maze_path=self.maze_path_width,
        )

    def ev_keydown(self, event):
        """Any key returns to the parent handler."""
        key = event.sym
        modifier = event.mod

        if modifier & (tcod.event.KMOD_LSHIFT | tcod.event.KMOD_RSHIFT):
            # >
            if key == tcod.event.K_PERIOD:
                self.room_max_distance += 1
            # <
            elif key == tcod.event.K_COMMA:
                if self.room_max_distance > 10:
                    self.room_max_distance -= 1
            else:
                return

        elif key == tcod.event.K_ESCAPE:
            return self.parent
        elif key == tcod.event.K_1:
            self.map_func = self.generate_map
        elif key == tcod.event.K_2:
            self.map_func = self.generate_maze

        elif key == tcod.event.K_UP:
            self.room_max_size += 1
        elif key == tcod.event.K_DOWN:
            if self.room_max_size > self.room_min_size:
                self.room_max_size -= 1
        elif key == tcod.event.K_RIGHT:
            if self.room_min_size < self.room_max_size:
                self.room_min_size += 1
        elif key == tcod.event.K_LEFT:
            if self.room_min_size > 3:
                self.room_min_size -= 1

        elif key == tcod.event.K_LEFTBRACKET:
            if self.maze_path_width > 1:
                self.maze_path_width -= 1
        elif key == tcod.event.K_RIGHTBRACKET:
            self.maze_path_width += 1

        self.map = self.map_func()


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


class CharacterScreenHandler(AskUserHandler):
    TITLE = "Character Information"

    def on_render(self, renderer):
        super().on_render(renderer)
        rendering.render_character_stats(renderer.root, self.engine, self.TITLE)


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
            engine=self.engine,
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



