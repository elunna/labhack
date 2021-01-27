from src.actions import ItemAction
from components.base_component import BaseComponent
from components.inventory import Inventory
from components.ai import ConfusedEnemy, ParalyzedAI
from src.exceptions import Impossible
from src import color, input_handlers


class Consumable(BaseComponent):
    def get_action(self, consumer):
        """Try to return the action for this item."""
        return ItemAction(consumer, self.parent)

    def activate(self, action):
        """Invoke this items ability.
            `action` is the context for this activation.
        """
        raise NotImplementedError()

    def consume(self):
        """Remove the consumed item from its containing inventory."""

        entity = self.parent
        inventory = entity.parent

        if isinstance(inventory, Inventory):
            inventory.items.remove(entity)


class HealingConsumable(Consumable):
    def __init__(self, amount):
        self.amount = amount

    def activate(self, action):
        consumer = action.entity
        amount_recovered = consumer.fighter.heal(self.amount)

        if amount_recovered > 0:
            self.engine.message_log.add_message(
                f"You consume the {self.parent.name}, and recover {amount_recovered} HP!",
                color.health_recovered,
            )
            self.consume()
        else:
            raise Impossible(f"Your health is already full.")


class ConfusionPotionConsumable(Consumable):
    def __init__(self, number_of_turns):
        self.number_of_turns = number_of_turns

    def activate(self, action):
        consumer = action.entity

        # TODO: Adjust for throwing at other monsters, etc.
        self.engine.message_log.add_message(
            f"You feel confused...", color.status_effect_applied
        )
        consumer.ai = ConfusedEnemy(
            entity=consumer,
            previous_ai=consumer.ai,
            turns_remaining=self.number_of_turns,
        )
        self.consume()


class ParalysisConsumable(Consumable):
    def __init__(self, number_of_turns):
        self.number_of_turns = number_of_turns

    def activate(self, action):
        consumer = action.entity

        # TODO: Adjust for throwing at other monsters, etc.
        self.engine.message_log.add_message(
            f"You can't move...", color.status_effect_applied
        )
        consumer.ai = ParalyzedAI(
            entity=consumer,
            previous_ai=consumer.ai,
            turns_remaining=self.number_of_turns,
        )
        self.consume()


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
                distance = consumer.distance(actor.x, actor.y)

                if distance < closest_distance:
                    target = actor
                    closest_distance = distance

        if target:
            self.engine.message_log.add_message(
                f"A lighting bolt zaps the {target.name} with a roaring crack!!"
            )
            target.fighter.take_damage(self.damage)
            self.consume()
        else:
            raise Impossible("No enemy is close enough to strike.")


class ConfusionConsumable(Consumable):
    def __init__(self, number_of_turns):
        self.number_of_turns = number_of_turns

    def get_action(self, consumer):
        self.engine.message_log.add_message(
            "Select a target location.", color.needs_target
        )
        return input_handlers.SingleRangedAttackHandler(
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
            raise Impossible("You cannot target an area that you cannot see.")
        if not target:
            raise Impossible("You must select an enemy to target.")
        if target is consumer:
            raise Impossible("You cannot confuse yourself!")

        self.engine.message_log.add_message(
            f"The eyes of the {target.name} look vacant, as it starts to stumble around!",
            color.status_effect_applied,
        )
        target.ai = ConfusedEnemy(
            entity=target, previous_ai=target.ai, turns_remaining=self.number_of_turns,
        )
        self.consume()


class FireballDamageConsumable(Consumable):
    def __init__(self, damage, radius):
        self.damage = damage
        self.radius = radius

    def get_action(self, consumer):
        # asks the user to select a target, and switches the event handler
        self.engine.message_log.add_message(
            "Select a target location.", color.needs_target
        )
        return input_handlers.AreaRangedAttackHandler(
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

        if not self.engine.game_map.visible[target_xy]:
            raise Impossible("You cannot target an area that you cannot see.")

        targets_hit = False
        for actor in self.engine.game_map.actors:
            if actor.distance(*target_xy) <= self.radius:
                self.engine.message_log.add_message(
                    f"The {actor.name} is engulfed in a fiery explosion!"
                )
                actor.fighter.take_damage(self.damage)
                targets_hit = True

        if not targets_hit:
            raise Impossible("There are no targets in the radius.")
        self.consume()
