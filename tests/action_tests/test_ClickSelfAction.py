import pytest

from actions.actions import Action
from actions.click_actions import ClickSelfAction
from tests import toolkit


@pytest.fixture
def hiddenmap():
    return toolkit.hidden_map()


def test_init__is_Action(hiddenmap):
    player = hiddenmap.player
    click = ClickSelfAction(player)
    assert isinstance(click, Action)
