from components.equipment import Equipment
from components.inventory import Inventory
from components.states import StatesComponent
from src import entity
from src.renderorder import RenderOrder

default_components = {
    "x": -1,
    "y": -1,
    "color": (255, 255, 255),
    "transparent": True,
    "blocks_movement": True,
    "render_order": RenderOrder.ACTOR,
    "actor": True  # Included for all Actors
}


class Actor(entity.Entity):
    """Defines an entity which is capable of moving and performing actions. An actor is either
    dead of alive, depending on their hit points.
    """
    def __init__(self, **kwargs):
        super().__init__()

        # Set the default core components for an Actor
        self.add_comp(**default_components)

        # Set the custom components afterward
        self.add_comp(**kwargs)

        if not self.has_comp("inventory"):
            self.add_comp(inventory=Inventory(capacity=0))

        if not self.has_comp("equipment"):
            self.add_comp(equipment=Equipment())

        if not self.has_comp("states"):
            self.add_comp(states=StatesComponent())

    @property
    def is_alive(self):
        """Returns True as long as this actor can perform actions."""
        # return bool(self.ai)
        return not self.fighter.is_dead()
