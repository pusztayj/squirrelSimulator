"""
@author: Justin Pusztay, Trevor Stalnaker
Filename: items.py

In this file we make all of our items.

Note that tools and health potions are not sharable. 
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
    
    def __init__(self,owner,name, strength, level=1, durability=100,
                 utility = 100,value = 50, staminaCost = 10,requirements=None,
                 isBuyable = True, isSellable = True):
        """
        Here we initialize a generalized weapon class.

        Durability: The health of the item
        Utility: The usefullness of the item
        Value: The market of the item.
        Level: The level of the item
        """
        Item.__init__(self,owner,name,level=1, durability=100,
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
               "Owner: " + self._owner.getName() + \
               "\nType: " + "Weapon" + \
               Item.__repr__(self) + \
                "\nBase Strength: " + str(round(self._strength))
               #"\nBase strength: " + str(round(self._strength + (self._level * (self._strength * (.05)))))
               
class Stick(Weapon,Drawable):

    def __init__(self,owner,strength = 10, level=1, durability=100,
                 utility = 100,value = 20, staminaCost = 10,requirements=None,
                 isBuyable = True, isSellable = True):
        """
        Here we create a specific weapon, named a stick.
        """
        Weapon.__init__(self,owner,"Stick", strength, level, durability,
                 utility,value, staminaCost,requirements,
                 isBuyable, isSellable)
        Drawable.__init__(self,"stick.png",(0,0))
        self._value = value
        

class Spear(Weapon,Drawable):

    def __init__(self,owner, strength = 15, level=1, durability=100,
                 utility = 100,value = 35, staminaCost = 10,requirements=None,
                 isBuyable = True, isSellable = True):
        """
        Here we create a specific weapon, named a spear.
        """
        Weapon.__init__(self, owner, "Spear", strength, level, durability,
                 utility,35, staminaCost,requirements,
                 isBuyable, isSellable)
        Drawable.__init__(self,"spear.png",(0,0))
        self._value = value

class IronSword(Weapon,Drawable):

    def __init__(self, owner, strength = 20, level=1, durability=100,
                 utility = 100,value = 70, staminaCost = 10,requirements=None,
                 isBuyable = True, isSellable = True):
        """
        Here we create a specific weapon, named an iron sword.

        This item is not sharable.
        """
        Weapon.__init__(self, owner, "Iron Sword", strength, level, durability,
                 utility,80, staminaCost,requirements,
                 isBuyable, isSellable)
        Drawable.__init__(self,"sword.png",(0,0))
        self._value = value

weapons = [Stick, Spear, IronSword]

########################################################
#################### Armor #############################
########################################################

class Armor(Item):

    def __init__(self, owner, name, strength, level=1, durability=100,
                 utility = 100,value = 50,requirements=None,
                 isBuyable = True, isSellable = True):
        """
        Here we initialize a generalized armor class.

        Durability: The health of the item
        Utility: The usefullness of the item
        Value: The market of the item.
        Level: The level of the item
        """
        Item.__init__(self, owner, name,level=1, durability=100,
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
               "Owner: " + self._owner.getName() + \
               "\nType: " + "Armor" + \
               Item.__repr__(self) + \
               "\nBase Strength: " + str(round(self._strength))
               #"\nBase strength: " + str(round(self._strength + (self._level * (self._strength * (.05)))))

class HideArmor(Armor,Drawable):
    
    def __init__(self,owner,strength = 8, level=1, durability=100,
                 utility = 100,value = 30,requirements=None,
                 isBuyable = True, isSellable = True):
        """
        Here we create a specific type of armor named Hide Armor. 
        """
        Armor.__init__(self,owner,"Hide Armor", strength, level, durability,
                 utility,35,requirements,
                 isBuyable, isSellable)

        Drawable.__init__(self,"hide_armor.png",(0,0))
        self._value = value

class LeatherArmor(Armor,Drawable):
    
    def __init__(self, owner, strength = 12, level=1, durability=100,
                 utility = 100,value = 45,requirements=None,
                 isBuyable = True, isSellable = True):
        """
        Here we create a specific type of armor named Leather Armor. 
        """
        Armor.__init__(self, owner, "Leather Armor", strength, level, durability,
                 utility,75,requirements,
                 isBuyable, isSellable)
        Drawable.__init__(self,"leather_armor.png",(0,0))
        self._value = value

class IronArmor(Armor,Drawable):
    
    def __init__(self, owner, strength = 17, level=1, durability=100,
                 utility = 100,value = 80,requirements=None,
                 isBuyable = True, isSellable = True):
        """
        Here we create a specific type of armor named Iron Armor. 
        """
        Armor.__init__(self, owner, "Iron Armor", strength, level, durability,
                 utility,value,requirements,
                 isBuyable, isSellable)
        Drawable.__init__(self,"iron_armor.png",(0,0))
        self._value = value
        

armors = [HideArmor, LeatherArmor, IronArmor]

########################################################
#################### Food ##############################
########################################################

class Food(Item):

    def __init__(self, owner, name, healthBoost, hungerBoost, level=1, durability=100,
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
        Item.__init__(self, owner, name,level=1, durability=100,
                 utility = 100,value = 50,requirements=None,
                 isBuyable = True, isSellable = True)
        self._healthBoost = healthBoost
        self._hungerBoost = hungerBoost

    def __repr__(self):
        """
        Returns a string representation of the foodstuff
        """
        return "Name: " + self._name + \
               "Owner: " + self._owner.getName() + \
               "\nType: " + "Food" + \
               Item.__repr__(self) + \
               "\nBase Health Boost: " + str(round(self._healthBoost))

class Berries(Food,Drawable):

    def __init__(self,  owner, healthBoost=5, hungerBoost=2, level=1, durability=100,
                 utility = 100,value = 15,requirements=None,
                 isBuyable = True, isSellable = True):
        """
        Here we create a specific type of armor named Iron Armor. 
        """
        Food.__init__(self, owner, "Berries", healthBoost, hungerBoost, level,
                         durability, utility,value,requirements, isBuyable,
                         isSellable)
        Drawable.__init__(self,"berries.png",(0,0))
        self._value = value

class NutSoup(Food,Drawable):

    def __init__(self, owner, healthBoost = 8, hungerBoost=4, level=1, durability=100,
                 utility = 100,value = 20,requirements=None,
                 isBuyable = True, isSellable = True):
        """
        Here we create a specific type of food named Nut Soup/Acorn Chowder. 
        """
        name = ["Nut Soup","Acorn Chowder"]
        Food.__init__(self,owner,random.choice(name), healthBoost, hungerBoost, level,
                         durability, utility,value,requirements, isBuyable,
                         isSellable)
        Drawable.__init__(self,"nutsoup.png",(0,0))
        self._value = value

class PecanPie(Food,Drawable):

    def __init__(self, owner, healthBoost = 13, hungerBoost=6, level=1, durability=100,
                 utility = 100,value = 45,requirements=None,
                 isBuyable = True, isSellable = True):
        """
        Here we create a specific type of food named Peacan Pie. 
        """
        Food.__init__(self,owner,"Pecan Pie", healthBoost, hungerBoost, level,
                         durability, utility,value,requirements, isBuyable,
                         isSellable)
        Drawable.__init__(self,"pecanpie.png",(0,0))
        self._value = value

########################################################
#################### Tool ##############################
########################################################

class Tool(Item):

    def __init__(self, owner, name, strength, level=1, durability=100,
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
        Item.__init__(self, owner, name,level=1, durability=100,
                 utility = 100,value = 50,requirements=None,
                 isBuyable = True, isSellable = True)
        self._strength = strength
        self._staminaCost = staminaCost
        self._acornBoost = acornBoost

    def getAcornBoost(self):
        return self._acornBoost

    def __repr__(self):
        """
        Returns a string representation of the tool.
        """
        return "Name: " + self._name + \
               "Owner: " + self._owner.getName() + \
               "\nType: " + "Tool" + \
               "\nAcorn Bonus: " + str(self._acornBoost/0.01) + "%" + \
               Item.__repr__(self) + \
               "\nBase Strength: " + str(round(self._strength))

class Shovel(Tool,Drawable):

    def __init__(self, owner, strength = 3, level=1, durability=100,
                 utility = 100,value = 50,staminaCost = 10, acornBoost = .2,
                 requirements=None, isBuyable = True, isSellable = True):
        """
        Here we create a specific type of tool named shovel. 
        """
        Tool.__init__(self, owner, "Shovel", strength, level,
                         durability, utility,value,staminaCost,acornBoost,requirements, isBuyable,
                         isSellable)
        Drawable.__init__(self,"shovel.png",(0,0))
        self._value = value

    def acornModifier(self):
        return 1.2 + self._level*.2

class PickAx(Tool,Drawable):

    def __init__(self, owner, strength = 5, level=1, durability=100,
                 utility = 100,value = 60,staminaCost = 10, acornBoost = .3,
                 requirements=None, isBuyable = True, isSellable = True):
        """
        Here we create a specific type of tool named pick ax. 
        """
        Tool.__init__(self, owner, "Pick Ax", strength, level,
                         durability, utility,value,staminaCost,acornBoost,requirements, isBuyable,
                         isSellable)
        Drawable.__init__(self,"pickax.png",(0,0))
        self._value = value

    def acornModifier(self):
        return 1.3 + self._level*.3

class Hoe(Tool,Drawable):

    def __init__(self, owner, strength = 8, level=1, durability=100,
                 utility = 100,value = 40,staminaCost = 10, acornBoost = .1,
                 requirements=None, isBuyable = True, isSellable = True):
        """
        Here we create a specific type of tool named hoe. 
        """
        Tool.__init__(self, owner, "Hoe", strength, level,
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

    def __init__(self, owner, healthBoost = 50,level=1, durability=100,
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
        super().__init__(owner, "Health Potion",level=1, durability=100,
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
               "Owner: " + self._owner.getName() + \
               "\nType: " + "Potions" + \
               Item.__repr__(self) + \
               "\nHealth Boost: " + str(round(self._healthBoost))
    
