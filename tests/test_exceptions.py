""" Tests for exceptions.py """
from src import exceptions


def test_Impossible__is_Exception():
    i = exceptions.Impossible()
    assert isinstance(i, Exception)


def test_QuitWithoutSaving__is_SystemExit():
    i = exceptions.QuitWithoutSaving()
    assert isinstance(i, SystemExit)
