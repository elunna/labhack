import random

import src.utils
from actions.die_action import DieAction
from actions.item_action import ItemAction
from components.component import Component
from components.inventory import Inventory
from src import color, quotes
from src import exceptions
from src import handlers


class Consumable(Component):
    def get_action(self, consumer):
        """Try to return the action for this item."""
        return ItemAction(consumer, self.parent)

    def activate(self, action):
        """Invoke this items ability.
            Return the results as an Action or list of Actions
            `action` is the context for this activation.
        """
        raise NotImplementedError()

    def consume(self):
        """Remove the consumed item from its containing inventory."""

        entity = self.parent
        inventory = entity.parent

        if isinstance(inventory, Inventory):
            # inventory.items.remove(entity)
            inventory.rm_inv_item(entity, 1)


class HealConsumable(Consumable):
    """ Heals x + 1dx, where x is the amount this object is initialized with. """
    def __init__(self, amount):
        self.amount = amount

    def activate(self, action):
        consumer = action.entity
        healing_amount = self.amount + random.randint(1, self.amount)
        amount_recovered = consumer.fighter.heal(healing_amount)

        if amount_recovered > 0:
            action.msg = f"You consume the {self.parent.name}, and recover {amount_recovered} HP!"
            self.consume()
        else:
            raise exceptions.Impossible(f"Your health is already full.")


class PoisonConsumable(Consumable):
    """ Deals x + 1dx, where x is the amount this object is initialized with. """
    def __init__(self, amount):
        self.amount = amount

    def activate(self, action):
        consumer = action.entity
        damage = self.amount + random.randint(1, self.amount)

        action.msg = f"You consume the {self.parent.name}, and take {damage} damage!"
        consumer.fighter.hp -= damage

        if consumer.fighter.is_dead():
            return DieAction(entity=consumer, cause=self.parent)


class LightningDamageConsumable(Consumable):
    def __init__(self, damage, maximum_range):
        self.damage = damage  # How much damage the lightning will deal.
        self.maximum_range = maximum_range  # How far the lightning can strike.

    def activate(self, action):
        consumer = action.entity
        target = None
        closest_distance = self.maximum_range + 1.0

        for actor in self.engine.game_map.actors:
            if actor is not consumer and self.parent.gamemap.visible[actor.x, actor.y]:
                distance = src.utils.distance(consumer.x, consumer.y, actor.x, actor.y)

                if distance < closest_distance:
                    target = actor
                    closest_distance = distance

        if target:
            action.msg = f"A lighting bolt zaps the {target.name} with a roaring crack!! "
            target.fighter.hp -= self.damage
            self.consume()
        else:
            raise exceptions.Impossible("No enemy is close enough to strike.")

        if target.fighter.is_dead():
            return DieAction(entity=target, cause=consumer)


class TargetedConfusionConsumable(Consumable):
    def __init__(self, number_of_turns):
        self.number_of_turns = number_of_turns

    def get_action(self, consumer):
        self.engine.msglog.add_message(
            "Select a target location.", color.needs_target
        )
        return handlers.SingleRangedAttackHandler(
            self.engine,
            # “xy” will be the coordinates of the target. The lambda function
            # executes ItemAction, which receives the consumer, the parent (the
            # item), and the “xy” coordinates.
            callback=lambda xy: ItemAction(consumer, self.parent, xy),
        )

    def activate(self, action):
        consumer = action.entity
        # Get the actor at the location
        target = action.target_actor

        if not self.engine.game_map.visible[action.target_xy]:
            raise exceptions.Impossible("You cannot target an area that you cannot see.")
        if not target:
            raise exceptions.Impossible("You must select an enemy to target.")
        if target is consumer:
            raise exceptions.Impossible("You cannot confuse yourself!")

        action.msg = f"The eyes of the {target.name} look vacant, as it starts to stumble around!"

        target.states.add_state("confused", self.number_of_turns)
        self.consume()


class FireballDamageConsumable(Consumable):
    def __init__(self, damage, radius):
        self.damage = damage
        self.radius = radius

    def get_action(self, consumer):
        # asks the user to select a target, and switches the event handler
        self.engine.msglog.add_message(
            "Select a target location.", color.needs_target
        )
        return handlers.AreaRangedAttackHandler(
            self.engine,
            radius=self.radius,
            callback=lambda xy: ItemAction(consumer, self.parent, xy),
        )

    def activate(self, action):
        """ gets the target location, and ensures that it is within the line of
            sight. It then checks for entities within the radius, damaging any
            that are close enough to hit (take note, there’s no exception for
            the player, so you can get blasted by your own fireball!). If no
            enemies were hit at all, the Impossible exception is raised, and the
            scroll isn’t consumed, as it would probably be frustrating to waste
            a scroll on something like a misclick. Assuming at least one entity
            was damaged, the scroll is consumed.
        """
        target_xy = action.target_xy
        consumer = action.entity

        if not self.engine.game_map.visible[target_xy]:
            raise exceptions.Impossible("You cannot target an area that you cannot see.")

        targets_hit = False

        results = []
        actors = self.engine.game_map.has_comp("fighter")
        for actor in actors:
            if src.utils.distance(actor.x, actor.y, *target_xy) <= self.radius:
                action.msg += f"The {actor.name} is engulfed in a fiery explosion! "
                actor.fighter.hp -= self.damage

                if actor.fighter.is_dead():
                    results.append(DieAction(entity=actor, cause=consumer))

                targets_hit = True

        if not targets_hit:
            raise exceptions.Impossible("There are no targets in the radius.")

        self.consume()

        return results


class BearTrapConsumable(Consumable):
    def __init__(self, damage, turns):
        self.damage = damage  # How much damage the bear trap will deal.
        self.turns = turns

    def activate(self, action):
        consumer = action.entity

        action.msg = f"A bear trap snaps on the {consumer.name}!! "
        consumer.fighter.hp -= self.damage

        if consumer.fighter.is_dead():
            return DieAction(entity=consumer, cause=self.parent)

        # Set the actors state to trapped for x turns
        consumer.states.add_state("trapped", self.turns)

        self.parent.rm_comp("hidden")  # Reveal the trap


class ConfusionTrapConsumable(Consumable):
    def __init__(self, number_of_turns):
        self.number_of_turns = number_of_turns

    def activate(self, action):
        consumer = action.entity
        x, y = consumer.x, consumer.y
        target = action.entity.gamemap.get_actor_at(x, y)
        if target.name == "player":
            action.msg = f"A spray of green mist hits you! You start to stumble..."
        else:
            action.msg = f"A spray of green mist hits the {target.name} and it starts to stumble around!"

        target.states.add_state("confused", self.number_of_turns)
        self.parent.rm_comp("hidden")  # Reveal the trap


class ParalysisTrapConsumable(Consumable):
    def __init__(self, number_of_turns):
        self.number_of_turns = number_of_turns

    def activate(self, action):
        consumer = action.entity
        x, y = consumer.x, consumer.y
        target = action.entity.gamemap.get_actor_at(x, y)
        if target.name == "player":
            action.msg = f"A spray of purple mist hits you! You can't move..."
        else:
            action.msg = f"A spray of purple mist hits the {target.name}!"

        consumer.states.add_state("paralyzed", self.number_of_turns)

        self.parent.rm_comp("hidden")  # Reveal the trap


class EngravingConsumable(Consumable):
    def __init__(self):
        self.quote = random.choice(quotes.quote_db)

    def activate(self, action):
        target = action.entity.gamemap.get_actor_at(action.entity.x, action.entity.y)
        if target.name == "player":
            action.msg = f"You see an engraving, it reads: '{self.quote}'"


class CamoflaugeConsumable(Consumable):
    def __init__(self, entity, x, y):
        self.x, self.y = x, y
        self.parent = entity

        # Replace the original tile with a "fake" tile to disguide it.
        self.original_tile = self.gamemap.tiles[x, y].copy()

        # We need to customize the tile symbol to blend in with the wall.
        room = self.gamemap.room_coords[x, y]
        self.gamemap.tiles[x, y] = room.char_dict[x, y]  # camo_tile

    def activate(self, action):
        # Replace the camo tile with it's original tile.
        self.gamemap.tiles[self.x, self.y] = self.original_tile