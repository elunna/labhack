class Behavior:
    """ What the hero (or entity) is "doing". If the hero has no behavior,
    he is waiting for user input. Otherwise, the behavior will determine which
    Actions he performs.
    """
    def __init__(self, hero):
        self.hero = hero

    def can_perform(self):
        # Returns a bool
        raise NotImplementedError()

    def get_action(self):
        # Returns the next logical action according the the behavior.
        raise NotImplementedError()


class RestBehavior(Behavior):
    """ This enables automatic resting. The hero will rest each turn until any
    of the following occurs:
        * He is fully rested.
        * He gets hungry.
        * He gets hit
        * A monster moves within x squares
    """
    def can_perform(self):
        # Check if a monster is next to you...

        # First draft: Always return True
        return True

    def get_action(self):
        # Returns the next logical action according the the behavior.
        return WaitAction()


class RunBehavior(Behavior):
    def __init__(self, hero, direction):
        self.hero = hero
        # We should always be able to take the first step
        self.firststep = True
        self.direction = direction

    def can_perform(self):
        # don't run into a wall
        # stop at doorways (or ends of corridors
        # stop when someone is in the way
        # stop when someone is netx to you
        # stop at items
        # run around corridors (complex)

        # First draft: Always return True
        return True

    def get_action(self):
        self.firststep = False
        # Returns the next logical action according the the behavior.
        return WaitAction()

# class RepeatBehavior
# Repeat an action x times
