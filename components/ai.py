import actions
import settings
import numpy as np  # type: ignore
import random
import tcod

class BaseAI:
    def __init__(self, entity):
        self.entity = entity

    @property
    def engine(self):
        """Return the engine this action belongs to."""
        return self.entity.gamemap.engine

    def yield_action(self):
        """ Generate an action with the objects needed to determine its scope.
            `self.engine` is the scope this action is being performed in.
            `self.entity` is the object performing the action.

            This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()

    def get_path_to(self, dest_x, dest_y, grid_movement=False):
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
        if grid_movement:
            diagonal = 0
        else:
            diagonal = 3

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
        # greed is used to define the heuristic. To get the fastest accurate heuristic
        # greed should be the lowest non-zero value on the cost array. Higher values
        # may be used for an inaccurate but faster heuristic.
        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=diagonal)

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

    def yield_action(self):
        # TODO: Put human controlling code here.
        pass


class StationaryAI(BaseAI):
    def __init__(self, entity):
        super().__init__(entity)
        self.path = []

    def yield_action(self):
        # Stationary monsters just sit there waiting.
        return actions.WaitAction(self.entity)


class ApproachAI(BaseAI):
    def __init__(self, entity):
        super().__init__(entity)
        self.path = []

    def yield_action(self):
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))  # Chebyshev distance.

        if self.engine.game_map.visible[self.entity.x, self.entity.y]:
            # If the player is right next to the entity, attack the player.
            if distance <= 1:
                return actions.MeleeAction(self.entity, dx, dy)

            self.path = self.get_path_to(target.x, target.y)

        if self.path:
            # If the player can see the entity, but the entity is too far away
            # to attack, then move towards the player.
            dest_x, dest_y = self.path.pop(0)

            return actions.MovementAction(
                self.entity, dest_x - self.entity.x, dest_y - self.entity.y,
            )

        # If the entity is not in the player’s vision, simply wait.
        # This keeps burning up enemy energy so they don't have a ton of moves
        # built up before we see them.
        return actions.WaitAction(self.entity)


class GridMoveAI(ApproachAI):
    """ The Grid Bug can only (and attack) in the 4 cardinal directions:
        N E S W.
    """
    def __init__(self, entity):
        super().__init__(entity)
        self.path = []

    def yield_action(self):
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))  # Chebyshev distance.

        if self.engine.game_map.visible[self.entity.x, self.entity.y]:
            # Only attack in "grid" directions: N/W/S/E of the entity
            if distance <= 1 and (dx, dy) in settings.CARDINAL_DIRECTIONS:
                return actions.MeleeAction(self.entity, dx, dy)

            self.path = self.get_path_to(target.x, target.y, grid_movement=True)

        if self.path:
            # Move towards the player.
            dest_x, dest_y = self.path.pop(0)

            return actions.MovementAction(
                self.entity, dest_x - self.entity.x, dest_y - self.entity.y,
            )

        # Entity is not in the player’s vision, simply wait.
        return actions.WaitAction(self.entity)


class ConfusedAI(BaseAI):
    """ A confused enemy will stumble around aimlessly for a given number of turns, then
        revert back to its previous AI. If an actor occupies a tile it is randomly moving
        into, it will attack.
    """

    def __init__(self, entity, previous_ai, turns_remaining):
        super().__init__(entity)

        self.previous_ai = previous_ai
        self.turns_remaining = turns_remaining

    def yield_action(self):
        # causes the entity to move in a randomly selected direction.
        # Revert the AI back to the original state if the effect has run its course.
        if self.turns_remaining <= 0:
            if self.entity == self.engine.player:
                self.engine.msg_log.add_message(f"You are no longer confused.")
            else:
                self.engine.msg_log.add_message(f"The {self.entity} is no longer confused.")

            self.entity.ai = self.previous_ai
        else:
            # Pick a random direction
            direction_x, direction_y = random.choice(settings.DIRECTIONS)

            self.turns_remaining -= 1

            # The actor will either try to move or attack in the chosen random direction.
            # Its possible the actor will just bump into the wall, wasting a turn.
            return actions.BumpAction(self.entity, direction_x, direction_y)


class ParalyzedAI(BaseAI):
    """ A confused enemy will stumble around aimlessly for a given number of turns, then
        revert back to its previous AI. If an actor occupies a tile it is randomly moving
        into, it will attack.
    """

    def __init__(self, entity, previous_ai, turns_remaining):
        super().__init__(entity)

        self.previous_ai = previous_ai
        self.turns_remaining = turns_remaining

    def yield_action(self):
        # Causes the entity to stay frozen in place
        # Revert the AI back to the original state if the effect has run its course.
        if self.turns_remaining <= 0:
            self.engine.msg_log.add_message(f"You are no longer paralyzed.")
            self.entity.ai = self.previous_ai
        else:
            self.engine.msg_log.add_message(f"You are frozen in place, helpless....")
            # We can just use the wait action to simulate paralysis
            self.turns_remaining -= 1
            return actions.WaitAction(self.entity)
