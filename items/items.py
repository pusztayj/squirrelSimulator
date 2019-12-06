"""
@author: Justin Pusztay, Trevor Stalnaker
Filename: items.py

In this file we make all of our items.
"""

from .item import Item
from modules.drawable import Drawable
import random

__all__ = ["Stick","Spear","IronSword","HideArmor","LeatherArmor","IronArmor",
         "Berries","NutSoup","PecanPie","Shovel","PickAx",
         "Hoe","Potions"]

########################################################
#################### Weapons ###########################
########################################################

class Weapon(Item):
    
    def __init__(self,name, strength, level=1, durability=100,
                 utility = 100,value = 50, staminaCost = 10,requirements=None,
                 isBuyable = True, isSellable = True):
        """
        Here we initialize a generalized weapon class.

        Durability: The health of the item
        Utility: The usefullness of the item
        Value: The market of the item.
        Level: The level of the item
        """
        Item.__init__(self,name,level=1, durability=100,
                 utility = 100,value = 50,requirements=None,
                 isBuyable = True, isSellable = True)
        self._strength = strength
        self._staminaCost = staminaCost
        self._causesBleeding = False


    def getStrength(self):
        """Calculate the strength done by the weapon."""
        return round((self._strength + (self._level * (self._strength * (.05)))) *
                     (self._durability / self._maxDurability))

    def getStaminaCost(self):
        """
        Here we return the stamina cost of an attack.
        """
        return self._staminaCost    

    def __repr__(self):
        """
        This is a string representation of the weapon. 
        """
        return "Name: " + self._name + \
               "\nType: " + "Weapon" + \
               Item.__repr__(self) + \
                "\nBase Strength: " + str(round(self._strength))
               #"\nBase strength: " + str(round(self._strength + (self._level * (self._strength * (.05)))))
               
class Stick(Weapon,Drawable):

    def __init__(self,strength = 10, level=1, durability=100,
                 utility = 100,value = 20, staminaCost = 10,requirements=None,
                 isBuyable = True, isSellable = True):
        """
        Here we create a specific weapon, named a stick.
        """
        Weapon.__init__(self,"Stick", strength, level, durability,
                 utility,value, staminaCost,requirements,
                 isBuyable, isSellable)
        Drawable.__init__(self,"stick.png",(0,0))
        self._value = value
        

class Spear(Weapon,Drawable):

    def __init__(self,strength = 15, level=1, durability=100,
                 utility = 100,value = 35, staminaCost = 10,requirements=None,
                 isBuyable = True, isSellable = True):
        """
        Here we create a specific weapon, named a spear.
        """
        Weapon.__init__(self,"Spear", strength, level, durability,
                 utility,35, staminaCost,requirements,
                 isBuyable, isSellable)
        Drawable.__init__(self,"spear.png",(0,0))
        self._value = value

class IronSword(Weapon,Drawable):

    def __init__(self,strength = 25, level=1, durability=100,
                 utility = 100,value = 80, staminaCost = 10,requirements=None,
                 isBuyable = True, isSellable = True):
        """
        Here we create a specific weapon, named an iron sword.
        """
        Weapon.__init__(self,"Iron Sword", strength, level, durability,
                 utility,80, staminaCost,requirements,
                 isBuyable, isSellable)
        Drawable.__init__(self,"sword.png",(0,0))
        self._value = value

weapons = [Stick, Spear, IronSword]

########################################################
#################### Armor #############################
########################################################

class Armor(Item):

    def __init__(self,name, strength, level=1, durability=100,
                 utility = 100,value = 50,requirements=None,
                 isBuyable = True, isSellable = True):
        """
        Here we initialize a generalized armor class.

        Durability: The health of the item
        Utility: The usefullness of the item
        Value: The market of the item.
        Level: The level of the item
        """
        Item.__init__(self,name,level=1, durability=100,
                 utility = 100,value = 50,requirements=None,
                 isBuyable = True, isSellable = True)
        self._strength = strength

    def getStrength(self):
        """
        Calculate the strength done by the weapon.
        """
        return round((self._strength + (self._level * (self._strength * (.05)))) *
                     (self._durability / self._maxDurability))

    def __repr__(self):
        """
        Returns a string representation of the armor. 
        """
        return "Name: " + self._name + \
               "\nType: " + "Armor" + \
               Item.__repr__(self) + \
               "\nBase Strength: " + str(round(self._strength))
               #"\nBase strength: " + str(round(self._strength + (self._level * (self._strength * (.05)))))

class HideArmor(Armor,Drawable):
    
    def __init__(self,strength = 8, level=1, durability=100,
                 utility = 100,value = 35,requirements=None,
                 isBuyable = True, isSellable = True):
        """
        Here we create a specific type of armor named Hide Armor. 
        """
        Armor.__init__(self,"Hide Armor", strength, level, durability,
                 utility,35,requirements,
                 isBuyable, isSellable)

        Drawable.__init__(self,"hide_armor.png",(0,0))
        self._value = value

class LeatherArmor(Armor,Drawable):
    
    def __init__(self,strength = 13, level=1, durability=100,
                 utility = 100,value = 75,requirements=None,
                 isBuyable = True, isSellable = True):
        """
        Here we create a specific type of armor named Leather Armor. 
        """
        Armor.__init__(self,"Leather Armor", strength, level, durability,
                 utility,75,requirements,
                 isBuyable, isSellable)
        Drawable.__init__(self,"leather_armor.png",(0,0))
        self._value = value

class IronArmor(Armor,Drawable):
    
    def __init__(self,strength = 21, level=1, durability=100,
                 utility = 100,value = 100,requirements=None,
                 isBuyable = True, isSellable = True):
        """
        Here we create a specific type of armor named Iron Armor. 
        """
        Armor.__init__(self,"Iron Armor", strength, level, durability,
                 utility,value,requirements,
                 isBuyable, isSellable)
        Drawable.__init__(self,"iron_armor.png",(0,0))
        self._value = value
        

armors = [HideArmor, LeatherArmor, IronArmor]

########################################################
#################### Food ##############################
########################################################

class Food(Item):

    def __init__(self,name, healthBoost, hungerBoost, level=1, durability=100,
                 utility = 100,value = 50,requirements=None,
                 isBuyable = True, isSellable = True):
        """
        Here we initialize a generalized armor class.

        healthBoost: The amount of health points that a foodstuff gives
        hungerBoost: The amount of hunger points a food stuff gives

        Durability: The health of the item
        Utility: The usefullness of the item
        Value: The market of the item.
        Level: The level of the item
        """
        Item.__init__(self,name,level=1, durability=100,
                 utility = 100,value = 50,requirements=None,
                 isBuyable = True, isSellable = True)
        self._healthBoost = healthBoost
        self._hungerBoost = hungerBoost

    def __repr__(self):
        """
        Returns a string representation of the foodstuff
        """
        return "Name: " + self._name + \
               "\nType: " + "Food" + \
               Item.__repr__(self) + \
               "\nBase Health Boost: " + str(round(self._healthBoost))

class Berries(Food,Drawable):

    def __init__(self, healthBoost=5, hungerBoost=2, level=1, durability=100,
                 utility = 100,value = 15,requirements=None,
                 isBuyable = True, isSellable = True):
        """
        Here we create a specific type of armor named Iron Armor. 
        """
        Food.__init__(self,"Berries", healthBoost, hungerBoost, level,
                         durability, utility,value,requirements, isBuyable,
                         isSellable)
        Drawable.__init__(self,"berries.png",(0,0))
        self._value = value

class NutSoup(Food,Drawable):

    def __init__(self, healthBoost = 8, hungerBoost=4, level=1, durability=100,
                 utility = 100,value = 20,requirements=None,
                 isBuyable = True, isSellable = True):
        """
        Here we create a specific type of food named Nut Soup/Acorn Chowder. 
        """
        name = ["Nut Soup","Acorn Chowder"]
        Food.__init__(self,random.choice(name), healthBoost, hungerBoost, level,
                         durability, utility,value,requirements, isBuyable,
                         isSellable)
        Drawable.__init__(self,"nutsoup.png",(0,0))
        self._value = value

class PecanPie(Food,Drawable):

    def __init__(self, healthBoost = 13, hungerBoost=6, level=1, durability=100,
                 utility = 100,value = 45,requirements=None,
                 isBuyable = True, isSellable = True):
        """
        Here we create a specific type of food named Peacan Pie. 
        """
        Food.__init__(self,"Pecan Pie", healthBoost, hungerBoost, level,
                         durability, utility,value,requirements, isBuyable,
                         isSellable)
        Drawable.__init__(self,"pecanpie.png",(0,0))
        self._value = value

########################################################
#################### Tool ##############################
########################################################

class Tool(Item):

    def __init__(self,name, strength, level=1, durability=100,
                 utility = 100,value = 50, staminaCost = 10, acornBoost = .1,
                 requirements=None, isBuyable = True, isSellable = True):
        """
        Here we initialize a generalized armor class.

        acornBoost: Increases the % of acorns that get mined.

        Durability: The health of the item
        Utility: The usefullness of the item
        Value: The market of the item.
        Level: The level of the item
        """
        Item.__init__(self,name,level=1, durability=100,
                 utility = 100,value = 50,requirements=None,
                 isBuyable = True, isSellable = True)
        self._strength = strength
        self._staminaCost = staminaCost
        self._acornBoost = acornBoost

    def __repr__(self):
        """
        Returns a string representation of the tool.
        """
        return "Name: " + self._name + \
               "\nType: " + "Tool" + \
               "\nAcorn Bonus: " + str(self._acornBoost/0.01) + "%" + \
               Item.__repr__(self) + \
               "\nBase Strength: " + str(round(self._strength))

class Shovel(Tool,Drawable):

    def __init__(self, strength = 3, level=1, durability=100,
                 utility = 100,value = 60,staminaCost = 10, acornBoost = .2,
                 requirements=None, isBuyable = True, isSellable = True):
        """
        Here we create a specific type of tool named shovel. 
        """
        Tool.__init__(self,"Shovel", strength, level,
                         durability, utility,value,staminaCost,acornBoost,requirements, isBuyable,
                         isSellable)
        Drawable.__init__(self,"shovel.png",(0,0))
        self._value = value

    def acornModifier(self):
        return 1.2 + self._level*.2

class PickAx(Tool,Drawable):

    def __init__(self, strength = 5, level=1, durability=100,
                 utility = 100,value = 95,staminaCost = 10, acornBoost = .3,
                 requirements=None, isBuyable = True, isSellable = True):
        """
        Here we create a specific type of tool named pick ax. 
        """
        Tool.__init__(self,"Pick Ax", strength, level,
                         durability, utility,value,staminaCost,acornBoost,requirements, isBuyable,
                         isSellable)
        Drawable.__init__(self,"pickax.png",(0,0))
        self._value = value

    def acornModifier(self):
        return 1.3 + self._level*.3

class Hoe(Tool,Drawable):

    def __init__(self, strength = 8, level=1, durability=100,
                 utility = 100,value = 40,staminaCost = 10, acornBoost = .1,
                 requirements=None, isBuyable = True, isSellable = True):
        """
        Here we create a specific type of tool named hoe. 
        """
        Tool.__init__(self,"Hoe", strength, level,
                         durability, utility,value,staminaCost,acornBoost,requirements, isBuyable,
                         isSellable)
        Drawable.__init__(self,"crowbar.png",(0,0))
        self._value = value

    def acornModifier(self):
        return 1.1 + self._level*.1


########################################################
#################### Potions ###########################
########################################################

class Potions(Item,Drawable):

    def __init__(self, healthBoost = 50,level=1, durability=100,
                 utility = 100,value = 50, staminaCost = 10,
                 requirements=None, isBuyable = True, isSellable = True):
        """
        Here we initialize a generalized potion class.

        Durability: The health of the item
        Utility: The usefullness of the item
        Value: The market of the item.
        Level: The level of the item

        This item is not sellable. 
        """
        super().__init__("Health Potion",level=1, durability=100,
                 utility = 85,requirements=None,
                 isBuyable = True, isSellable = True)
        Drawable.__init__(self,"healthpotion.png",(0,0))
        self._healthBoost = healthBoost
        self._value = 100

    def getHealthBoost(self):
        """
        Returns the health boost of the potion.
        """
        return self._healthBoost

    def __repr__(self):
        """
        Returns a string representation of the health potion.
        """
        return "Name: " + self._name + \
               "\nType: " + "Potions" + \
               Item.__repr__(self) + \
               "\nHealth Boost: " + str(round(self._healthBoost))
    
