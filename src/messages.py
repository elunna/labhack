from . import color
import textwrap


class Msg:
    """Represents a single message in the game. Can have a corresponding color."""
    def __init__(self, text, fg=(255, 255, 255)):
        self.plain_text = text
        self.fg = fg  # Foreground color: Tuple[int, int, int]

        self.count = 1  # Shows how many times a msg is repeated
        # used to display something like “The Orc attacks (x3).” Rather than
        # crowding our message log with the same message over and over, we can
        # “stack” the messages by increasing a message’s count.

    @property
    def full_text(self):
        """The full text of this message, including the count if necessary."""
        if self.count > 1:
            return f"{self.plain_text} (x{self.count})"
        return self.plain_text


class MsgLog:
    """Manages the message history in the game."""
    def __init__(self):
        self.messages = []

    def add_message(self, text, fg=color.white, *, stack=True):
        """Add a message to this log.
            `text` is the message text, `fg` is the text color.
            If `stack` is True then the message can stack with a previous message
            of the same text.
        """
        if stack and self.messages and text == self.messages[-1].plain_text:
            self.messages[-1].count += 1
        else:
            self.messages.append(Msg(text, fg))

    @staticmethod
    def wrap(string, width):
        """Return a wrapped text message."""
        for line in string.splitlines():  # Handle newlines in messages.
            yield from textwrap.wrap(
                line, width, expand_tabs=True,
            )


class HelpInfo(MsgLog):
    """ Manages the help info and command reference in the game. Re-uses the message log and loads an
    outside help.txt file.
    """
    def __init__(self):
        super().__init__()
        with open('help.txt') as f:
            for line in f.readlines():
                self.add_message(line, stack=False)
