from actions import actions
from . import color
from . import exceptions
from . import gamemap
from . import gameworld
from . import msglog
from . import rendering
from . import settings
from tcod.map import compute_fov
import lzma
import pickle
import tcod


class Engine:
    """ The driver of the game, manages the entities, events, and player and
        makes sure that the screen is correctly updated.
    """
    game_map: gamemap.GameMap
    game_world: gameworld.GameWorld

    def __init__(self, player):
        # TODO: Remove requirement for player
        self.msglog = msglog.MsgLog()
        self.helplog = msglog.HelpInfo()
        self.mouse_location = (0, 0)
        self.player = player
        self.renderer = None
        self.turns = 0

    def handle_enemy_turns(self):
        for actor in set(self.game_map.actors) - {self.player}:
            if actor.ai:
                while not actor.energymeter.burned_out():
                    # We'll use the energy regardless.
                    actor.energymeter.burn_turn()

                    try:
                        # Get the next calculated action from the AI.
                        self.handle_action(actor.ai.perform())
                    except exceptions.Impossible:
                        pass  # Ignore impossible action exceptions from AI

    def add_energy(self):
        # All actors gets an energy reboost!
        for entity in set(self.game_map.actors):
            entity.energymeter.add_energy(settings.energy_per_turn)

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

    def render(self, renderer):
        # Message Panel
        rendering.render_messages(
            console=renderer.msg_panel,
            x=settings.msg_panel_x, y=0,
            width=settings.screen_width,
            height=settings.msg_panel_height,
            messages=self.msglog.messages,
        )

        # Map Panel
        rendering.render_map(renderer.map_panel, self.game_map)

        # Stat Panel
        rendering.render_names_at_mouse_location(
            console=renderer.stat_panel,
            x=settings.tooltip_x,
            y=settings.tooltip_y,
            engine=self
        )

        rendering.render_stats(
            console=renderer.stat_panel,
            engine=self,
            player=self.player
        )

        rendering.render_bar(
            console=renderer.stat_panel,
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=settings.hp_bar_width,
        )

        rendering.render_dungeon_lvl_text(
            console=renderer.stat_panel,
            dungeon_level=self.game_world.current_floor,
        )

        renderer.msg_panel.blit(renderer.root, 0, settings.msg_panel_y)
        renderer.map_panel.blit(renderer.root, 0, settings.map_panel_y)
        renderer.stat_panel.blit(renderer.root, 0, settings.stat_panel_y)

        renderer.msg_panel.clear()
        renderer.stat_panel.clear()

    def save_as(self, filename):
        """Save this Engine instance as a compressed file."""
        # pickle serializes an object hierarchy in Python.
        # lzma compresses the data

        save_data = lzma.compress(pickle.dumps(self))

        with open(filename, "wb") as f:
            f.write(save_data)

    # def bring_out_the_dead(self):
        # for entity in set(self.game_map.actors):
            # if entity.ai and entity.fighter.is_dead():
                # pass


    def handle_action(self, action):
        if action is None:
            return False

        action_queue = [action]

        while action_queue:
            try:
                current_action = action_queue[0]
                result = current_action.perform()
            except exceptions.Impossible as exc:
                self.msglog.add_message(exc.args[0], color.impossible)
                return False  # Skip enemy turn on exceptions

            # Display any messages from the current action's result
            if current_action.msg:
                self.msglog.add_message(current_action.msg)

            # Current action has been handled
            action_queue.pop(0)

            # Process results
            if isinstance(result, actions.Action):
                action_queue.append(result)
            elif isinstance(result, list):
                action_queue.extend(result)

        return True
