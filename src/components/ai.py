from src.actions import Action, BumpAction, MeleeAction, MovementAction, WaitAction
from src import settings
import numpy as np  # type: ignore
import random
import tcod


class BaseAI(Action):
    entity = None

    def perform(self):
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
        cost = np.array(self.entity.gamemap.tiles["walkable"], dtype=np.int8)

        for entity in self.entity.gamemap.entities:
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

        pathfinder.add_root((self.entity.x, self.entity.y))  # Start position.

        # Compute the path to the destination and remove the starting point.
        path = pathfinder.path_to((dest_x, dest_y))[1:].tolist()

        # Convert from List[List[int]] to List[Tuple[int, int]].
        return [(index[0], index[1]) for index in path]


class HeroControllerAI(BaseAI):
    def __init__(self, entity):
        super().__init__(entity)
        self.path = []

    def perform(self):
        # TODO: Put human controlling code here.
        pass


class StationaryAI(BaseAI):
    def __init__(self, entity):
        super().__init__(entity)
        self.path = []

    def perform(self):
        # Stationary monsters just sit there waiting.
        return WaitAction(self.entity)



class HostileEnemy(BaseAI):
    def __init__(self, entity):
        super().__init__(entity)
        self.path = []

    def perform(self):
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))  # Chebyshev distance.

        if self.engine.game_map.visible[self.entity.x, self.entity.y]:
            # If the player is right next to the entity, attack the player.
            if distance <= 1:
                return MeleeAction(self.entity, dx, dy)

            self.path = self.get_path_to(target.x, target.y)

        if self.path:
            # If the player can see the entity, but the entity is too far away
            # to attack, then move towards the player.
            dest_x, dest_y = self.path.pop(0)

            return MovementAction(
                self.entity, dest_x - self.entity.x, dest_y - self.entity.y,
            )

        # If the entity is not in the player’s vision, simply wait.
        return WaitAction(self.entity)


class ConfusedEnemy(BaseAI):
    """ A confused enemy will stumble around aimlessly for a given number of turns, then
        revert back to its previous AI. If an actor occupies a tile it is randomly moving
        into, it will attack.
    """

    def __init__(self, entity, previous_ai, turns_remaining):
        super().__init__(entity)

        self.previous_ai = previous_ai
        self.turns_remaining = turns_remaining

    def perform(self):
        # causes the entity to move in a randomly selected direction.
        # Revert the AI back to the original state if the effect has run its course.
        if self.turns_remaining <= 0:
            self.engine.message_log.add_message(
                f"The {self.entity.name} is no longer confused."
            )
            self.entity.ai = self.previous_ai
        else:
            # Pick a random direction
            direction_x, direction_y = random.choice(settings.DIRECTIONS)

            self.turns_remaining -= 1

            # The actor will either try to move or attack in the chosen random direction.
            # Its possible the actor will just bump into the wall, wasting a turn.
            return BumpAction(self.entity, direction_x, direction_y)



class ParalyzedAI(BaseAI):
    """ A confused enemy will stumble around aimlessly for a given number of turns, then
        revert back to its previous AI. If an actor occupies a tile it is randomly moving
        into, it will attack.
    """

    def __init__(self, entity, previous_ai, turns_remaining):
        super().__init__(entity)

        self.previous_ai = previous_ai
        self.turns_remaining = turns_remaining

    def perform(self):
        # Causes the entity to stay frozen in place
        # Revert the AI back to the original state if the effect has run its course.
        if self.turns_remaining <= 0:
            self.engine.message_log.add_message(
                f"You are no longer paralyzed."
            )
            self.entity.ai = self.previous_ai
        else:
            self.engine.message_log.add_message(
                f"You are frozen in place, helpless...."
            )
            # We can just use the wait action to simulate paralysis
            self.turns_remaining -= 1
            return WaitAction(self.entity)
