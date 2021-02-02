class Component:
    # entity: Entity  # Owning entity instance.
    parent = None

    @property
    def gamemap(self):
        if self.parent:
            return self.parent.gamemap

    @property
    def engine(self):
        if self.parent:
            return self.gamemap.engine
