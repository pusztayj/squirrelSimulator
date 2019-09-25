
import random, math

class Item():

    def __init__(self, name, requirements=None, level=1, durability=100,
                 isBuyable = True, isSellable = True):
        self._name = name
        self._level = level
        self._skillRequirements = requirements
        self._maxDurability = durability
        self._durability = durability
        self._isBuyable = True
        self._isSellable = True
        
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

    def decrementDurability(self):
        """Decreases durability by one"""
        self._durability -= 1

    def isBroken(self):
        """Determines if an item has no more durability"""
        return self._durability <= 0

    def __repr__(self):
        return "Name: " + self._name + \
               "\nType: " + type(self).__name__ + \
               "\nLevel: " + str(self._level) + \
               "\nDurability: " + str(self._durability) + "/" + str(self._maxDurability)


class Weapon(Item):
    
    def __init__(self, name, damage, level, requirements,staminaCost = 10):
        super().__init__(name, requirements, level)
        self._damage = damage
        self._staminaCost = staminaCost
        self._causesBleeding = False

    def getDamage(self):
        """Calculate the damage done by the weapon"""
        return round((self._damage + (self._level * (self._damage * (.05)))) *
                     (self._durability / self._maxDurability))

    def getStaminaCost(self):
        return self._staminaCost    

    def __repr__(self):
        return super().__repr__() + \
               "\nBase Damage: " + str(round(self._damage + (self._level * (self._damage * (.05)))))
                                       
class Armor(Item):

    def __init__(self, name, protection, level, requirements):
        super().__init__(name, requirements, level)
        self._protection = protection

    def getProtection(self):
        return round((self._protection + (self._level * (self._protection * (.05)))) *
                     (self._durability / self._maxDurability))

    def __repr__(self):
        return super().__repr__() + \
               "\nBase Protection: " + str(round(self._protection + (self._level * (self._protection * (.05)))))


class Tool(Weapon):

    def __init__(self, name, damage, level, requirements):
        super.__init__(name, damage, level, requirements)

class Stick(Weapon):

    def __init__(self, level=1):
        super().__init__("stick", 8, level, None)

class SharpStick(Weapon):

    def __init__(self, level=1):
        super().__init__("sharp stick", 12, level, None)
    
class HideArmor(Armor):

    def __init__(self, level=1):
        super().__init__("hide armor", 8, level, None)
