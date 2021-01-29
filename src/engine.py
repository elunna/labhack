from src import exceptions
from src import settings
from src.entity_factories import corpse_generator
from src.game_map import GameMap
from src.game_world import GameWorld
from src.message_log import MessageLog
from tcod.map import compute_fov


class Engine:
    """ The driver of the game. Manages the entities, actors, events, and player
        and makes sure they are routed to the renderer..
    """
    game_map: GameMap
    game_world: GameWorld

    def __init__(self, player):
        self.message_log = MessageLog()
        self.mouse_location = (0, 0)
        self.player = player
        self.turns = 0

    def add_energy(self):
        # Everyone gets an energy reboost!
        # TODO: Maybe only entities within player's vision
        # if self.engine.game_map.visible[self.entity.x, self.entity.y]:

        for entity in set(self.game_map.actors):
            entity.energymeter.add_energy(settings.energy_per_turn)

    def handle_enemy_turns(self):
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                while not entity.energymeter.burned_out():
                    # Get the next calculated action from the AI.
                    action = entity.ai.perform()

                    # We'll use the energy regardless.
                    entity.energymeter.burn_turn()

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
