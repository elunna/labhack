class Attack:
    def __init__(self, name, dies):
        self.name = name
        self.dies = dies

    def min_dmg(self):
        return len(self.dies)

    def max_dmg(self):
        return sum(self.dies)