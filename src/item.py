from components.item_comp import ItemComponent
from src import entity
from src.renderorder import RenderOrder


class Item(entity.Entity):
    def __init__(
        self, *,
        x=0, y=0,
        char="?",
        color=(255, 255, 255),
        name="<Unnamed>",
        consumable=None,
        equippable=None,
        stackable=None,
        item=ItemComponent(),
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=False,
            render_order=RenderOrder.ITEM,
            item=item
        )

        self.add_comp(consumable=consumable)
        self.add_comp(equippable=equippable)
        self.add_comp(transparent=True)
        if stackable:
            self.add_comp(stackable=stackable)