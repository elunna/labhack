from typing import Union

import tcod.event

import actions.actions

"""An event handler return value which can trigger an action or switch active handlers.

    If a handler is returned then it will become the active handler for future events.
    If an action is returned it will be attempted and if it's valid then
    MainGameEventHandler will become the active handler.
"""
ActionOrHandler = Union[actions.actions.Action, "BaseEventHandler"]


class BaseEventHandler(tcod.event.EventDispatch[ActionOrHandler]):
    def handle_events(self, event):
        """Handle an event and return the next active event handler."""
        state = self.dispatch(event)

        if isinstance(state, BaseEventHandler):
            return state

        assert not isinstance(state, actions.actions.Action), f"{self!r} can not handle actions."
        return self

    def on_render(self, renderer):
        raise NotImplementedError()

    def ev_quit(self, event):
        raise SystemExit()