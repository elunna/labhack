"""Handle the loading and initialization of game sessions."""
from . import color
from . import entity_factories
from . import settings
from .engine import Engine
from .game_world import GameWorld
import copy
import lzma
import pickle


def new_game():
    """Return a brand new game session as an Engine instance."""
    player = copy.deepcopy(entity_factories.player)

    engine = Engine(player=player)

    engine.game_world = GameWorld(
        engine=engine,
        max_rooms=settings.max_rooms,
        room_min_size=settings.room_min_size,
        room_max_size=settings.room_max_size,
        map_width=settings.map_width,
        map_height=settings.map_height,
    )

    engine.game_world.generate_floor()
    engine.update_fov()

    engine.message_log.add_message(
        "Hello and welcome, adventurer, to yet another dungeon!", color.welcome_text
    )

    # No starting inventory for now...
    # dagger = copy.deepcopy(entity_factories.dagger)
    # leather_armor = copy.deepcopy(entity_factories.leather_armor)

    # dagger.parent = player.inventory
    # leather_armor.parent = player.inventory

    # player.inventory.items.append(dagger)
    # player.equipment.toggle_equip(dagger, add_message=False)

    # player.inventory.items.append(leather_armor)
    # player.equipment.toggle_equip(leather_armor, add_message=False)

    return engine


def load_game(filename):
    """Load an Engine instance from a file."""
    with open(filename, "rb") as f:
        engine = pickle.loads(lzma.decompress(f.read()))

    assert isinstance(engine, Engine)
    return engine
