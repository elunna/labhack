"""Handle the loading and initialization of game sessions."""
from . import color
from . import factory
from .engine import Engine
import lzma
import pickle


def new_game():
    """Return a brand new game session as an Engine instance."""
    player = factory.make("player")
    engine = Engine(player=player)

    new_map = engine.dungeon.current_map

    # Add player
    startx, starty = new_map.upstairs_location
    new_map.place(player, startx, starty)
    new_map.player = player

    engine.update_fov()

    engine.msglog.add_message(
        "You have entered what appears to be an abandoned research facility, or is it...", color.welcome_text
    )

    dagger = factory.make("dagger")
    player.inventory.add_inv_item(dagger)
    player.equipment.toggle_equip(dagger)

    leather_armor = factory.make("leather vest")
    player.inventory.add_inv_item(leather_armor)
    player.equipment.toggle_equip(leather_armor)

    starting_items = [
        "healing vial",
        "lightning scroll",
        "confusion scroll",
        "fireball scroll",
    ]

    for item in starting_items:
        new_item = factory.make(item)
        player.inventory.add_inv_item(new_item)

    return engine


def load_game(filename):
    """Load an Engine instance from a file."""
    with open(filename, "rb") as f:
        engine = pickle.loads(lzma.decompress(f.read()))

    assert isinstance(engine, Engine)
    return engine
