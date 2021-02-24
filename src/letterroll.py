import string


class LetterRoll:
    def __init__(self):
        # self.letters = string.ascii_lowercase + string.ascii_uppercase
        self.letters = string.ascii_lowercase
        self.index = -1

    def __len__(self):
        return len(self.letters)

    def next_letter(self):
        self.index += 1
        i = self.index % len(self.letters)
        return self.letters[i]