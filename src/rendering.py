from components.equippable import Weapon
from . import color, utils
from . import messages
from . import settings
from . import tiles
from components import equipment
import math
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
        self.msg_panel = tcod.Console(
            width=settings.screen_width,
            height=settings.msg_panel_height
        )

        self.map_panel = tcod.Console(
            width=settings.map_width,
            height=settings.map_height,
            order="F",
        )

        self.stat_panel = tcod.Console(
            width=settings.screen_width,
            height=settings.stat_panel_height
        )


def render_bar(console, current_value, maximum_value, total_width):
    """Renders a fillable bar (like an HP bar)"""
    bar_width = int(float(current_value) / maximum_value * total_width)

    console.draw_rect(
        x=settings.hp_bar_x,
        y=settings.hp_bar_y,
        width=settings.hp_bar_width,
        height=settings.hp_bar_height,
        ch=1,
        bg=color.bar_empty
    )

    if bar_width > 0:
        console.draw_rect(
            x=settings.hp_bar_x,
            y=settings.hp_bar_y,
            width=bar_width,
            height=settings.hp_bar_height,
            ch=1,
            bg=color.bar_filled
        )

    console.print(
        x=1, y=settings.hp_bar_y,
        string=f"HP: {current_value}/{maximum_value}",
        fg=color.bar_text
    )


def render_dungeon_lvl_text(console, dungeon_level):
    """ Render the level the player is currently on, at the given location. """
    x, y = settings.dlevel_text_location
    console.print(x=x, y=y, string=f"Dlevel: {dungeon_level}")


def render_stats(console, engine, player):
    """Renders all the important player stats in the stat panel."""
    ac_stat = f"AC:{player.fighter.ac}"
    str_stat = f"Str:{player.attributes.strength}"
    dex_stat = f"Dex:{player.attributes.dexterity}"
    con_stat = f"Con:{player.attributes.constitution}"
    xp_lvl_stat = f"XL:{player.level.current_level}"
    turns = f"Turns:{engine.turns}"
    money = player.inventory.item_dict.get('$', 0)

    console.print(
        x=22, y=settings.hp_bar_y,
        string=f"{ac_stat} | {str_stat} | {dex_stat} | {con_stat} | {xp_lvl_stat} | {turns}"
    )
    console.print(
        x=22, y=settings.hp_bar_y + 1, fg=tcod.gold,
        string= f"${money}"
    )

    # Render states
    console.print(
        x=22, y=settings.tooltip_y - 2, fg=tcod.red,
        string=f"{player.states.to_string()}"
    )


def render_names_at_mouse_location(console, x, y, engine):
    """ takes the console, x and y coordinates (the location to draw the names), and the engine.
    From the engine, it grabs the mouse’s current x and y positions, and passes them to get_names_at_location,
    which we can assume for the moment will return the list of entity names we want. Once we have these entity
    names as a string, we can print that string to the given x and y location on the screen, with console.print.
    """
    mouse_x, mouse_y = engine.mouse_location

    names_at_mouse_location = engine.game_map.get_names_at(
        x=mouse_x,
        y=mouse_y - settings.msg_panel_height,      # Need to correct for message window offset.
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
                console.print(
                    x=entity.x,
                    y=entity.y,
                    string=entity.char,
                    fg=entity.color
                )

        # Also remember items/traps that are on explored tiles
        if game_map.explored[entity.x, entity.y]:
            item_or_trap = "item" in entity or "trap" in entity
            if item_or_trap and "hidden" not in entity:
                console.print(
                    x=entity.x,
                    y=entity.y,
                    string=entity.char,
                    fg=entity.color
                )

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

    log_console.print_box(
        0, 0, log_console.width, 1, title, alignment=tcod.CENTER
    )

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
    qty_of_items = len(engine.player.inventory.item_dict)
    item_groups = engine.player.inventory.sorted_dict()

    height_for_groups = (len(item_groups) * 2)
    padding_space = 2
    height = qty_of_items + height_for_groups + padding_space

    if height <= 3:
        height = 3

    # TODO: Design decision, should inventory stay in one place?
    x = console.width // 2
    # if engine.player.x <= 30:
    #     x = 40
    # else:
    #     x = 0

    y = 0

    # width = len(title) + 10
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
        for char in settings.ITEM_CATEGORIES:
            groups = item_groups.get(char)
            if groups:
                group_name = settings.ITEM_CATEGORIES[char]
                console.print(x + 1, y + i + 1, f" {char}  {group_name}:")
                i += 1
            else:
                continue

            for group in groups:
                for letter in group:
                    item_key = letter
                    item = engine.player.inventory.item_dict[letter]
                    is_equipped = engine.player.equipment.is_equipped(item)
                    if "stackable" in item:
                        qty = item.stackable.size
                    else:
                        qty = 1

                    if qty > 1:
                        # Pluralize the last word
                        item_string = f"({item_key}) {qty} {utils.pluralize_str(item.name)}"
                    else:

                        item_string = f"({item_key}) {item.name}"

                    # Weapon notation strings
                    if "equippable" in item and isinstance(item.equippable, Weapon):
                        dnotation = item.equippable.attack_comp.attacks[0].to_text()
                        item_string += f"({dnotation})"

                    if is_equipped:
                        item_string += f" (Equipped)"

                    console.print(x + 1, y + i + 1, item_string)
                    i += 1
            i += 1  # Adds a space between categories

    else:
        console.print(x + 1, y + 1, "(Empty)")


def highlight_cursor(console, x, y):
    """Highlights the specified coordinate with a white background and black foreground. """
    console.tiles_rgb["bg"][x, y] = color.white
    console.tiles_rgb["fg"][x, y] = color.black


def hilite_radius(console, x, y, radius):
    """Highlights the area surrounding the specified coordinates. """
    # Highlight the affected tiles.
    max_x = x + radius
    min_x = x - radius
    max_y = y + radius
    min_y = y - radius

    for x2 in range(min_x, max_x + 1):
        for y2 in range(min_y, max_y + 1):
            if distance(x, y, x2, y2) <= radius:
                console.tiles_rgb["bg"][x2, y2] = color.red
                console.tiles_rgb["fg"][x2, y2] = color.black


def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


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


def render_levelup_menu(console, engine, title):
    """Deprecated: Renders the level up menu for the player when the reach a new level. """
    if engine.player.x <= 30:
            x = 40
    else:
        x = 0

    console.draw_frame(
        x=x, y=0,
        width=35,
        height=8,
        title=title,
        clear=True,
        fg=(255, 255, 255),
        bg=(0, 0, 0),
    )

    console.print(x=x + 1, y=1, string="Congratulations! You level up!")
    console.print(x=x + 1, y=2, string="Select an attribute to increase.")

    console.print(
        x=x + 1, y=4,
        string=f"a) Constitution (+20 HP, from {engine.player.fighter.max_hp})",
    )
    console.print(
        x=x + 1, y=5,
        string=f"b) Strength (+1 attack, from {engine.player.attributes.strength})",
    )
    console.print(
        x=x + 1, y=6,
        string=f"c) Agility (+1 defense, from {engine.player.fighter.ac})",
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
