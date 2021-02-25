"""Handle the loading and initialization of game sessions."""
from . import color
from . import factory
from . import dungeon
from .engine import Engine
import copy
import lzma
import pickle


def new_game():
    """Return a brand new game session as an Engine instance."""
    player = copy.deepcopy(factory.player)
    engine = Engine(player=player)

    engine.dungeon = dungeon.Dungeon(engine=engine)
    new_map = engine.dungeon.generate_floor()
    engine.dungeon.set_dlevel(1)

    # Add player
    new_map.entities.add(player)
    new_map.player = player

    # Place player on upstair.
    player.place(*new_map.upstairs_location, new_map)

    # Add the map to the engine
    engine.game_map = new_map

    # Add the engine to the map
    new_map.engine = engine

    engine.update_fov()

    engine.msglog.add_message(
        "You have entered what appears to be an abandoned research facility, or is it...", color.welcome_text
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
