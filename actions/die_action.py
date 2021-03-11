from actions.actions import Action
from src.renderorder import RenderOrder


class DieAction(Action):
    """This action kills an actor and converts it's stats to a dead corpse. If the death was caused by
    another actor, that actor will get experience points for the kill.
    """
    def __init__(self, entity, cause):
        super().__init__(entity)
        self.cause = cause

    def perform(self):
        """Performs the death of the entity."""
        trap_cause = "trap" in self.cause

        if self.entity.has_comp("player"):
            self.msg = "You died!"

        # TODO: Update with component type/breed check
        elif self.cause.has_comp("player"):
            self.msg = f"You kill the {self.entity.name}!"

            # You get xp for the kill
            self.cause.level.add_xp(self.entity.level.xp_given)
        else:
            self.msg = f"The {self.cause.name} kills the {self.entity.name}!"

            # Traps don't get xp...
            if not trap_cause:
                # The causing entity gets xp for the kill
                self.cause.level.add_xp(self.entity.level.xp_given)

        # Kill the entity
        self.entity.char = "%"
        self.entity.blocks_movement = False
        self.entity.ai = None
        if self.entity.has_comp("player"):
            self.entity.name = f"player corpse"
        else:
            self.entity.name = f"{self.entity.name} corpse"

        self.entity.render_order = RenderOrder.CORPSE
