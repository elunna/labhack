from . import color
from . import exceptions
from . import render_functions
from . import settings
from .settings import MOVE_KEYS, WAIT_KEYS, CURSOR_Y_KEYS, CONFIRM_KEYS
from .setup_game import load_game, new_game
from typing import Union
from components import ai
import os
import src.actions
import tcod
import tcod.event
import traceback

ActionOrHandler = Union[src.actions.Action, "BaseEventHandler"]
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

        assert not isinstance(state, src.actions.Action), f"{self!r} can not handle actions."
        return self

    def on_render(self, console):
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
                return GameOverEventHandler(self.engine)

            # Player leveled up
            elif self.engine.player.level.requires_level_up:
                # This handler is currently on hold.
                # return LevelUpEventHandler(self.engine)

                # Instead, boost a random stat.
                self.engine.player.level.get_random_stat_increase()

            return MainGameEventHandler(self.engine)  # Return to the main handler.
        return self

    def handle_action(self, action):
        """ Handle actions returned from event methods.
            Returns True if the action will advance a turn.
        """

        if action is None:
            return False

        try:
            action.perform()
        except exceptions.Impossible as exc:
            self.engine.message_log.add_message(exc.args[0], color.impossible)
            return False  # Skip enemy turn on exceptions

        self.engine.handle_enemy_turns()
        self.engine.update_fov()

        return True

    def ev_mousemotion(self, event):
        if self.engine.game_map.in_bounds(event.tile.x, event.tile.y):
            self.engine.mouse_location = event.tile.x, event.tile.y

    def on_render(self, console):
        # render_map(console, self.engine.game_map)
        self.engine.render(console)


class MainGameEventHandler(EventHandler):
    """ For reference, these are the event codes for tcod.
        https://python-tcod.readthedocs.io/en/latest/tcod/event.html
    """
    def ev_keydown(self, event):
        action = None
        player = self.engine.player

        # TODO: Crude way to handle paralysis, fix this later
        if isinstance(player.ai, ai.ParalyzedAI):
            action = player.ai.perform()
            if action:
                return action
            # This is a hack, we don't want to skip the players turn when they
            # break free of paralysis. This will skip enemy turns and give the
            # player to act once they are unparalyzed.
            return None

        # A key was pressed, determine which key and create an appropriate action.
        key = event.sym

        # Used to tell us if a player is holding a modifier key like control,
        # alt, or shift.
        modifier = event.mod


        # Handle >
        if key == tcod.event.K_PERIOD and modifier & (
                tcod.event.KMOD_LSHIFT | tcod.event.KMOD_RSHIFT
        ):
            return src.actions.TakeStairsAction(player)

        # Ctrl-X: Character Screen
        if key == tcod.event.K_x and modifier & (
                tcod.event.KMOD_LCTRL | tcod.event.KMOD_RCTRL
        ):
            return CharacterScreenEventHandler(self.engine)

        if key in MOVE_KEYS:
            # Check if player is confused
            # TODO: Replace with a better use of the AI states in the future.
            # HumanAI might be this whole input handler, while there might be a
            # different event handler for confusion.
            # ConfusedEventHandler could even be a subclass of Main...
            if isinstance(player.ai, ai.ConfusedEnemy):
                action = player.ai.perform()
            else:
                dx, dy = MOVE_KEYS[key]
                action = src.actions.BumpAction(player, dx, dy)

        elif key in WAIT_KEYS:
            action = src.actions.WaitAction(player)

        elif key == tcod.event.K_ESCAPE:
            raise SystemExit()

        elif key == tcod.event.K_v:
            return HistoryViewer(self.engine)

        elif key == tcod.event.K_COMMA:
            action = src.actions.PickupAction(player)

        elif key == tcod.event.K_i:
            return InventoryActivateHandler(self.engine)

        elif key == tcod.event.K_d:
            return InventoryDropHandler(self.engine)

        elif key == tcod.event.K_SLASH:
            return LookHandler(self.engine)

        # No valid key was pressed
        return action


class GameOverEventHandler(EventHandler):
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
            return HistoryViewer(self.engine)


class HistoryViewer(EventHandler):
    """Print the history on a larger window which can be navigated."""

    def __init__(self, engine):
        super().__init__(engine)
        self.log_length = len(engine.message_log.messages)
        self.cursor = self.log_length - 1

    def on_render(self, console):
        super().on_render(console)  # Draw the main state as the background.

        log_console = tcod.Console(console.width - 6, console.height - 6)

        # Draw a frame with a custom banner title.
        log_console.draw_frame(0, 0, log_console.width, log_console.height)

        log_console.print_box(
            0, 0, log_console.width, 1, "┤Message history├", alignment=tcod.CENTER
        )

        # Render the message log using the cursor parameter.
        # self.engine.message_log.render_messages(
        render_functions.render_messages(
            console=log_console,
            x=1, y=1,
            width=log_console.width - 2,
            height=log_console.height - 2,
            messages=self.engine.message_log.messages[: self.cursor + 1],
        )
        log_console.blit(console, 3, 3)

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
                return GameOverEventHandler(self.engine)

            return MainGameEventHandler(self.engine)
        return None


class AskUserEventHandler(EventHandler):
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
        return MainGameEventHandler(self.engine)


class InventoryEventHandler(AskUserEventHandler):
    """ This handler lets the user select an item.
        What happens then depends on the subclass.
    """

    TITLE = "<missing title>"

    def on_render(self, console):
        """ Render an inventory menu, which displays the items in the inventory, and the letter to select them.
            Will move to a different position based on where the player is located, so the player can always see where
            they are.
            If there’s nothing in the inventory, it just prints “Empty”.
        """
        super().on_render(console)
        number_of_items_in_inventory = len(self.engine.player.inventory.items)

        height = number_of_items_in_inventory + 2

        if height <= 3:
            height = 3

        if self.engine.player.x <= 30:
            x = 40
        else:
            x = 0

        y = 0

        width = len(self.TITLE) + 4

        console.draw_frame(
            x=x,
            y=y,
            width=width,
            height=height,
            title=self.TITLE,
            clear=True,
            fg=(255, 255, 255),
            bg=(0, 0, 0),
        )

        if number_of_items_in_inventory > 0:
            for i, item in enumerate(self.engine.player.inventory.items):
                item_key = chr(ord("a") + i)
                is_equipped = self.engine.player.equipment.item_is_equipped(item)

                item_string = f"({item_key}) {item.name}"

                if is_equipped:
                    item_string = f"{item_string} (E)"

                console.print(x + 1, y + i + 1, item_string)
        else:
            console.print(x + 1, y + 1, "(Empty)")

    def ev_keydown(self, event):
        # takes the user’s input, from letters a - z, and associates that with
        # an index in the inventory.
        player = self.engine.player
        key = event.sym
        index = key - tcod.event.K_a

        if 0 <= index <= 26:
            try:
                selected_item = player.inventory.items[index]
            except IndexError:
                self.engine.message_log.add_message("Invalid entry.", color.invalid)
                return None
            return self.on_item_selected(selected_item)
        return super().ev_keydown(event)

    def on_item_selected(self, item):
        """Called when the user selects a valid item."""
        raise NotImplementedError()


class InventoryActivateHandler(InventoryEventHandler):
    """Handle using an inventory item."""

    TITLE = "Select an item to use"

    def on_item_selected(self, item):
        """Return the action for the selected item."""
        if item.consumable:
            # Return the action for the selected item.
            return item.consumable.get_action(self.engine.player)
        elif item.equippable:
            return src.actions.EquipAction(self.engine.player, item)
        else:
            return None


class InventoryDropHandler(InventoryEventHandler):
    """ Handle dropping an inventory item."""

    TITLE = "Select an item to drop"

    def on_item_selected(self, item):
        """ Drop this item."""
        return src.actions.DropItem(self.engine.player, item)


class SelectIndexHandler(AskUserEventHandler):
    """ Handles asking the user for an index on the map.
        what we’ll use when we want to select a tile on the map.
    """

    def __init__(self, engine):
        """ Sets the cursor to the player when this handler is constructed."""

        super().__init__(engine)
        player = self.engine.player
        engine.mouse_location = player.x, player.y

    def on_render(self, console):
        """ Highlight the tile under the cursor.
            render the console as normal, by calling super().on_render, but it
            also adds a cursor on top, that can be used to show where the current
            cursor position is. This is especially useful if the player is
            navigating around with the keyboard.
         """

        super().on_render(console)
        x, y = self.engine.mouse_location
        console.tiles_rgb["bg"][x, y] = color.white
        console.tiles_rgb["fg"][x, y] = color.black

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
            y = max(0, min(y, self.engine.game_map.height - 1))
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
        return MainGameEventHandler(self.engine)


class SingleRangedAttackHandler(SelectIndexHandler):
    """Handles targeting a single enemy. Only the enemy selected will be affected."""

    def __init__(self, engine, callback):
        super().__init__(engine)

        # activates when the user selects a target.
        self.callback = callback

    def on_index_selected(self, x, y):
        return self.callback((x, y))


class AreaRangedAttackHandler(SelectIndexHandler):
    """Handles targeting an area within a given radius. Any entity within the area will be affected."""

    def __init__(self, engine, radius, callback):
        # callback: Callable[[Tuple[int, int]], Optional[Action]]
        super().__init__(engine)

        self.radius = radius
        self.callback = callback

    def on_render(self, console):
        """Highlight the tile under the cursor."""
        super().on_render(console)

        x, y = self.engine.mouse_location

        # Draw a rectangle around the targeted area, so the player can see the affected tiles.
        console.draw_frame(
            x=x - self.radius - 1,
            y=y - self.radius - 1,
            width=self.radius ** 2,
            height=self.radius ** 2,
            fg=color.red,
            clear=False,
        )

    def on_index_selected(self, x, y):
        # same as the one we defined for SingleRangedAttackHandler.
        return self.callback((x, y))


class PopupMessage(BaseEventHandler):
    """Display a popup text window."""

    def __init__(self, parent_handler, text):
        self.parent = parent_handler
        self.text = text

    def on_render(self, console):
        """Render the parent and dim the result, then print the message on top."""
        self.parent.on_render(console)
        console.tiles_rgb["fg"] //= 8
        console.tiles_rgb["bg"] //= 8

        console.print(
            console.width // 2,
            console.height // 2,
            self.text,
            fg=color.white,
            bg=color.black,
            alignment=tcod.CENTER,
        )

    def ev_keydown(self, event):
        """Any key returns to the parent handler."""
        return self.parent


class LevelUpEventHandler(AskUserEventHandler):
    """ PAUSED: For now this function is on hold until a more advanced skill tree
        is developed. When a level up is triggered, we will instead give a boost
        to a random stat.
    """
    TITLE = "Level Up"

    def on_render(self, console):
        super().on_render(console)

        if self.engine.player.x <= 30:
            x = 40
        else:
            x = 0

        console.draw_frame(
            x=x, y=0,
            width=35,
            height=8,
            title=self.TITLE,
            clear=True,
            fg=(255, 255, 255),
            bg=(0, 0, 0),
        )

        console.print(x=x + 1, y=1, string="Congratulations! You level up!")
        console.print(x=x + 1, y=2, string="Select an attribute to increase.")

        console.print(
            x=x + 1, y=4,
            string=f"a) Constitution (+20 HP, from {self.engine.player.fighter.max_hp})",
        )
        console.print(
            x=x + 1, y=5,
            string=f"b) Strength (+1 attack, from {self.engine.player.fighter.power})",
        )
        console.print(
            x=x + 1, y=6,
            string=f"c) Agility (+1 defense, from {self.engine.player.fighter.defense})",
        )

    def ev_keydown(self, event):
        player = self.engine.player
        key = event.sym
        index = key - tcod.event.K_a

        if 0 <= index <= 2:
            if index == 0:
                player.level.increase_max_hp()
            elif index == 1:
                player.level.increase_power()
            else:
                player.level.increase_defense()
        else:
            self.engine.message_log.add_message("Invalid entry.", color.invalid)

            return None

        return super().ev_keydown(event)

    def ev_mousebuttondown(self, event):
        """ Don't allow the player to click to exit the menu, like normal.  """
        return None


class CharacterScreenEventHandler(AskUserEventHandler):
    TITLE = "Character Information"

    def on_render(self, console):
        super().on_render(console)

        if self.engine.player.x <= 30:
            x = 40
        else:
            x = 0

        y = 0

        width = len(self.TITLE) + 4

        console.draw_frame(
            x=x, y=y,
            width=width,
            height=7,
            title=self.TITLE,
            clear=True,
            fg=(255, 255, 255),
            bg=(0, 0, 0),
        )

        console.print(
            x=x + 1, y=y + 1,
            string=f"Level: {self.engine.player.level.current_level}"
        )
        console.print(
            x=x + 1, y=y + 2,
            string=f"XP: {self.engine.player.level.current_xp}"
        )
        console.print(
            x=x + 1, y=y + 3,
            string=f"XP for next Level: {self.engine.player.level.experience_to_next_level}",
        )

        console.print(
            x=x + 1, y=y + 4,
            string=f"Attack: {self.engine.player.fighter.power}"
        )
        console.print(
            x=x + 1, y=y + 5,
            string=f"Defense: {self.engine.player.fighter.defense}"
        )


class MainMenuHandler(BaseEventHandler):
    """Handle the main menu rendering and input."""

    def on_render(self, console):
        """Render the main menu on a background image."""
        # Load the background image and remove the alpha channel.
        background_image = tcod.image.load(settings.bg_img)[:, :, :3]

        console.draw_semigraphics(background_image, 0, 0)

        console.print(
            console.width // 2,
            console.height // 2 - 4,
            settings.title_extended,
            fg=color.menu_title,
            alignment=tcod.CENTER,
        )
        console.print(
            console.width // 2,
            console.height - 2,
            settings.author,
            fg=color.menu_title,
            alignment=tcod.CENTER,
        )

        menu_width = settings.menu_width

        for i, text in enumerate(
            ["[N] Play a new game", "[C] Continue last game", "[Q] Quit"]
        ):
            console.print(
                console.width // 2,
                console.height // 2 - 2 + i,
                text.ljust(menu_width),
                fg=color.menu_text,
                bg=color.black,
                alignment=tcod.CENTER,
                bg_blend=tcod.BKGND_ALPHA(64),
            )

    def ev_keydown( self, event):
        # Event handler for main menu.

        if event.sym in (tcod.event.K_q, tcod.event.K_ESCAPE):
            raise SystemExit()
        elif event.sym == tcod.event.K_c:

            try:
                return MainGameEventHandler(
                    load_game(settings.save_file)
                )
            except FileNotFoundError:
                return PopupMessage(
                    self,
                    "No saved game to load."
                )
            except Exception as exc:
                traceback.print_exc()  # Print to stderr.
                return PopupMessage(
                    self,
                    f"Failed to load save:\n{exc}"
                )

        elif event.sym == tcod.event.K_n:
            return MainGameEventHandler(new_game())

        return None
