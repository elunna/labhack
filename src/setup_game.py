"""Handle the loading and initialization of game sessions."""
from . import color
from . import factory
from . import gameworld
from .engine import Engine
import copy
import lzma
import pickle


def new_game():
    """Return a brand new game session as an Engine instance."""
    player = copy.deepcopy(factory.player)

    engine = Engine(player=player)

    engine.game_world = gameworld.GameWorld(engine)

    engine.game_world.generate_floor()
    engine.update_fov()

    engine.msglog.add_message(
        "Hello and welcome, adventurer, to yet another dungeon!", color.welcome_text
    )

    dagger = copy.deepcopy(factory.dagger)
    player.inventory.add_item(dagger)
    player.equipment.toggle_equip(dagger)

    leather_armor = copy.deepcopy(factory.leather_vest)
    player.inventory.add_item(leather_armor)
    player.equipment.toggle_equip(leather_armor)

    # For debugging purposes, add every item to player's inventory
    # TODO: Factory for making these

    # Health Potion
    health_potion = copy.deepcopy(factory.health_potion)
    player.inventory.add_item(health_potion)

    # Lightning scroll
    lightning_scroll = copy.deepcopy(factory.lightning_scroll)
    player.inventory.add_item(lightning_scroll)

    # Confusion scroll
    confusion_scroll = copy.deepcopy(factory.confusion_scroll)
    player.inventory.add_item(confusion_scroll)

    # Fireball scroll
    fireball_scroll = copy.deepcopy(factory.fireball_scroll)
    player.inventory.add_item(fireball_scroll)

    return engine


def load_game(filename):
    """Load an Engine instance from a file."""
    with open(filename, "rb") as f:
        engine = pickle.loads(lzma.decompress(f.read()))

    assert isinstance(engine, Engine)
    return engine
