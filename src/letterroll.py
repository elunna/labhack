from src import settings


class LetterRoll:
    """This manages a collection of letters that are mainly used for the inventory.
    The letter maintains a position (letter) in the roll, and can be called on to find a next letter.
    """
    def __init__(self):
        self.letters = settings.VALID_INV_LETTERS
        self.index = -1

    def __len__(self):
        """Returns how many letters are in the current collection of letters."""
        return len(self.letters)

    def next_letter(self):
        """ Advances the index by one and returns the next letter.

        :return: The next letter represented by the index.
        """
        self.index += 1
        i = self.index % len(self.letters)
        return self.letters[i]
