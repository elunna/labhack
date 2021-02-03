class Component:
    # entity: Entity  # Owning entity instance.
    parent = None

    @property
    def gamemap(self):
        """Return the game map this Component belongs to."""
        if self.parent:
            return self.parent.gamemap

    @property
    def engine(self):
        """Return the engine this Component belongs to."""
        if self.parent:
            return self.gamemap.engine
