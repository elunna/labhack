from components.component import Component


class LetterComponent(Component):
    def __init__(self, letter=None):
        # TODO: Restrict letters to lowercase alphabet.
        self.letter = letter
