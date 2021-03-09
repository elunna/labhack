import tcod

from handlers.base_handler import BaseEventHandler
from src import settings, procgen, rendering
from src.maze import Maze


class MapDebugHandler(BaseEventHandler):
    """Display a random from the generator."""

    def __init__(self, parent_handler):
        self.parent = parent_handler
        self.max_rooms = settings.max_rooms
        self.room_min_size = settings.room_min_size
        self.room_max_size = settings.room_max_size
        self.room_max_distance = 30
        self.maze_path_width = 1
        self.map_func = self.generate_map
        self.mode = ''
        self.map = self.map_func()  # Do this last!

    def generate_map(self):
        self.mode = "ROOMS & CORRIDORS"
        # Generate a new map
        return procgen.generate_map(
            max_rooms=self.max_rooms,
            room_min_size=self.room_min_size,
            room_max_size=self.room_max_size,
            map_width=settings.map_width,
            map_height=settings.map_height,
            max_distance=self.room_max_distance,
            difficulty=1,
        )

    def generate_maze(self):
        self.mode = "MAZE"
        fitted_width, fitted_height = Maze.dimensions_to_fit(
            settings.map_width,
            settings.map_height,
            path_width=self.maze_path_width
        )
        m = Maze(width=fitted_width, height=fitted_height, path_width=self.maze_path_width)
        m.create_maze()
        return m.export_gamemap()

    def on_render(self, renderer):
        """Render the parent and dim the result, then print the message on top."""
        self.parent.on_render(renderer)

        # Set all tiles to visible
        self.map.visible[:] = True
        self.map.explored[:] = True

        rendering.render_map(renderer.root, self.map)
        # Render debug info
        rendering.render_map_debugger(
            console=renderer.root,
            mode=self.mode,
            max_rooms=self.max_rooms,
            min_size=self.room_min_size,
            max_size=self.room_max_size,
            max_dist=self.room_max_distance,
            maze_path=self.maze_path_width,
        )

    def ev_keydown(self, event):
        """Any key returns to the parent handler."""
        key = event.sym
        modifier = event.mod

        if modifier & (tcod.event.KMOD_LSHIFT | tcod.event.KMOD_RSHIFT):
            # >
            if key == tcod.event.K_PERIOD:
                self.room_max_distance += 1
            # <
            elif key == tcod.event.K_COMMA:
                if self.room_max_distance > 10:
                    self.room_max_distance -= 1
            # +
            elif key == tcod.event.K_EQUALS:
                self.max_rooms += 1
            # -
            elif key == tcod.event.K_MINUS:
                self.max_rooms -= 1
            else:
                return

        elif key == tcod.event.K_ESCAPE:
            return self.parent
        elif key == tcod.event.K_1:
            self.map_func = self.generate_map
        elif key == tcod.event.K_2:
            self.map_func = self.generate_maze

        elif key == tcod.event.K_UP:
            self.room_max_size += 1
        elif key == tcod.event.K_DOWN:
            if self.room_max_size > self.room_min_size:
                self.room_max_size -= 1
        elif key == tcod.event.K_RIGHT:
            if self.room_min_size < self.room_max_size:
                self.room_min_size += 1
        elif key == tcod.event.K_LEFT:
            if self.room_min_size > 3:
                self.room_min_size -= 1

        elif key == tcod.event.K_LEFTBRACKET:
            if self.maze_path_width > 1:
                self.maze_path_width -= 1
        elif key == tcod.event.K_RIGHTBRACKET:
            self.maze_path_width += 1

        self.map = self.map_func()