from . import exceptions
from . import render_functions
from . import settings
from .entity_factories import corpse_generator
from .game_map import GameMap
from .game_world import GameWorld
from .message_log import MessageLog
from tcod.map import compute_fov
import lzma
import pickle
import tcod


class Engine:
    """ The driver of the game, manages the entities, events, and player and
        makes sure that the screen is correctly updated.
    """
    game_map: GameMap
    game_world: GameWorld

    def __init__(self, player):
        self.message_log = MessageLog()
        self.mouse_location = (0, 0)
        self.player = player

        # Define separate panels for the map, messages, and stats.
        self.msg_panel = tcod.Console(
            width=settings.screen_width,
            height=settings.msg_panel_height
        )
        self.map_panel = tcod.Console(
            width=settings.map_width,
            height=settings.map_height,
            order="F",
        )
        self.stat_panel = tcod.Console(
            width=settings.screen_width,
            height=settings.stat_panel_height
        )

    def handle_enemy_turns(self):
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                # Get the next calculated action from the AI.
                action = entity.ai.perform()
                try:
                    # Execute the action
                    action.perform()
                    # entity.ai.perform()
                except exceptions.Impossible:
                    pass # Ignore impossible action exceptions from AI
                except AttributeError:
                    pass


        # Convert any dead monsters to corpse items
        for actor in set(self.game_map.actors) - {self.player}:
            if not actor.is_alive:
                # Replace the actor with an item that is a corpse
                corpse = corpse_generator(actor)

                # Remove the dead actor from the map
                self.game_map.entities.remove(actor)

                # Replace it with the corpse item
                self.game_map.entities.add(corpse)


    def update_fov(self):
        """Recompute the visible area based on the players point of view."""

        # Set the game_map’s visible tiles to the result of the compute_fov.
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=settings.fov_radius,
        )

        # If a tile is "visible" it should be added to "explored".
        self.game_map.explored |= self.game_map.visible

    def render(self, console):
        # Message Panel
        render_functions.render_messages(
            console=self.msg_panel,
            x=settings.msg_panel_x, y=0,
            width=settings.screen_width,
            height=settings.msg_panel_height,
            messages=self.message_log.messages,
        )

        # Map Panel
        render_functions.render_map(self.map_panel, self.game_map)

        # Stat Panel
        render_functions.render_names_at_mouse_location(
            console=self.stat_panel,
            x=settings.tooltip_x,
            y=settings.tooltip_y,
            engine=self
        )

        render_functions.render_bar(
            console=self.stat_panel,
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=settings.hp_bar_width,
        )

        render_functions.render_dungeon_lvl_text(
            console=self.stat_panel,
            dungeon_level=self.game_world.current_floor,
        )

        self.msg_panel.blit(console, 0, settings.msg_panel_y)
        self.map_panel.blit(console, 0, settings.map_panel_y)
        self.stat_panel.blit(console, 0, settings.stat_panel_y)

        self.msg_panel.clear()
        self.stat_panel.clear()

        # blit(dest: tcod.console.Console,
        #    dest_x: int = 0, dest_y: int = 0,
        #    src_x: int = 0, src_y: int = 0,
        #    width: int = 0, height: int = 0,
        #    fg_alpha: float = 1.0, bg_alpha: float = 1.0,
        #    key_color: Optional[Tuple[int, int, int]] = None) → None



    def save_as(self, filename):
        """Save this Engine instance as a compressed file."""
        # pickle serializes an object hierarchy in Python.
        # lzma compresses the data

        save_data = lzma.compress(pickle.dumps(self))

        with open(filename, "wb") as f:
            f.write(save_data)
