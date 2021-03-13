from components.component import Component


class LightComponent(Component):
    """Manages the light eminating from an entity."""
    def __init__(self, radius=1):
        self.radius = radius

    def area(self):
        """Square area"""
        x = self.parent.x
        y = self.parent.y

        return {(x2, y2) for x2 in range(x - self.radius, x + self.radius + 1)
                for y2 in range(y - self.radius, y + self.radius + 1)}
