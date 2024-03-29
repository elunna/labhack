from components.equippable import Weapon
from . import color, utils
from . import messages
from . import settings
from . import tiles
from components import equipment
import numpy as np
import tcod


class Renderer:
    """Creates the main rendering root console with the tileset, and manages the rendering
    between the different console panels.
    """
    def __init__(self):
        tileset = tcod.tileset.load_tilesheet(
            path=settings.tileset,
            columns=32,
            rows=8,
            charmap=tcod.tileset.CHARMAP_TCOD
        )

        # Create the screen:
        # https://python-tcod.readthedocs.io/en/latest/tcod/context.html

        self.context = tcod.context.new_terminal(
            settings.screen_width,
            settings.screen_height,
            tileset=tileset,
            title=settings.title,
            vsync=True,
            renderer=tcod.RENDERER_SDL2,  # Fix green lines on Windows
        )

        # The “order” argument affects the order of our x and y variables in
        # numpy (an underlying library that tcod uses). By default, numpy
        # accesses 2D arrays in [y, x] order, which is fairly unintuitive. By
        # setting order="F", we can change this to be [x, y] instead.
        self.root = tcod.Console(settings.screen_width, settings.screen_height, order="F")

        # Define separate panels for the map, messages, and stats.
        self.msg_panel = tcod.Console(width=settings.screen_width, height=settings.msg_panel_height)
        self.map_panel = tcod.Console(width=settings.map_width, height=settings.map_height, order="F",)
        self.stat_panel = tcod.Console(width=settings.screen_width, height=settings.stat_panel_height)

    def render_all(self, engine):
        player = engine.player

        # Message Panel
        render_messages(
            console=self.msg_panel,
            x=settings.msg_panel_x, y=0,
            width=settings.screen_width,
            height=settings.msg_panel_height,
            msg_list=engine.msglog.messages,
        )

        # Map Panel
        render_map(self.map_panel, engine.game_map)

        # Stat Panel
        render_names_at_mouse_location(
            console=self.stat_panel,
            x=settings.tooltip_x,
            y=settings.tooltip_y,
            engine=engine
        )

        ac_stat = f"AC:{player.fighter.ac}"
        str_stat = f"Str:{player.attributes.strength}"
        dex_stat = f"Dex:{player.attributes.dexterity}"
        con_stat = f"Con:{player.attributes.constitution}"
        xp_lvl_stat = f"XL:{player.level.current_level}"
        turns = f"Turns:{engine.turns}"

        render_text(
            self.stat_panel,
            x=22,
            y=settings.hp_bar_y,
            text=f"{ac_stat} | {str_stat} | {dex_stat} | {con_stat} | {xp_lvl_stat} | {turns}",
        )

        # Render players money
        money = player.inventory.item_dict.get('$', '$0')

        render_text(
            self.stat_panel,
            x=22,
            y=settings.hp_bar_y + 1,
            text=f"{money}",
            fg=tcod.gold,
        )

        # Render player states
        render_text(
            self.stat_panel,
            x=22,
            y=settings.tooltip_y - 2,
            text=f"{player.states.to_string()}",
            fg=tcod.red,
        )

        # Render current dungeon level
        x, y = settings.dlevel_text_location
        render_text(
            self.stat_panel,
            x=x,
            y=y,
            text=f"Dlevel: {engine.dungeon.dlevel}",
        )

        # Render HP Bar
        render_bar(
            console=self.stat_panel,
            x=settings.hp_bar_x,
            y=settings.hp_bar_y,
            val=player.fighter.hp,
            max_val=player.fighter.max_hp,
            total_width=settings.hp_bar_width,
            label="HP"
        )

        self.msg_panel.blit(self.root, 0, settings.msg_panel_y)
        self.map_panel.blit(self.root, 0, settings.map_panel_y)
        self.stat_panel.blit(self.root, 0, settings.stat_panel_y)

        self.msg_panel.clear()
        self.stat_panel.clear()


def render_text(console, x, y, text, fg=tcod.white):
    console.print(x=x, y=y, fg=fg, string=text)


def render_bar(console, x, y, val, max_val, total_width, label=''):
    """Renders a fillable bar (like an HP bar)"""
    bar_width = int(float(val) / max_val * total_width)

    console.draw_rect(
        x=x,
        y=y,
        width=settings.hp_bar_width,
        height=settings.bar_height,
        ch=1,
        bg=color.bar_empty
    )

    if bar_width > 0:
        console.draw_rect(
            x=x,
            y=y,
            width=bar_width,
            height=settings.bar_height,
            ch=1,
            bg=color.bar_filled
        )

    console.print(x=1, y=y, string=f"{label}: {val}/{max_val}", fg=color.bar_text)


def render_names_at_mouse_location(console, x, y, engine):
    """ takes the console, x and y coordinates (the location to draw the names), and the engine.
    From the engine, it grabs the mouse’s current x and y positions, and passes them to get_names_at_location,
    which we can assume for the moment will return the list of entity names we want. Once we have these entity
    names as a string, we can print that string to the given x and y location on the screen, with console.print.
    """
    mouse_x, mouse_y = engine.mouse_location

    # Need to correct for message window offset.
    mouse_y -= settings.msg_panel_height

    names_at_mouse_location = engine.game_map.get_names_at(
        x=mouse_x,
        y=mouse_y,
    )

    console.print(x=x, y=y, string=f"({mouse_x},{mouse_y}): {names_at_mouse_location}")


def render_messages(console, x, y, width, height, msg_list):
    """Render the messages provided. Render this log over the given area.
        `x`, `y`, `width`, `height` is the rectangular region to render onto the `console`.
    The `messages` are rendered starting at the last message and working backwards.
    """
    y_offset = height - 1

    for message in reversed(msg_list):
        for line in reversed(list(messages.MsgLog.wrap(message.full_text, width))):
            console.print(x=x, y=y + y_offset, string=line, fg=message.fg)
            y_offset -= 1
            if y_offset < 0:
                return  # No more space to print messages.


def render_map(console, game_map):
    """Render all the tiles in the map.
        If a tile is in the "visible" array, then draw it with the "light" colors.
        If it isn't, but it's in the "explored" array, then draw it with the "dark" colors.
        Otherwise, the default is "SHROUD".
    """

    # tiles_rgb method, much faster than using the console.print method
    # np.select allows us to conditionally draw the tiles we want, based on
    # what’s specified in condlist. Since we’re passing [self.visible, self.explored],
    # it will check if the tile being drawn is either visible, then explored.
    # If it’s visible, it uses the first value in choicelist, in this case,
    # self.tiles["light"]. If it’s not visible, but explored, then we draw
    # self.tiles["dark"]. If neither is true, we use the default argument,
    # which is just the SHROUD we defined earlier.
    console.tiles_rgb[0: game_map.width, 0: game_map.height] = np.select(
        condlist=[game_map.visible, game_map.explored],
        choicelist=[game_map.tiles["light"], game_map.tiles["dark"]],
        default=tiles.SHROUD,
    )

    # Sort the entities by render order.
    entities_sorted_for_rendering = sorted(
        game_map.entities, key=lambda x: x.render_order.value
    )

    for entity in entities_sorted_for_rendering:
        # Only print entities that are in the FOV
        if game_map.visible[entity.x, entity.y]:

            # Make sure it is not hidden or invisible!
            if "hidden" not in entity:
                console.print(x=entity.x, y=entity.y, string=entity.char, fg=entity.color)

        # Also remember items/traps that are on explored tiles
        if game_map.explored[entity.x, entity.y]:
            item_or_trap = "item" in entity or "trap" in entity
            if item_or_trap and "hidden" not in entity:
                console.print(x=entity.x, y=entity.y, string=entity.char, fg=entity.color)

    # TODO: Move to separate function
    # For testing: Render the room numbers
    # for room in game_map.rooms:
    #     room_x, room_y = room.center
    #     console.print(
    #         x=room_x,
    #         y=room_y,
    #         string=str(room.label),
    #         # fg=entity.color
    #     )


def render_history(console, title, cursor, msglog):
    """Renders the full message history."""
    log_console = tcod.Console(console.width - 6, console.height - 6)

    # Draw a frame with a custom banner title.
    log_console.draw_frame(0, 0, log_console.width, log_console.height)

    log_console.print_box(0, 0, log_console.width, 1, title, alignment=tcod.CENTER)

    # Render the message log using the cursor parameter.
    render_messages(
        console=log_console,
        x=1, y=1,
        width=log_console.width - 2,
        height=log_console.height - 2,
        msg_list=msglog.messages[: cursor + 1],
    )
    log_console.blit(console, 3, 3)


def render_inv(console, engine, title):
    """ Displays a nicely formatted list of our inventory, separated by category
        Categories: weapons, armor, potions, scrolls
    """
    inv_contents = engine.player.inventory.list_contents()
    qty_of_items = len(engine.player.inventory.item_dict)
    padding_space = 2
    height = len(inv_contents) + padding_space

    if height <= 3:
        height = 3
    x = console.width // 2
    y = 0
    width = x - 2

    console.draw_frame(
        x=x,
        y=y,
        width=width,
        height=height,
        title=title,
        clear=True,
        fg=(255, 255, 255),
        bg=(0, 0, 0),
    )

    if qty_of_items > 0:
        i = 0  # Counter for vertical spacing
        for line in inv_contents:
            fg = tcod.white
            if "Equipped" in line:
                # fg = tcod.light_blue
                fg = tcod.light_cyan

            console.print(x + 1, y + i + 1, line, fg=fg)

            i += 1
    else:
        console.print(x + 1, y + 1, "(Empty)")


def highlight_cursor(console, x, y):
    """Highlights the specified coordinate with a white background and black foreground. """
    console.tiles_rgb["bg"][x, y] = color.white
    console.tiles_rgb["fg"][x, y] = color.black


def hilite_tiles(console, tileset):
    """Highlights the area surrounding the specified coordinates. """
    # Highlight the affected tiles.
    for x, y in tileset:
        console.tiles_rgb["bg"][x, y] = color.red
        console.tiles_rgb["fg"][x, y] = color.black


def draw_rect(console, x, y, radius):
    """Draw a rectangle around the targeted area, so the player can see the affected tiles."""
    console.draw_frame(
        x=x - radius - 1,
        y=y - radius - 1,
        width=radius ** 2,
        height=radius ** 2,
        fg=color.red,
        clear=False,
    )


def render_popup(console, text):
    """Renders simple popup text over a dimmed background. """
    console.tiles_rgb["fg"] //= 8
    console.tiles_rgb["bg"] //= 8

    console.print(
        console.width // 2,
        console.height // 2,
        text,
        fg=color.white,
        bg=color.black,
        alignment=tcod.CENTER,
    )


def render_character_stats(console, engine, title):
    """Displays all the character stats and equipped items on a special screen. """
    msgs = [
        f"Level: {engine.player.level.current_level}",
        f"XP: {engine.player.level.current_xp}",
        f"XP for next Level: {engine.player.level.experience_to_next_level}",
        "",
        f"AC: {engine.player.fighter.ac}",
        f"Strength: {engine.player.attributes.strength}",
        f"Dexterity: {engine.player.attributes.dexterity}",
        f"Constitution: {engine.player.attributes.constitution}",
        "",
        "Equipment Slots:",
    ]
    for slot in equipment.EquipmentType:
        equipped = engine.player.equipment.slots[slot.name]
        equipped = equipped if equipped else ''
        msgs.append(f"{slot.name}: {equipped}")

    if engine.player.x <= 30:
        x = 40
    else:
        x = 0
    y = 0

    width = len(title) + 4

    console.draw_frame(
        x=x, y=y,
        width=width,
        height=len(msgs) + 2,
        title=title,
        clear=True,
        fg=(255, 255, 255),
        bg=(0, 0, 0),
    )

    for i, m in enumerate(msgs):
        console.print(
            x=x + 1, y=y + 1 + i,
            string=m
        )


def render_main_menu(console):
    """Renders the main menu and options."""
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
        f"Version {settings.version}",
        fg=color.menu_title,
        alignment=tcod.CENTER,
    )

    menu_width = settings.menu_width

    for i, text in enumerate([
        "[N] Play a new game",
        "[C] Continue last game",
        "[G] Generate test map",
        "[Q] Quit"
    ]
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


def render_map_debugger(console, mode, max_rooms, min_size, max_size, max_dist, maze_path):
    """Displays the map debugging screen and the available options."""
    maxrooms_str = f"Max Rooms:{max_rooms} +/-"
    minsize_str = f"Min Size:{min_size}"
    maxsize_str = f"Max Size:{max_size}"

    console.print(x=0, y=0, string=f"MODE: {mode}")

    console.print(
        x=0, y=settings.map_height + 1,
        string=f"{maxrooms_str}"
    )

    console.print(
        x=0, y=settings.map_height + 2,
        string=f"{minsize_str} | {maxsize_str} (Adjust with Arrow Keys)"
    )

    console.print(
        x=0, y=settings.map_height + 3,
        string=f"Max Dist:{max_dist} </>"
    )

    console.print(
        x=0, y=settings.map_height + 4,
        string=f"Maze path:{maze_path} [/]"
    )

    console.print(
        x=0, y=settings.map_height + 5,
        string=f"ESC: Return to main menu"
    )
