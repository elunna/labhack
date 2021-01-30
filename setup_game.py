"""Handle the loading and initialization of game sessions."""
import color
import entity_factories
import settings
from engine import Engine
from game_world import GameWorld
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
    dagger = copy.deepcopy(entity_factories.dagger)
    dagger.parent = player.inventory
    player.inventory.items.append(dagger)
    player.equipment.toggle_equip(dagger, add_message=False)

    leather_armor = copy.deepcopy(entity_factories.leather_armor)
    leather_armor.parent = player.inventory
    player.inventory.items.append(leather_armor)
    player.equipment.toggle_equip(leather_armor, add_message=False)

    # For debugging purposes, add every item to player's inventory
    health_potion = copy.deepcopy(entity_factories.health_potion)
    health_potion.parent = player.inventory
    player.inventory.items.append(health_potion)

    confusion_potion = copy.deepcopy(entity_factories.confusion_potion)
    confusion_potion.parent = player.inventory
    player.inventory.items.append(confusion_potion)

    paralysis_potion = copy.deepcopy(entity_factories.paralysis_potion)
    paralysis_potion.parent = player.inventory
    player.inventory.items.append(paralysis_potion)

    lightning_scroll = copy.deepcopy(entity_factories.lightning_scroll)
    lightning_scroll.parent = player.inventory
    player.inventory.items.append(lightning_scroll)

    confusion_scroll = copy.deepcopy(entity_factories.confusion_scroll)
    confusion_scroll.parent = player.inventory
    player.inventory.items.append(confusion_scroll)

    fireball_scroll = copy.deepcopy(entity_factories.fireball_scroll)
    fireball_scroll.parent = player.inventory
    player.inventory.items.append(fireball_scroll)

    return engine


def load_game(filename):
    """Load an Engine instance from a file."""
    with open(filename, "rb") as f:
        engine = pickle.loads(lzma.decompress(f.read()))

    assert isinstance(engine, Engine)
    return engine


def save_as(game_engine, filename):
    """Save an Engine instance as a compressed file."""
    # pickle serializes an object hierarchy in Python.
    # lzma compresses the data

    save_data = lzma.compress(pickle.dumps(game_engine))

    with open(filename, "wb") as f:
        f.write(save_data)
