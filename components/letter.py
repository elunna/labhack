from components.component import Component
from src import settings


class LetterComponent(Component):
    def __init__(self, letter):
        # The money symbol ($) is okay too.
        if letter not in settings.VALID_INV_LETTERS + "$":
            raise ValueError(f'Letter must be one of: {settings.VALID_INV_LETTERS}')
        self.letter = letter
