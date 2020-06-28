"""
@authors: Justin Pusztay, Trevor Stalnaker

We create an abstracted item class that holds its name, level,
durability, utility, whether or not the item is buyable or sellable. 
"""

import random, math
from modules.drawable import Drawable
from managers.itemManager import ITEMS

class Item(Drawable):

    def __init__(self, item, owner=None, level=1):
        """
        Here we initialize the itmem class where we pass its name, utility,
        value, and whether or not the item is buyable or sellable. 
        """
        self._attributes = ITEMS.getAttributes(item)

        Drawable.__init__(self,self._attributes["image"],(0,0))

        self._attributes["item"] = item
        self._attributes["owner"] = owner
        self._attributes["level"] = level
        self._attributes["maxDurability"] = self._attributes["durability"]
        self._attributes["maxUtility"] = 100

    def getAttribute(self, attribute):
        if (attribute in list(self._attributes.keys()) \
           and self._attributes[attribute] != None) \
           or attribute in ("requirements", "owner"):
            return self._attributes[attribute]
        else:
            raise Exception(self._attributes["item"] + \
                            " has no attribute " + attribute)

    def calculateStrength(self):
        """Calculate the item's current strength factoring in level and durability"""
        if self._attributes["strength"] != None:
            strength = self._attributes["strength"]
            return round((strength + (self._attributes["level"] * (strength*.05))) *
                         (self._attributes["durability"] / \
                          self._attributes["maxDurability"]))
        else:
            raise Exception(self._attributes["item"] + \
                            " has no attribute strength")

    def acornModifier(self):
        acornBoost = self._attributes["acornBoost"]
        if self._attributes["acornBoost"] != None:
            return 1 + acornBoost + ((self._attributes["level"]-1)*acornBoost)
        else:
            raise Exception(self._attributes["item"] + \
                            " has no attribute acornBoost")

    def setOwner(self, new):
        """
        Sets the owner of the item.
        """
        self._attributes["owner"] = new
        
    def rename(self, name):
        """Rename an item"""
        self._attributes["name"] = name

    def isBuyable(self):
        """
        Returns if an item is buyable from the presepctive of the player.
        """
        return self._attributes["buyable"]

    def isSellable(self):
        """
        Returns if an item is buyable from the presepctive of the player.
        """
        return self._attributes["sellable"]

    def isSharable(self):
        """
        Returns if an item is sharable. 
        """
        return self._attributes["sharable"]

    def checkRequirements(self, entity):
        """Determines if an entity is worthy of a given item"""
        req = self._attributes["requirements"]
        if req == None:
            return True
        stats = entity.stats()
        for x in range(len(req)):
            if stats[x] < reqs[x]:
                return False
        return True

    def setDurability(self,durability):
        """
        Sets a new durability less than the maximum durability.
        """
        if durability <= self._attributes["maxDurability"]:
            self._attributes["durability"] = durability

    def setUtility(self,utility):
        """
        Sets a new utility less than the maximum utility.
        """
        if utility <= self._attributes["maxUtility"]:
            self._attributes["utility"] = utility

    def decrementDurability(self):
        """Decreases durability by one"""
        self._attributes["durability"] -= 1

    def isBroken(self):
        """Determines if an item has no more durability"""
        return self._attributes["durability"] <= 0

    def __repr__(self):
        temp = "Name: " + self._attributes["name"] + "\nOwner: "
        if self._attributes["owner"] != None:
            temp += self._attributes["owner"].getName()
        else:
            temp += "No owner"
        temp += "\nType: " + self._attributes["type"] + \
                "\nLevel: " + str(self._attributes["level"]) + \
                "\nDurability: " + str(self._attributes["durability"]) + \
                "/" + str(self._attributes["maxDurability"]) + \
                "\nUtility: " + str(self._attributes["utility"]) + "/" + \
                str(self._attributes["maxUtility"]) + \
                "\nValue: " + str(self._attributes["value"])
        for x in [("strength","Base Strength"),
                  ("healthBoost","Health Boost"),
                  ("hungerBoost","Hunger Boost")]:
            if self._attributes[x[0]] != None:
                temp += "\n" + x[1] + ": " + str(round(self._attributes[x[0]]))
        if self._attributes["acornBoost"] != None:
            temp += "\nAcorn Bonus: " + str(self._attributes["acornBoost"]/0.01) + "%"
        return temp


                                       
