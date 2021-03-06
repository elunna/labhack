class EnergyMeter(object):
    def __init__(self, threshold):
        self.threshold = threshold
        self.energy = 0

    def add_energy(self, amt):
        self.energy += amt

    def burn_turn(self):
        if self.energy >= self.threshold:
            self.energy -= self.threshold
            return True
        return False

    def burned_out(self):
        return self.energy < self.threshold
