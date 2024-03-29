from components.component import Component
from actions.wait_action import WaitAction
from actions.movement_action import MovementAction
from actions.bump_action import BumpAction
from src import settings, tiles
import numpy as np
import tcod


class BaseAI(Component):
    """Contains the base functionality for actor AI's. """
    def yield_action(self):
        """No perform implemented, since the entities which will be using AI to
        act will have to have an AI class that inherits from this one.
        """
        raise NotImplementedError()

    def get_path_to(self, dest_x, dest_y, diagonal=3):
        """ Compute and return a path to the target position.
            If there is no valid path then returns an empty list.

            Uses the "walkable" tiles in our map.

            get_path_to uses the “walkable” tiles in our map, along with some
            TCOD pathfinding tools to get the path from the BaseAI’s parent entity
            to whatever their target might be. In the case of this tutorial, the
            target will always be the player, though you could theoretically write
            a monster that cares more about food or treasure than attacking the player.

            The pathfinder first builds an array of cost, which is how “costly”
            (time consuming) it will take to get to the target. If a piece of
            terrain takes longer to traverse, its cost will be higher. In the
            case of our simple game, all parts of the map have the same cost, but
            what this cost array allows us to do is take other entities into account.

            How? Well, if an entity exists at a spot on the map, we increase the
            cost of moving there to “10”. What this does is encourages the entity
            to move around the entity that’s blocking them from their target. Higher
            values will cause the entity to take a longer path around; shorter values
            will cause groups to gather into crowds, since they don’t want to move around.

            More information about TCOD’s pathfinding can be found here.
            https://python-tcod.readthedocs.io/en/latest/tcod/path.html

            If diagonal is 3, the actor will use diagonal movement.
            If diagonal is 0, the actor will only use cardinal directions.

        """
        # Copy the walkable array.
        cost = np.array(self.parent.gamemap.tiles["walkable"], dtype=np.int8)

        for entity in self.parent.gamemap.entities:
            # Check that an enitiy blocks movement and the cost isn't zero (blocking.)
            if entity.blocks_movement and cost[entity.x, entity.y]:
                # Add to the cost of a blocked position.
                # A lower number means more enemies will crowd behind each other in
                # hallways.  A higher number means enemies will take longer paths in
                # order to surround the player.
                cost[entity.x, entity.y] += 10

        # Create a graph from the cost array and pass that graph to a new pathfinder.
        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=diagonal)
        pathfinder = tcod.path.Pathfinder(graph)

        pathfinder.add_root((self.parent.x, self.parent.y))  # Start position.

        # Compute the path to the destination and remove the starting point.
        path = pathfinder.path_to((dest_x, dest_y))[1:].tolist()

        # Convert from List[List[int]] to List[Tuple[int, int]].
        return [(index[0], index[1]) for index in path]


class HostileAI(BaseAI):
    """ Makes monsters aggressively seek out and attack the player. Monsters will only chase
    if they are within the chase_distance. They will attack if next to the player.
    """
    def __init__(self, diagonal=3):
        self.path = []
        self.diagonal = diagonal
        self.chase_distance = 12

    def yield_action(self):
        """Determines if the monster should move closer, attack, or wait."""
        target = self.engine.player
        dx = target.x - self.parent.x
        dy = target.y - self.parent.y
        if self.can_attack(target, dx, dy):
            return BumpAction(self.parent, dx, dy)

        self.path = self.get_path_to(target.x, target.y, self.diagonal)

        # Only chase the player if we're under a chase distance threshold.
        if self.path and len(self.path) < self.chase_distance:
            # Move towards the player.
            dest_x, dest_y = self.path.pop(0)
            return MovementAction(
                self.parent, dest_x - self.parent.x, dest_y - self.parent.y,
            )

        # If the entity is not in the player’s vision, simply wait.
        return WaitAction(self.parent)

    def can_attack(self, target, dx, dy):
        """Returns True if the monster is able to attack, otherwise False."""
        distance = max(abs(dx), abs(dy))  # Chebyshev distance.
        if self.engine.game_map.visible[self.parent.x, self.parent.y]:
            # If the player is right next to the entity, attack the player.
            return distance <= 1
        return False

    # def can_chase(self):


class GridAI(HostileAI):
    """Like HostileAI, but monsters with this AI can only move and attack in cardinal directions: N, E, S, W.
    """
    def __init__(self):
        # This just creates a hostile AI with a diagonal of 0 so the actor will only use
        super().__init__(diagonal=0)

    def can_attack(self, target, dx, dy):
        """Returns True if the monster is next to the player and directly N, E, S, or W."""
        distance = max(abs(dx), abs(dy))  # Chebyshev distance.
        if distance > 1:
           return False
        return  (dx, dy) in settings.CARDINAL_DIR.values()


class RunAI(BaseAI):
    """ This is an AI for the player to auto-run in a direction until we run into an obstacle or something
    interesting.
    """
    def __init__(self, direction):
        self.dx, self.dy = direction
        self.first_step = True
        self.stop_after_first_stop = False

    def can_perform(self):
        """Returns True if the player can move in the """
        target_tile = (self.parent.x + self.dx, self.parent.y + self.dy)
        result = True
        actor_in_way = self.parent.gamemap.get_actor_at(*target_tile)

        # Do not run into a wall (or unwalkable tile)
        if not self.parent.gamemap.walkable(*target_tile):
            result = False

        elif self.first_step:
            if actor_in_way:
                # For the first step, we want enable attacking - but then stop after that.
                self.stop_after_first_stop = True
            return True

        elif self.stop_after_first_stop:
            result = False

        # Do not run into another actor
        elif actor_in_way:
            result = False

        # Do not run along-side another actor

        # Stop at traps
        elif self.parent.gamemap.get_trap_at(self.parent.x, self.parent.y):
            result = False

        # Stop at doors, stairs
        elif self.parent.gamemap.tiles[self.parent.x, self.parent.y] \
                in [tiles.door, tiles.down_stairs, tiles.up_stairs]:
            result = False

        # Stop at any entities
        elif self.parent.gamemap.filter(x=self.parent.x, y=self.parent.y) - {self.parent}:
            result = False

        # Stop at cooridor ends?

        return result

    def yield_action(self):
        """Returns a BumpAction if it's the first step.
        For all other steps we return a MovementAction.
        """
        if self.first_step:
            self.first_step = False

            return BumpAction(
                entity=self.parent,
                dx=self.dx,
                dy=self.dy
            )

        return MovementAction(
            entity=self.parent,
            dx=self.dx,
            dy=self.dy
        )


class TravelAI(BaseAI):
    """ This is an AI for the player to auto-walk to a destination tile until we run into an obstacle
    or encounter something interesting.
    """
    def __init__(self, entity, x, y):
        self.parent = entity
        self.path = self.get_path_to(x, y, 3)
        # self.first_step = True

    def can_perform(self):
        if self.path:
            return True
        return False

    def yield_action(self):
        # Move towards the target.
        dest_x, dest_y = self.path.pop(0)

        return MovementAction(
            self.parent,
            dest_x - self.parent.x,
            dest_y - self.parent.y,
        )


class RestAI(BaseAI):
    """ This is an AI for the player to rest in place until HP is fully restored or something interesting
    happens near us.
    """
    def __init__(self):
        self.first_turn = True

    def can_perform(self):
        """Returns True if the player can safely rest. """
        if self.first_turn:
            return True

        gamemap = self.parent.gamemap
        x, y = self.parent.x, self.parent.y

        radius = 1.5  # Try to get actors within 1 square.
        # Is there an enemy next to us?

        close_actors = gamemap.get_entities_within(x, y, radius) - {self.parent}
        if close_actors:
            return False

        # Is our HP full?
        if self.parent.fighter.hp_full():
            return False
        return True

    def yield_action(self):
        """Returns a WaitAction. """
        self.first_turn = False
        return WaitAction(self.parent)
