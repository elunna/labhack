from components.component import Component
from actions.wait_action import WaitAction
from actions.movement_action import MovementAction
from actions.attack_actions import MeleeAttack
from actions.bump_action import BumpAction
from src import settings, tiles
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
                return BumpAction(self.parent, dx, dy)

            self.path = self.get_path_to(target.x, target.y)

        if self.path:
            # If the player can see the entity, but the entity is too far away
            # to attack, then move towards the player.
            dest_x, dest_y = self.path.pop(0)
            return BumpAction(
                self.parent, dest_x - self.parent.x, dest_y - self.parent.y,
            )

        # If the entity is not in the player’s vision, simply wait.
        return WaitAction(self.parent)


class RunAI(BaseAI):
    def __init__(self, direction):
        self.dx, self.dy = direction
        self.first_step = True

    def can_perform(self):
        target_tile = (self.parent.x + self.dx, self.parent.y + self.dy)
        result = True
        if self.first_step:
            return True

        # Stop at any entities
        if self.parent.gamemap.filter(x=self.parent.x, y=self.parent.y) - {self.parent}:
            result = False

        # Do not run into a wall (or unwalkable tile)
        elif not self.parent.gamemap.walkable(*target_tile):
            result = False

        # Do not run into another actor
        elif self.parent.gamemap.get_actor_at(*target_tile):
            result = False

        # Do not run along-side another actor

        # Stop at traps
        elif self.parent.gamemap.get_trap_at(self.parent.x, self.parent.y):
            result = False

        # Stop at doors, stairs
        elif self.parent.gamemap.tiles[self.parent.x, self.parent.y] \
                in [tiles.door, tiles.down_stairs, tiles.up_stairs]:
            result = False

        # Stop at cooridor ends?

        if result is False:
            self.parent.ai = None

        return result

    def yield_action(self):
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
