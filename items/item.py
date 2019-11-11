import random, math

class Item():

    def __init__(self, name, level=1, durability=100, utility = 100,
                 value = 50, requirements=None, isBuyable = True,
                 isSellable = True):
        self._name = name
        self._level = level
        self._skillRequirements = requirements
        self._maxDurability = durability
        self._durability = durability
        self._maxUtility = 100
        self._utility = utility
        self._isBuyable = isBuyable
        self._isSellable = isSellable
        self._value = value

    def getValue(self):
        """Returns the value of the item in acorns."""
        return self._value

    def getName(self):
        """Return the item's name"""
        return self._name

    def rename(self, name):
        """Rename an item"""
        self._name = name

    def isBuyable(self):
        """
        Returns if an item is buyable from the presepctive of the player.
        """
        return self._isBuyable

    def isSellable(self):
        """
        Returns if an item is buyable from the presepctive of the player.
        """
        return self._isSellable

    def getRequirements(self):
        """Display the requirements for the item"""
        return self._skillRequirements

    def checkRequirements(self, entity):
        """Determines if an entity is worthy of a given item"""
        if self._skillRequirements == None:
            return True
        stats = entity.stats()
        for x in range(len(self._skillRequirements)):
            if stats[x] < self._skillRequirements[x]:
                return False
        return True

    def getLevel(self):
        """Return the level of the weapon"""
        return self._level

    def getDurability(self):
        """Return the durability of the item"""
        return self._durability

    def setDurability(self,durability):
        """
        Sets a new durability less than the maximum durability.
        """
        if durability <= self._maxDurability:
            self._durability = durability

    def getUtility(self):
        """Return the durability of the item"""
        return self._utility

    def setUtility(self,utility):
        """
        Sets a new utility less than the maximum utility.
        """
        if utility <= self._maxUtility:
            self._utility = utility

    def decrementDurability(self):
        """Decreases durability by one"""
        self._durability -= 1

    def isBroken(self):
        """Determines if an item has no more durability"""
        return self._durability <= 0

    def __repr__(self):
        return "\nLevel: " + str(self._level) + \
               "\nDurability: " + str(self._durability) + "/" + str(self._maxDurability) + \
               "\nUtility: " + str(self._utility) + "/" + str(self._maxUtility) + \
               "\nValue: " + str(self._value)


                                       
