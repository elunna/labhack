from enum import Enum, auto
import tcod.event

""" This is a collection of all the constants used in the project."""

author = "Erik Lunna"
email = "eslunna@gmail.com"
title = "Lab Hack Version 1.0"
pypi_title = 'labhack'
title_extended = "Lab Hack: A Roguelike Venture in Super-Science!"
short_description = 'A super-science roguelike'

github="https://github.com/elunna/labhack"

version = '0.0.2'

"""Filename info """
tileset = "images/dejavu10x10_gs_tc.png"
bg_img = "images/menu_background.png"
save_file = "savegame.sav"

fov_radius = 8

# EnergyMeter and speed settings
energy_per_turn = 10  # The standard energy gained per turn

# These are thresholds based around the energy regeneration
# TODO: Use an Enum instead?
very_slow = 18
slow = 14
normal = 10
fast = 6
very_fast = 4


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
stat_str_x = 22
stat_def_x = 30
stat_xl_x = 40
stat_turns_x = 50

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

DIRECTIONS = [
    (-1, -1),  # Northwest
    (0, -1),  # North
    (1, -1),  # Northeast
    (-1, 0),  # West
    (1, 0),  # East
    (-1, 1),  # Southwest
    (0, 1),  # South
    (1, 1),  # Southeast
    (0, 0),  # None/Wait
]

CARDINAL_DIRECTIONS = [
    (0, -1),  # North
    (-1, 0),  # West
    (1, 0),  # East
    (0, 1),  # South
]

"""Enums"""


class RenderOrder(Enum):
    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()


class EquipmentType(Enum):
    WEAPON = auto()
    ARMOR = auto()


"""Constants for input keys
    For reference, these are the event codes for tcod.
    https://python-tcod.readthedocs.io/en/latest/tcod/event.html
"""
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
    tcod.event.K_SEMICOLON,
}

""" Entity Generation """

max_items_by_floor = [
    (1, 1),
    (4, 2),
]

max_monsters_by_floor = [
    (1, 2), # Levels 1-3
    (4, 3), # Levels 4-5 etc
    (6, 5),
]


item_chances = {
    # keys in the dictionary represent the floor number,
    # and the value is a list of tuples.
    # 0: [(health_potion, 35), (confusion_potion, 35)],
    0: [
        ("health potion", 35),
        ("paralysis potion", 5),
        ("confusion scroll", 10),
        ("lightning scroll", 25),
        ("fireball scroll", 25),
        ("leather armor", 15),
        ("dagger", 15),
        ("chain mail", 5),
        ("sword", 5),
    ],
}

enemy_chances = {
    0: [
        ('shrieker', 5),
        ('violet fungus', 5),
        ('lichen', 5),
        ('grid bug', 5),
        ('firefly', 5),
        ('brown mold', 5),
        ('yellow mold', 5),
        ('green mold', 5),
        ('red mold', 5),
    ],
    2: [
        ('troll', 15),
        ('gas spore', 10),
        ('yellow light', 10),
        ('black light', 10),
        ('flaming sphere', 10),
        ('freezing sphere', 10),
        ('shocking sphere', 10),
        ('spark bug', 10),
        ('orc', 10),
    ],
    3: [
        ('jiggling blob', 20),
        ('lava blob', 20),
        ('static blob', 20),
        ('burbling blob', 20),
        ('quivering blob', 20),
        ('arc bug', 20),
        ('acid blob', 20),
    ],
    4: [
        ('gelatinous cube', 50),
        ('disgusting mold', 50),
        ('black mold', 50),
        ('lightning bug', 50),
    ],
}
