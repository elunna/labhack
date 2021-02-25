from src import utils


def test_myround__0():
    result = utils.myround(0)
    assert result == 0


def test_myround__default_base_25__5_rounds_to_0():
    assert utils.myround(5) == 0


def test_myround__default_base_25__12_rounds_to_0():
    assert utils.myround(12) == 0


def test_myround__default_base_25__12_5_rounds_to_0():
    assert utils.myround(12.5) == 0


def test_myround__default_base_25__13_rounds_to_25():
    assert utils.myround(13) == 25


def test_myround__default_base_25__20_rounds_to_0():
    assert utils.myround(20) == 25


def test_myround__default_base_25__25_rounds_to_25():
    assert utils.myround(25) == 25


def test_myround__default_base_25__26_rounds_to_25():
    assert utils.myround(26) == 25
