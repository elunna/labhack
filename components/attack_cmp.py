from components.component import Component

""" Describes the attack that a player, monster, or item has.
    Consists of:
        * the attack "verbs" (ie: kicks, bites, punches, etc)
        * The die(s) to roll for each attack
        * Any special power associated with the attack (cold, fire, poison)
        * Any bonus to-hit or damage for each attack.

    Ex: A MEAN horsie has some bites and kick attacks.
    { 'bite': 2d6, 'bite': 2d6', 'kick': 2d8 )

    Instead of D-notation, we can use lists of ints
    { 'bite': [6, 6], 'bite': [6, 6], 'kick': [6, 6])

    What if the monster has a special attack, like poison?
    { 'bite': [6, 6], 'poison': [6, 6])

    This is a possibility, but it leaves out how they are poisoning you (bite, sting, stab). One way to
    solve this could be to create more top dicts of attacks.

    self.physical_attacks = { 'bite': [6, 6], 'bite': [6, 6], 'kick': [6, 6])
    self.special_attacks = {
        'poison': {'bite': [6, 6], 'bite': [6, 6]'),
        'cold': {'freezing breath': [10]]
    }

    Attacks could also get bonuses - like to-hit or constant damage bonuses (ie: 1d6 + 1)

    { 'bite': [6, 6], 'poison': [6, 6], 'to-hit': 1, 'bonus': 2)

    But it might be easier to simply have:
        self.physical_to_hit_bonus
        self.physical_dmg_bonus
        self.special_to_hit_bonus
        self.special_dmg_bonus

    We might be able to create lambdas for more advanced calculations.

    And against specific breeds of monsters, we can also add (or subtract) certain bonuses:
        Water vs metallic enemies
        Poison vs non-poison resistant enemies
        Cold vs Fire-resistant enemies
        Fire vs cold-resistant enemies

    Also good to note what kind of attack this falls into:
        Melee: standard
        Ranged (thrown object)
        Ray (Wand/gun)
        Firearms
        Explosive (huge to-hit bonus

    We would also just use a list of named tuples.
    Attack = collections.namedtuple('Attack', 'name dies bonus_dmg tohit special ')
    
    Note: Named tuples did not work with *args, with got clogged up being uppacked.
"""


class AttackComponent(Component):
    def __init__(self, *args):
        # args is a tuple of Attack named tuples
        self.attacks = tuple(args)

    def __len__(self):
        return len(self.attacks)
