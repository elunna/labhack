from src import utils


def test_distance__same_point_0():
    assert utils.distance(0, 0, 0, 0) == 0


def test_distance__1_sq_east_1():
    assert utils.distance(0, 0, 1, 0) == 1


def test_distance__1_sq_diagonal():
    result = utils.distance(0, 0, 1, 1)
    assert round(result, 2) == 1.41


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


def test_pluralize_last_word():
    result = utils.pluralize_str("healing vial")
    expected = "healing vials"
    assert result == expected
