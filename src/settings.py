from enum import Enum, auto
import tcod.event

""" This is a collection of all the constants used in the project."""

author = "Erik Lunna"
email = "eslunna@gmail.com"
title = "Lab Hack Version 1.0"
title_extended = "Lab Hack: A Roguelike Venture in Super-Science!"
short_description = 'A super-science roguelike'

github="https://github.com/elunna/labhack"

version = '0.0.2'

"""Filename info """
tileset = "images/dejavu10x10_gs_tc.png"
bg_img = "images/menu_background.png"
save_file = "../savegame.sav"

fov_radius = 8

# Define screen dimensions
screen_width = 80
screen_height = 55

# Main Menu
menu_width = 24

# Message Panel
msg_panel_y = 0
msg_panel_x = 1
msg_panel_width = screen_width - 10
msg_panel_height = 5

# Map Panel
map_panel_y = msg_panel_height
map_width = 80
map_height = 45

# Stat Panel
stat_panel_y = msg_panel_height + map_height
stat_panel_height = 5

hp_bar_x = 0
hp_bar_y = 0
hp_bar_width = 20
hp_bar_height = 1

dlevel_text_location = (0, 1)

tooltip_x = 0
tooltip_y = 4

# Room Generation
room_max_size = 10
room_min_size = 6
max_rooms = 30

# Entity settings
max_items_by_floor = [
    (1, 1),
    (4, 2),
]

max_monsters_by_floor = [
    (1, 2), # Levels 1-3
    (4, 3), # Levels 4-5 etc
    (6, 5),
]

DIRECTIONS = [
    (-1, -1),  # Northwest
    (0, -1),  # North
    (1, -1),  # Northeast
    (-1, 0),  # West
    (1, 0),  # East
    (-1, 1),  # Southwest
    (0, 1),  # South
    (1, 1),  # Southeast
]

"""Enums"""


class RenderOrder(Enum):
    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()


class EquipmentType(Enum):
    WEAPON = auto()
    ARMOR = auto()


"""Constants for input keys"""

MOVE_KEYS = {
    # Arrow keys.
    tcod.event.K_UP: (0, -1),
    tcod.event.K_DOWN: (0, 1),
    tcod.event.K_LEFT: (-1, 0),
    tcod.event.K_RIGHT: (1, 0),
    tcod.event.K_HOME: (-1, -1),
    tcod.event.K_END: (-1, 1),
    tcod.event.K_PAGEUP: (1, -1),
    tcod.event.K_PAGEDOWN: (1, 1),

    # Numpad keys.
    tcod.event.K_KP_1: (-1, 1),
    tcod.event.K_KP_2: (0, 1),
    tcod.event.K_KP_3: (1, 1),
    tcod.event.K_KP_4: (-1, 0),
    tcod.event.K_KP_6: (1, 0),
    tcod.event.K_KP_7: (-1, -1),
    tcod.event.K_KP_8: (0, -1),
    tcod.event.K_KP_9: (1, -1),

    # Vi keys.
    tcod.event.K_h: (-1, 0),
    tcod.event.K_j: (0, 1),
    tcod.event.K_k: (0, -1),
    tcod.event.K_l: (1, 0),
    tcod.event.K_y: (-1, -1),
    tcod.event.K_u: (1, -1),
    tcod.event.K_b: (-1, 1),
    tcod.event.K_n: (1, 1),
}

WAIT_KEYS = {
    tcod.event.K_PERIOD,
    tcod.event.K_KP_5,
    tcod.event.K_CLEAR,
}

CURSOR_Y_KEYS = {
    tcod.event.K_UP: -1,
    tcod.event.K_DOWN: 1,
    tcod.event.K_PAGEUP: -10,
    tcod.event.K_PAGEDOWN: 10,
}

CONFIRM_KEYS = {
    tcod.event.K_RETURN,
    tcod.event.K_KP_ENTER,
}
