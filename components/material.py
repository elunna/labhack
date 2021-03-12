from components.component import Component


MATERIALS = [
    "CLOTH", "COPPER", "GLASS", "IRON", "LEATHER", "PAPER", "PLASTIC", "WOOD",
    # BONE?
    # types of plastic
    # RUBBER
    # aluminium, acrylic, and dense plastics, poly-carbonate, epoxy,
    # ABS, styrofoam
]

CORROSIONS = [
    "BURN", "ROT", "MELT", "RUST", "CORRODE",
    # RADIATED, IRRADIATED?, DULL
]


class MaterialComponent(Component):
    """Defines the type of material that an item or entity is constructed from and manages it's level of
    corrosion. The more corroded something is, the less effective it is and the more likely it is to break
    or outright disintegrate.

    Erosion_levels:
        # 0 is no corrosion
        # 1 is the first level of corrosion (no lingual modifier) ex: just "rusted"
        # 2 is the second level: "very rusted"
        # 3 is the third and final level of corrosion: "thoroughly rusted"

        Examples:
            A burned cloak has the same effectiveness as a -1 enchantment.
            A very burned cloak has the same effectiveness as a -2 enchantment.
            A thoroughly burned cloak has the same effectiveness as a -3 enchantment.
            If an item with -3 erosion in a single type (like burned) is burned again - it is destroyed.

    Vulnerabilities:
        Some items are vulnerable to certain effects which instantly destroy the item
            (and may cause other effects)
        Glass is subject to sharp strikes and forces and may shatter.
        Gas is subject to fire and may explode.

    """
    def __init__(self, material, *vulnerabilities):
        if material not in MATERIALS:
            raise ValueError(f"{material} is not a valid material!")
        self.material = material

        if any(v for v in vulnerabilities if v not in CORROSIONS):
            raise ValueError(f'MaterialComponent received invalid vulnerabilitiy!')

        # Create a dict of the different valid erosions, start each one at 0.
        self.erosion = {v: 0 for v in vulnerabilities}

        # "SHATTER", "FREEZE", "ZAP/VAPORIZE - instantly destroys the item

    def add_erosion(self, erosion_type):
        if erosion_type in self.erosion:
            if self.erosion[erosion_type] < 3:
                self.erosion[erosion_type] += 1
                return True
        return False

        # is it plastic and thoroughly melted?

    # def fix(self, erosion):
        # repairs one level of erosion
        # return True

    def burn(self):
        return self.add_erosion("BURN")

    def rot(self):
        return self.add_erosion("ROT")

    def melt(self):
        return self.add_erosion("MELT")

    def rust(self):
        return self.add_erosion("RUST")

    def corrode(self):
        return self.add_erosion("CORRODE")

    # def impact(self):  # forced/impact
        # impact damage is a sharp physical force, which breaks delicate objects.
        # return True

    # def freeze(self):
    #     return self.material == "GLASS"

    # def is_zappable?
    # 	is it a wand or ring? it will instantly vanish?

    # def is_breakable(self):
    #     return self.breakable

        # (through normal usage or attacking)
        # slightly broken (increased chance of fully breaking by 50%)
        # Reduces effectiveness by 50%
        # The breakable number means it has a 1 in x chance of breaking, 0 never breaks



# subclasses of MaterialComponent
# LeatherItem
# 	vulnerabilities
# WoodItem
# IronItem
# ClothItem
# PaperItem

