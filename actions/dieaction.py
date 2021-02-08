from actions.actions import Action
from src.renderorder import RenderOrder


class DieAction(Action):
    def __init__(self, entity, cause):
        super().__init__(entity)
        self.cause = cause

    def perform(self):
        # TODO: What if the cause is a non-actor? Trap, drowning, bomb, etc.

        # if self.entity == self.engine.player:
        if self.entity.name == "Player":
            self.msg = "You died!"
        elif self.cause.name == "Player":
            self.msg = f"You kill the {self.entity.name}!"

            # You get xp for the kill
            self.cause.level.add_xp(self.entity.level.xp_given)
        else:
            self.msg = f"The {self.cause.name} kills the {self.entity.name}!"

            # The causing entity gets xp for the kill
            self.cause.level.add_xp(self.entity.level.xp_given)

        # Kill the entity
        self.entity.char = "%"
        self.entity.color = (191, 0, 0)
        self.entity.blocks_movement = False
        self.entity.ai = None
        self.entity.name = f"{self.entity.name} corpse"
        self.entity.render_order = RenderOrder.CORPSE