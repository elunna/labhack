from handlers.base_handler import BaseEventHandler
from src import rendering


class PopupMsgHandler(BaseEventHandler):
    """Display a popup text window."""

    def __init__(self, parent_handler, text):
        self.parent = parent_handler
        self.text = text

    def on_render(self, renderer):
        """Render the parent and dim the result, then print the message on top."""
        self.parent.on_render(renderer)
        rendering.render_popup(renderer.root, self.text)

    def ev_keydown(self, event):
        """Any key returns to the parent handler."""
        return self.parent