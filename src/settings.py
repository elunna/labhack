""" This is a collection of all the constants used in the project."""

author = "Erik Lunna"
title = "Lab Hack Version 1.0"
title_extended = "Lab Hack: A Roguelike Venture in Super-Science!"

version = 1.0

"""Filename info """
tileset = "images/dejavu10x10_gs_tc.png"
bg_img = "images/menu_background.png"
save_file = "savegame.sav"

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
max_rooms = 3

# Entity settings
energy_per_turn = 10  # This is how much energy each actor regains per turn
DEFAULT_THRESHOLD = 10

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

CARDINAL_DIR = {
    'N': (0, -1),  # North
    'W': (-1, 0),  # West
    'E': (1, 0),  # East
    'S': (0, 1),  # South
}

ITEM_CATEGORIES = {
    # Sets the order that the inventory is displayed in.
    '/': "Weapons",
    '[': "Armor",
    '%': "Edibles",
    '!': "Potions",
    '~': "Scrolls"
}

# Slashem implements AC bonus for dexterity
dex_ac_bonus_table = {
    0: 3,
    1: 3,
    2: 3,
    3: 3,
    4: 2,
    5: 2,
    6: 1,
    7: 1,
    8: 0,
    9: 0,
    10: 0,
    11: 0,
    12: 0,
    13: 0,
    14: 0,
    15: -1,
    16: -2,
    17: -3,
    18: -4,
    19: -5,
    20: -6,
    21: -6,
    22: -7,
    23: -7,
    24: -8,
    25: -8
}

# Is this bonus for to-hit or damage?
strength_bonus_table = {
    3: -2,
    4: -2,
    5: -2,
    6: -1,
    7: -1,
    8: 0,
    9: 0,
    10: 0,
    11: 0,
    12: 0,
    13: 0,
    14: 0,
    15: 0,
    16: 0,
    17: 1,
    18: 1,
    # 17-18 / 50 + 1
    # 18 / 51 to 18 / 99 + 2
    # 18 / ** to
}
