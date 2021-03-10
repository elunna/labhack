import tcod

from src.actor import Actor
from src.player import Player


def test_init__is_Actor():
    p = Player()
    assert isinstance(p, Actor)


def test_init__has_player_component():
    p = Player()
    assert p.has_comp("player")


def test_init__char_is_at_symbol():
    p = Player()
    assert p.char == "@"


def test_init__color_is_white():
    p = Player()
    assert p.color == tcod.white


def test_init__ai_is_None():
    p = Player()
    assert p.has_comp("ai")
    assert p.ai is None


def test_init__has_equipment():
    p = Player()
    assert p.has_comp("equipment")


def test_init__has_fighter():
    p = Player()
    assert p.has_comp("fighter")


def test_init__fighter_ac_10():
    p = Player()
    assert p.fighter.ac == 10


def test_init__fighter_hp_30_max():
    p = Player()
    assert p.fighter.max_hp == 30


def test_init__has_attack_comp():
    p = Player()
    assert p.has_comp("attack_comp")


def test_init__has_attributes():
    p = Player()
    assert p.has_comp("attributes")


def test_init__has_player_inventory():
    p = Player()
    assert p.has_comp("inventory")


def test_init__has_level():
    p = Player()
    assert p.has_comp("level")


def test_init__level_starts_at_level_1():
    p = Player()
    assert p.level.current_level == 1


def test_init__level_starts_at_0_xp():
    p = Player()
    assert p.level.current_xp == 0


def test_init__has_energycomponent():
    p = Player()
    assert p.has_comp("energy")


def test_init__energy_refill_starts_at_12():
    p = Player()
    assert p.energy.refill == 12


def test_init__has_regeneration():
    p = Player()
    assert p.has_comp("regeneration")
