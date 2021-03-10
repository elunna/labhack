from components.item_comp import ItemComponent
from src import entity
from src.renderorder import RenderOrder

default_components = {
    "x": -1,
    "y": -1,
    "color": (255, 255, 255),
    "transparent": True,
    "blocks_movement": False,
    "render_order": RenderOrder.ITEM,
}


class Item(entity.Entity):
    """Represents items in the game."""
    def __init__(self, **kwargs):
        super().__init__()

        # Set the default core components for an Actor
        self.add_comp(**default_components)

        # Set the custom components afterward
        self.add_comp(**kwargs)

        self.add_comp(item=ItemComponent())
