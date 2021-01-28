class BaseComponent:
    # entity: Entity  # Owning entity instance.
    parent = None

    @property
    def gamemap(self):
        return self.parent.gamemap

    @property
    def engine(self):
        return self.gamemap.engine
