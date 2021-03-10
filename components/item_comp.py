from .component import Component


class ItemComponent(Component):
    """An entity which has this component is defined as an Item. If the player picks up an
    item it keeps track of the letter used so it can be reused if dropped.
    """
    pass
