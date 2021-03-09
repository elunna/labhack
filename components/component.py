class Component:
    """Represents a single component that can plug into an entity."""
    # entity: Entity  # Owning entity instance.
    parent = None

    @property
    def gamemap(self):
        """Returns the owning entity's gamemap reference."""
        return self.parent.gamemap

    @property
    def engine(self):
        """Returns the owning entity's gamemap's engine reference."""
        return self.gamemap.engine
