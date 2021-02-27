from components.component import Component


class WeightComponent(Component):
    def __init__(self, weight):
        if weight <= 0:
            raise ValueError("Invalid weight, weight must be a positive integer!")
        self.weight = weight