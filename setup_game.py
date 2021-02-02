"""Handle the loading and initialization of game sessions."""
from engine import Engine
import game_world
import copy
import factories
import lzma
import pickle

import logger
log = logger.get_logger(__name__)


def new_game():
    """Return a brand new game session as an Engine instance."""
    log.debug('Initializing new game')

    player = copy.deepcopy(factories.player)

    engine = Engine(player=player)

    engine.game_world = game_world.GameWorld(engine=engine)

    engine.game_world.generate_floor()
    engine.update_fov()

    engine.msg_log.add_message("Hello and welcome, adventurer, to yet another dungeon!")

    log.debug('Granting player full spoiled inventory')

    dagger = factories.mk_item('dagger')
    dagger.parent = player.inventory
    player.inventory.items.append(dagger)
    player.equipment.toggle_equip(dagger, add_message=False)

    leather_armor = factories.mk_item('leather armor')
    leather_armor.parent = player.inventory
    player.inventory.items.append(leather_armor)
    player.equipment.toggle_equip(leather_armor, add_message=False)

    # For debugging purposes, add every item to player's inventory
    health_potion = factories.mk_item('health potion')
    health_potion.parent = player.inventory
    player.inventory.items.append(health_potion)

    confusion_potion = factories.mk_item('confusion potion')
    confusion_potion.parent = player.inventory
    player.inventory.items.append(confusion_potion)

    paralysis_potion = factories.mk_item('paralysis potion')
    paralysis_potion.parent = player.inventory
    player.inventory.items.append(paralysis_potion)

    lightning_scroll = factories.mk_item('lightning scroll')
    lightning_scroll.parent = player.inventory
    player.inventory.items.append(lightning_scroll)

    confusion_scroll = factories.mk_item('confusion scroll')
    confusion_scroll.parent = player.inventory
    player.inventory.items.append(confusion_scroll)

    fireball_scroll = factories.mk_item('fireball scroll')
    fireball_scroll.parent = player.inventory
    player.inventory.items.append(fireball_scroll)

    return engine


def load_game(filename):
    """Load an Engine instance from a file."""
    log.debug('Loading previous game.')

    with open(filename, "rb") as f:
        engine = pickle.loads(lzma.decompress(f.read()))

    assert isinstance(engine, Engine)
    return engine


def save_as(game_engine, filename):
    """Save an Engine instance as a compressed file."""
    # pickle serializes an object hierarchy in Python.
    # lzma compresses the data

    log.debug('Compressing save data')
    save_data = lzma.compress(pickle.dumps(game_engine))

    log.debug('Saving game.')
    with open(filename, "wb") as f:
        f.write(save_data)
