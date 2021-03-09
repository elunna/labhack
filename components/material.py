from components.component import Component


class MaterialComponent(Component):
    """Defines the type of material that an item or entity is constructed from."""
    def __init__(self, material):
        self.material = material
