import logger
import textwrap

log = logger.get_logger(__name__)


class Message:
    def __init__(self, text):
        self.plain_text = text
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


class MessageLog:
    def __init__(self):
        log.debug("Initializing MessageLog")
        self.messages = []

    def add_message(self, text, *, stack=True):
        """Add a message to this log.
            `text` is the message text, `fg` is the text color.
            If `stack` is True then the message can stack with a previous message
            of the same text.
        """
        log.debug(f"msg: {text}")
        if stack and self.messages and text == self.messages[-1].plain_text:
            self.messages[-1].count += 1
        else:
            self.messages.append(Message(text))

    @staticmethod
    def wrap(string, width):
        """Return a wrapped text message."""
        for line in string.splitlines():  # Handle newlines in messages.
            yield from textwrap.wrap(
                line, width, expand_tabs=True,
            )

