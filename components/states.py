from components.component import Component

AUTO_STATES = ["paralyzed", "sleeping", "raving mad", "frozen", "fainted"]


class StatesComponent(Component):
    """ This is an attempt to manage the durations of states like:
        * confused
        * sleeping
        * paralyzed
        * hallucinating
        * stunned
        * hungry, weak, starving, fainting

    """
    def __init__(self):
        # A dict of states and their timeouts.
        self.states = {}

    @property
    def autopilot(self):
        """ Tells us if the actor has a state which renders it incapable of controlling it's own actions. """
        for state in self.states:
            if state in AUTO_STATES:
                return True
        return False

    def add_state(self, new_state, timeout):
        # If the state is already in, just add to it.
        if new_state in self.states:
            self.states[new_state] += timeout
        else:
            self.states[new_state] = timeout

    def decrease(self):
        """Decreases all the timeouts on all the states by one. If any timeouts reach 0, we remove the
        state. We also return a list of all the states that were deleted.
        """
        # Decrease the timeout on all states by 1.
        to_remove = []

        for state in self.states:
            self.states[state] -= 1
            if self.states[state] <= 0:
                to_remove.append(state)

        # Remove any states with 0 timeout
        for state in to_remove:
            self.states.pop(state)

        return to_remove

    def to_string(self):
        return ", ".join(f"{k}({v})" for k, v in self.states.items())

