from . import color, logger
from . import dungeon
from . import exceptions
from . import gamemap
from . import messages
from actions import actions
from actions.wait_action import WaitAction
import lzma
import pickle
import random
import tcod

log = logger.setup_logger(__name__)


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

    def enemy_turns(self):
        """Goes through each actor in the current gamemap (excluding the player) and
        processes the actions provided by their AI.
        """
        actors = set(self.game_map.actors) - {self.player}
        for actor in actors:
            self.handle_actor_turn(actor)

    def handle_actor_turn(self, actor):
        """Processes a single actor's turn and gets their action from their AI."""
        while not actor.energy.burned_out() and actor.is_alive:
            actor.energy.burn_turn()

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
        """All actors gets an energy reboost!"""
        for entity in self.game_map.actors:
            entity.energy.add_energy()

    def update_fov(self):
        """Recompute the visible area based on the players point of view."""
        transparent_tiles = self.game_map.tiles["transparent"].copy()

        # Account for any entities that block vision
        blocking_entities = [e for e in self.game_map.entities if e.transparent is False]

        for e in blocking_entities:
            transparent_tiles[e.x, e.y] = False

        lit_tiles = self.game_map.lit.copy()

        # Set the lit tiles immediately around the player.
        radius = 3
        for x in range(radius):
            for y in range(radius):
                dx = -1 + x
                dy = -1 + y
                lit_tiles[self.player.x + dx, self.player.y + dy] = True

        # Set the game_map’s visible tiles to the result of the compute_fov.
        # radius is the maximum view distance from pov. If this is zero then the maximum distance is used.
        # If light_walls is True then visible obstacles will be returned, otherwise only transparent areas
        # will be.
        # algorithm is the field-of-view algorithm to run. The default value is tcod.FOV_RESTRICTIVE.
        # The options are:
        # tcod.FOV_BASIC: Simple ray-cast implementation.
        # tcod.FOV_DIAMOND
        # tcod.FOV_SHADOW: Recursive shadow caster.
        # tcod.FOV_PERMISSIVE(n): n starts at 0 (most restrictive) and goes up to 8 (most permissive.)
        # tcod.FOV_RESTRICTIVE
        # tcod.FOV_SYMMETRIC_SHADOWCAST
        self.game_map.visible[:] = tcod.map.compute_fov(
            transparency=transparent_tiles,
            pov=(self.player.x, self.player.y),
            # radius=settings.fov_radius,
            radius=15,
            light_walls=True,
            algorithm=tcod.FOV_RESTRICTIVE,
        )

        # Remove hidden blockers from visible
        for e in blocking_entities:
            if "hidden" in e:
                self.game_map.visible[e.x, e.y] = False

        # If a tile is not "lit", it should be removed from visible.
        self.game_map.visible &= lit_tiles

        # If a tile is "visible" it should be added to "explored".
        self.game_map.explored |= self.game_map.visible

    def render(self, renderer):
        """ Render the current GameMap and it's entities to the screen."""
        renderer.render_all(self)

    def save_as(self, filename):
        """Save this Engine instance as a compressed file."""
        # pickle serializes an object hierarchy in Python.
        # lzma compresses the data

        save_data = lzma.compress(pickle.dumps(self))

        with open(filename, "wb") as f:
            f.write(save_data)

    def check_level(self):
        """Checks the status of the player's experience to see if they qualify for an upgrade."""
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
        """ Handles an action from the game and processes all of the results.
        :param action: A type or subclass of Action.
        :return: True if all of the actions and following actions were processed successfuly, False if not.
        """
        if action is None:
            return False

        action_queue = [action]

        while action_queue:
            try:
                current_action = action_queue[0]
                result = current_action.perform()

                if action.entity.name == "player":
                    # Just log the player's actions

                    log.debug(f'Engine: handling {current_action}')
                    log.debug(f'\tresult: {result}')

            except exceptions.Impossible as exc:
                log.debug(f'\tImpossible: {exc}')
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
        """ Creates a random monster in a random valid location on the current map. """
        # 1 out of 70 chance of creating a monster
        CHANCE = 70
        if random.randint(1, CHANCE) == 1:
            self.dungeon.summon_random_monster(self.player.level.current_level)

    def reduce_timeouts(self):
        """ Go through all off the states that each actor has and reduce the timeout by 1."""
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

    def end_of_turn(self):
        # All actors get an energy recharge every turn
        self.add_energy()

        # Once player turn is complete, run the monsters turns.
        self.enemy_turns()

        # If the player leveled up, handle it.
        self.check_level()

        # Random chance at summoning new dungeon monster.
        self.generate_monster()

        # Handle end-of-turn states ..Decrease timeouts on states
        self.reduce_timeouts()

        # Check if player regenerates
        self.player.regeneration.activate(self.turns)



        # Increment turns
        self.turns += 1

