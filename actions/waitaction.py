from actions.actions import Action


class WaitAction(Action):
    # Entity does nothing this turn
    def perform(self) -> None:
        pass