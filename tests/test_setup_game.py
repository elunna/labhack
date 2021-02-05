""" Tests for setup_game.py """

from src import setup_game
from src.engine import Engine
from src.gameworld import GameWorld


def test_new_game__is_Engine():
    game = setup_game.new_game()
    assert isinstance(game, Engine)


def test_new_game__GameWorld():
    game = setup_game.new_game()
    assert isinstance(game.game_world, GameWorld)


def test_new_game__player():
    game = setup_game.new_game()
    assert game.player


def test_new_game__first_msg():
    game = setup_game.new_game()
    result = game.message_log.messages[0]
    assert result.plain_text == "Hello and welcome, adventurer, to yet another dungeon!"


# TODO: Test load_game with mocks
# def test_load_game
