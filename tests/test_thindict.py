import pytest
from src.thindict import ThinDict


def test_ThinDict__is_dict():
    td = ThinDict(allowed_keys=['a', 'b', 'c'])
    assert isinstance(td, dict)


def test_ThinDict__default_initialval_is_None():
    td = ThinDict(allowed_keys=['a', 'b', 'c'])
    assert td['a'] is None
    assert td['b'] is None


def test_ThinDict___initialval():
    td = ThinDict(allowed_keys=['a', 'b', 'c'], initial_val=1)
    assert td['a'] == 1
    assert td['b'] == 1


def test_ThinDict__valid_key():
    td = ThinDict(allowed_keys=['a', 'b', 'c'])
    td['a'] = 1
    assert td['a'] == 1

    # Try setting again
    td['a'] = 2
    assert td['a'] == 2


def test_ThinDict__invalid_key():
    td = ThinDict(allowed_keys=['a', 'b', 'c'])
    with pytest.raises(KeyError):
        td['d'] = 1
