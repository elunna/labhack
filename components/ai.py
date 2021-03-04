from components.component import Component
from actions.wait_action import WaitAction
from actions.movement_action import MovementAction
from actions.attack_actions import MeleeAttack
from actions.bump_action import BumpAction
from src import settings
import numpy as np  # type: ignore
import random
import tcod


class BaseAI(Component):
    def yield_action(self):
        # No perform implemented, since the entities which will be using AI to
        # act will have to have an AI class that inherits from this one.
        raise NotImplementedError()

    def get_path_to(self, dest_x, dest_y):
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
        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph)

        pathfinder.add_root((self.parent.x, self.parent.y))  # Start position.

        # Compute the path to the destination and remove the starting point.
        path = pathfinder.path_to((dest_x, dest_y))[1:].tolist()

        # Convert from List[List[int]] to List[Tuple[int, int]].
        return [(index[0], index[1]) for index in path]


class HostileAI(BaseAI):
    def __init__(self):
        self.path = []

    def yield_action(self):
        target = self.engine.player
        dx = target.x - self.parent.x
        dy = target.y - self.parent.y
        distance = max(abs(dx), abs(dy))  # Chebyshev distance.

        if self.engine.game_map.visible[self.parent.x, self.parent.y]:
            # If the player is right next to the entity, attack the player.
            if distance <= 1:
                return MeleeAttack(self.parent, dx, dy)

            self.path = self.get_path_to(target.x, target.y)

        if self.path:
            # If the player can see the entity, but the entity is too far away
            # to attack, then move towards the player.
            dest_x, dest_y = self.path.pop(0)
            return MovementAction(
                self.parent, dest_x - self.parent.x, dest_y - self.parent.y,
            )

        # If the entity is not in the player’s vision, simply wait.
        return WaitAction(self.parent)


class ConfusedAI(BaseAI):
    """ A confused enemy will stumble around aimlessly for a given number of turns, then
        revert back to its previous AI. If an actor occupies a tile it is randomly moving
        into, it will attack.
    """
    def __init__(self, previous_ai, turns_remaining):
        self.previous_ai = previous_ai
        self.turns_remaining = turns_remaining

    def yield_action(self):
        # causes the entity to move in a randomly selected direction.
        # Revert the AI back to the original state if the effect has run its course.
        # Pick a random direction
        direction_x, direction_y = random.choice(settings.DIRECTIONS)

        self.turns_remaining -= 1

        # The actor will either try to move or attack in the chosen random direction.
        # Its possible the actor will just bump into the wall, wasting a turn.
        action = BumpAction(self.parent, direction_x, direction_y)

        if self.turns_remaining <= 0:
            # If it's the last turn, we'll notify the player and return the
            # AI to the previous one.
            action.msg = f"The {self.parent.name} is no longer confused."
            self.parent.ai = self.previous_ai

        return action


class RunAI(BaseAI):
    def __init__(self, direction):
        self.dx, self.dy = direction
        self.first_step = True
        self.next_move = None

    def can_perform(self):
        target_tile = (self.parent.x + self.dx, self.parent.y + self.dy)

        # Do not run into a wall (or unwalkable tile)
        if not self.parent.gamemap.walkable(*target_tile):
            return False

        # Do not run into another actor
        if self.parent.gamemap.get_actor_at(*target_tile):
            return False

        # Do no run along-side another actor

        # Stop at something interesting: items on floor, dungeon feature, etc.

        # Stop at cooridor ends, doors

        return True

    def yield_action(self):
        return MovementAction(
            entity=self.parent,
            dx=self.parent.x + self.dx,
            dy=self.parent.y + self.dy
        )


class ParalyzedAI(BaseAI):
    """ A paralyzed enemy is motionless and unable to act for x turns,
    then reverts back to its previous AI.
    """
    def __init__(self, previous_ai, turns_remaining):
        self.previous_ai = previous_ai
        self.turns_remaining = turns_remaining

    def yield_action(self):
        self.turns_remaining -= 1
        action = WaitAction(self.parent)

        if self.turns_remaining <= 0:
            # If it's the last turn, we'll notify the player and return the AI to the previous one.
            action.msg = f"The {self.parent.name} regains control."
            self.parent.ai = self.previous_ai

        return action
