from src import color
from src.message_log import MessageLog
from src import settings
from src import tile_types
import numpy as np
import tcod


class TcodRenderer:
    """ Handle all the rendering details that the engine requires."""
    pass


def render_bar(console, current_value, maximum_value, total_width):
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
    """ Render the level the player is currently on, at the given location.  """
    x, y = settings.dlevel_text_location

    console.print(x=x, y=y, string=f"Dlevel: {dungeon_level}")


def get_names_at_location(x, y, game_map):
    """ takes “x” and “y” variables, though these represent a spot on the map.
        We first check that the x and y coordinates are within the map, and are
        currently visible to the player. If they are, then we create a string of
        the entity names at that spot, separated by a comma. We then return that
        string, adding capitalize to make sure the first letter in the string is
        capitalized.
    """
    if not game_map.in_bounds(x, y) or not game_map.visible[x, y]:
        return ""

    names = ", ".join(
        entity.name for entity in game_map.entities if entity.x == x and entity.y == y
    )

    return names.capitalize()


def render_names_at_mouse_location(console, x, y, engine):
    """ takes the console, x and y coordinates (the location to draw the names),
        and the engine. From the engine, it grabs the mouse’s current x and y
        positions, and passes them to get_names_at_location, which we can assume
        for the moment will return the list of entity names we want. Once we
        have these entity names as a string, we can print that string to the
        given x and y location on the screen, with console.print.
    """
    mouse_x, mouse_y = engine.mouse_location

    names_at_mouse_location = get_names_at_location(
        x=mouse_x,
        y=mouse_y - settings.msg_panel_height,      # Need to correct for message window offset.
        game_map=engine.game_map
    )

    console.print(x=x, y=y, string=f"Looking at: {names_at_mouse_location}")


def render_messages(console, x, y, width, height, messages):
    """Render the messages provided. Render this log over the given area.
            `x`, `y`, `width`, `height` is the rectangular region to render onto
            the `console`.
    The `messages` are rendered starting at the last message and working
    backwards.
    """
    y_offset = height - 1

    for message in reversed(messages):
        for line in reversed(list(MessageLog.wrap(message.full_text, width))):
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
    console.tiles_rgb[0: game_map.width, 0: game_map.height] = np.select(
        # np.select allows us to conditionally draw the tiles we want, based on
        # what’s specified in condlist. Since we’re passing [self.visible, self.explored],
        # it will check if the tile being drawn is either visible, then explored.
        # If it’s visible, it uses the first value in choicelist, in this case,
        # self.tiles["light"]. If it’s not visible, but explored, then we draw
        # self.tiles["dark"]. If neither is true, we use the default argument,
        # which is just the SHROUD we defined earlier.

        condlist=[game_map.visible, game_map.explored],
        choicelist=[game_map.tiles["light"], game_map.tiles["dark"]],
        default=tile_types.SHROUD,
    )

    # Sort the entities by render order.
    entities_sorted_for_rendering = sorted(
        game_map.entities, key=lambda x: x.render_order.value
    )

    for entity in entities_sorted_for_rendering:
        # Only print entities that are in the FOV
        if game_map.visible[entity.x, entity.y]:
            console.print(
                x=entity.x,
                y=entity.y,
                string=entity.char,
                fg=entity.color
            )


def render_main_menu(console):
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


def render_char_scr(title, console, engine):
    if engine.player.x <= 30:
        x = 40
    else:
        x = 0

    y = 0

    width = len(title) + 4

    console.draw_frame(
        x=x, y=y,
        width=width,
        height=7,
        title=title,
        clear=True,
        fg=(255, 255, 255),
        bg=(0, 0, 0),
    )

    console.print(
        x=x + 1, y=y + 1,
        string=f"Level: {engine.player.level.current_level}"
    )
    console.print(
        x=x + 1, y=y + 2,
        string=f"XP: {engine.player.level.current_xp}"
    )
    console.print(
        x=x + 1, y=y + 3,
        string=f"XP for next Level: {engine.player.level.experience_to_next_level}",
    )

    console.print(
        x=x + 1, y=y + 4,
        string=f"Attack: {engine.player.fighter.power}"
    )
    console.print(
        x=x + 1, y=y + 5,
        string=f"Defense: {engine.player.fighter.defense}"
    )


def render_lvl_up_menu(title, console, engine):
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
        string=f"b) Strength (+1 attack, from {engine.player.fighter.power})",
    )
    console.print(
        x=x + 1, y=6,
        string=f"c) Agility (+1 defense, from {engine.player.fighter.defense})",
    )


def render_popup_msg(console, text):
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


def draw_rect(console, x, y, radius):
    # Draw a rectangle around the targeted area, so the player can see the affected tiles.
    console.draw_frame(
        x=x - radius - 1,
        y=y - radius - 1,
        width=radius ** 2,
        height=radius ** 2,
        fg=color.red,
        clear=False,
    )