from actions.actions import Action


class WaitAction(Action):
    """Instructs the entity to do nothing this turn."""
    def perform(self) -> None:
        pass