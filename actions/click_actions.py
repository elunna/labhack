from actions.pickup_action import PickupAction
from actions.actions import Action
from actions.search_action import SearchAction


class ClickSelfAction(Action):
    """Like Bump but for handling clicking yourself!)"""

    def perform(self):
        gamemap = self.entity.gamemap
        # Check for any items on the current tile
        items = gamemap.filter("item", x=self.entity.x, y=self.entity.y)
        if items:
            return PickupAction(self.entity)
        else:
            return SearchAction(self.entity)
