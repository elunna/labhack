from actions.wait_action import WaitAction
from . import color
from . import dungeon
from . import exceptions
from . import gamemap
from . import messages
from . import rendering
from . import settings
from actions import actions
# from tcod.map import compute_fov
import lzma
import pickle
import random
import tcod


class Engine:
    """ The driver of the game, manages the entities, events, and player and
        makes sure that the screen is correctly updated.
    """
    game_map: gamemap.GameMap

    def __init__(self, player):
        # TODO: Remove requirement for player
        self.msglog = messages.MsgLog()
        self.helplog = messages.HelpInfo()
        self.mouse_location = (0, 0)
        self.player = player
        self.renderer = None
        self.turns = 0
        self.dungeon = dungeon.Dungeon(engine=self)

    def handle_enemy_turns(self):
        actors = set(self.game_map.actors) - {self.player}
        for actor in actors:
            if actor.ai:
                while not actor.energymeter.burned_out() and actor.is_alive:
                    # We'll use the energy regardless.
                    actor.energymeter.burn_turn()

                    # Check for auto-states (like paralysis)
                    if actor.states.autopilot:
                        action = self.handle_auto_states(actor)
                    else:
                        action = actor.ai.yield_action()

                    try:
                        # Get the next calculated action from the AI.
                        self.handle_action(action)
                    except exceptions.Impossible:
                        pass  # Ignore impossible action exceptions from AI

    def add_energy(self):
        # All actors gets an energy reboost!
        for entity in self.game_map.actors:
            entity.energymeter.add_energy(settings.energy_per_turn)

    def update_fov(self):
        """Recompute the visible area based on the players point of view."""
        transparent_tiles = self.game_map.tiles["transparent"].copy()

        # Account for any entities that block vision
        blocking_entities = [e for e in self.game_map.entities if e.transparent is False]

        for e in blocking_entities:
            transparent_tiles[e.x, e.y] = False

        # Set the game_map’s visible tiles to the result of the compute_fov.
        self.game_map.visible[:] = tcod.map.compute_fov(
            transparent_tiles,
            (self.player.x, self.player.y),
            radius=settings.fov_radius,
        )
        # Remove hidden blockers from visible
        for e in blocking_entities:
            if "hidden" in e:
                self.game_map.visible[e.x, e.y] = False

        # If a tile is "visible" it should be added to "explored".
        self.game_map.explored |= self.game_map.visible

    def render(self, renderer):
        # Message Panel
        rendering.render_messages(
            console=renderer.msg_panel,
            x=settings.msg_panel_x, y=0,
            width=settings.screen_width,
            height=settings.msg_panel_height,
            msg_list=self.msglog.messages,
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
            dungeon_level=self.dungeon.dlevel,
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

    def check_level(self):
        # Player leveled up
        if self.player.level.requires_level_up:
            next_level = self.player.level.current_level + 1
            self.msglog.add_message(f"You advance to level {next_level}!", tcod.light_blue)

            # Instead, boost a random stat.
            choice = random.randint(1, 3)
            if choice == 1:
                self.player.level.increase_max_hp()
                self.msglog.add_message("Your health improves!")
            elif choice == 2:
                self.player.level.increase_strength()
                self.msglog.add_message("You feel stronger!")
            else:
                self.player.level.increase_ac()
                self.msglog.add_message("Your movements are getting swifter!")

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

            # Some actions, like searching, will need to update the display
            # if current_action.recompute_fov:
            #     self.update_fov()
                # self.render(self.renderer)

            # Current action has been handled
            action_queue.pop(0)

            # Process results
            if isinstance(result, actions.Action):
                action_queue.append(result)
            elif isinstance(result, list):
                action_queue.extend(result)

        return True

    def generate_monster(self):
        # 1 out of 70 chance of creating a monster
        CHANCE = 70
        if random.randint(1, CHANCE) == 1:
            self.dungeon.summon_random_monster(self.player.level.current_level)

    def reduce_timeouts(self):
        for actor in self.game_map.actors:
            # Decrease all the timeouts for states in each actor
            for state in actor.states.decrease():
                if actor.name == "player":
                    self.msglog.add_message(f"You feel less {state}")
                else:
                    self.msglog.add_message(f"The {actor.name} is less {state}")

    def handle_auto_states(self, actor):
        """ This handles things that "take over" an actors turn, like paralysis or sleep.
        """
        # For now just use WaitAction
        return WaitAction(actor)
