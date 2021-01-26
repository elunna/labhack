from src.entity import Entity
from src.settings import RenderOrder


class Item(Entity):
    def __init__(
        self, *,
        x=0, y=0,
        char="?",
        color=(255, 255, 255),
        name="<Unnamed>",
        consumable=None,
        equippable=None,
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=False,
            render_order=RenderOrder.ITEM,
        )

        self.consumable = consumable

        if self.consumable:
            self.consumable.parent = self

        self.equippable = equippable

        if self.equippable:
            self.equippable.parent = self