from components.component import Component


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

    def add_state(self, new_state, timeout):
        # If the state is already in, just add to it.
        if new_state in self.states:
            self.states[new_state] += timeout
        else:
            self.states[new_state] = timeout

    def decrease(self):
        # Decrease the timeout on all states by 1.
        to_remove = []

        for state in self.states:
            self.states[state] -= 1
            if self.states[state] == 0:
                to_remove.append(state)

        # Remove any states with 0 timeout
        for state in to_remove:
            self.states.pop(state)

    def to_string(self):
        return ", ".join(f"{k}({v})" for k, v in self.states.items())

