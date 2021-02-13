from src import entity
from src.renderorder import RenderOrder


class Actor(entity.Entity):
    def __init__(
            self, *,
            x=0, y=0,
            char="?",
            color=(255, 255, 255),
            name="<Unnamed>",
            ai_cls,
            equipment,
            fighter,
            attacks,
            attributes,
            inventory,
            level,
            energymeter,
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=True,
            render_order=RenderOrder.ACTOR,
        )

        self.add_comp(ai=ai_cls)
        self.add_comp(equipment=equipment)
        self.add_comp(fighter=fighter)
        self.add_comp(attacks=attacks)
        self.add_comp(attributes=attributes)
        self.add_comp(inventory=inventory)
        self.add_comp(level=level)
        self.add_comp(energymeter=energymeter)

    @property
    def is_alive(self):
        """Returns True as long as this actor can perform actions."""
        return bool(self.ai)
