from components.equipment import Equipment
from components.inventory import Inventory
from components.states import StatesComponent
from src import entity
from src.renderorder import RenderOrder


class Actor(entity.Entity):
    """Defines an entity which is capable of moving and performing actions. An actor is either
    dead of alive, depending on their hit points.
    """
    def __init__(
            self, *,
            name,
            char,
            color=(255, 255, 255),
            x=-1,
            y=-1,
            transparent=True,

            fighter,
            ai,
            attack_comp,
            level,
            energy,
            inventory=Inventory(capacity=0),
            equipment=Equipment(),
            states=StatesComponent(),
            attributes=None,
            regeneration=None
    ):
        super().__init__(
            name=name,
            char=char,
            color=color,
            x=x,
            y=y,

            blocks_movement=True,
            render_order=RenderOrder.ACTOR,
            transparent=transparent,

            fighter=fighter,
            ai=ai,
            attack_comp=attack_comp,
            level=level,
            energy=energy,
            inventory=inventory,
            equipment=equipment,
            states=states,
        )


        if attributes:
            self.add_comp(attributes=attributes)
        if regeneration:
            self.add_comp(regeneration=regeneration)

    @property
    def is_alive(self):
        """Returns True as long as this actor can perform actions."""
        # return bool(self.ai)
        return not self.fighter.is_dead()
