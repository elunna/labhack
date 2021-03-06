""" Tests for actors.py """
import pytest

from components.ai import HostileAI, BaseAI
from components.attack import Attack
from components.attack_cmp import AttackComponent
from components.energy import EnergyComponent
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from src import factory
from src import entity
from src.actor import Actor


@pytest.fixture
def test_actor():
    components = {
        "char": "x",
        "color": (255, 255, 255),
        "ai_cls": HostileAI(),
        "fighter": Fighter(max_hp=1, base_ac=10),
        "attack_comp": AttackComponent(Attack('zap', [1])),
        "level": Level(xp_given=1, difficulty=0),
        "energy": EnergyComponent(threshold=10)
    }
    return Actor(name="actor", **components)


def test_init__is_Entity(test_actor):
    assert isinstance(test_actor, entity.Entity)


def test_init_xy(test_actor):
    assert test_actor.x == -1
    assert test_actor.y == -1


def test_init_char(test_actor):
    assert test_actor.char == "x"


def test_init_color(test_actor):
    assert test_actor.color == (255, 255, 255)


def test_init_name(test_actor):
    assert test_actor.name == "actor"


def test_init_ai_cls(test_actor):
    assert isinstance(test_actor.ai, BaseAI)


def test_init_fighter(test_actor):
    assert test_actor.fighter


def test_init_attack_comp(test_actor):
    assert isinstance(test_actor.attack_comp, AttackComponent)


def test_init_attributes(test_actor):
    # Not included by default, only for player
    assert "attributes" not in test_actor
    # assert isinstance(test_actor.attributes, Attributes)

# attributes for player


def test_init_level(test_actor):
    assert isinstance(test_actor.level, Level)


def test_init_energy(test_actor):
    assert isinstance(test_actor.energymeter, EnergyComponent)


def test_init_inventory(test_actor):
    assert isinstance(test_actor.inventory, Inventory)


def test_init_equipment(test_actor):
    assert test_actor.equipment


def test_is_alive(test_actor):
    assert test_actor.is_alive
