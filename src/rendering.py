from . import color
from . import msglog
from . import settings
from . import tiles
import numpy as np
import tcod


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
        y=mouse_y - settings.msg_panel_height,  # Hack: correct for message window offset.
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
        for line in reversed(list(msglog.MsgLog.wrap(message.full_text, width))):
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
        default=tiles.SHROUD,
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

def render_history(console, engine, cursor):
    log_console = tcod.Console(console.width - 6, console.height - 6)

    # Draw a frame with a custom banner title.
    log_console.draw_frame(0, 0, log_console.width, log_console.height)

    log_console.print_box(
        0, 0, log_console.width, 1, "┤Message history├", alignment=tcod.CENTER
    )

    # Render the message log using the cursor parameter.
    # self.engine.message_log.render_messages(
    render_messages(
        console=log_console,
        x=1, y=1,
        width=log_console.width - 2,
        height=log_console.height - 2,
        messages=engine.message_log.messages[: cursor + 1],
    )
    log_console.blit(console, 3, 3)


def render_inv(console, engine, title):
    number_of_items_in_inventory = len(engine.player.inventory.items)

    height = number_of_items_in_inventory + 2

    if height <= 3:
        height = 3

    if engine.player.x <= 30:
        x = 40
    else:
        x = 0

    y = 0

    width = len(title) + 4

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

    if number_of_items_in_inventory > 0:
        for i, item in enumerate(engine.player.inventory.items):
            item_key = chr(ord("a") + i)
            is_equipped = engine.player.equipment.item_is_equipped(item)

            item_string = f"({item_key}) {item.name}"

            if is_equipped:
                item_string = f"{item_string} (E)"

            console.print(x + 1, y + i + 1, item_string)
    else:
        console.print(x + 1, y + 1, "(Empty)")


