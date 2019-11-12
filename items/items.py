"""
Filename: items.py

In this file we make all of our items.
"""

from .item import Item
from modules.drawable import Drawable

__all__ = ["Stick","Spear","IronSword","HideArmor","LeatherArmor","IronArmor",
         "Berries","NutSoup","PecanPie","Shovel","PickAx",
         "CrowBar","Potions"]

########################################################
#################### Weapons ###########################
########################################################

class Weapon(Item):
    
    def __init__(self,name, strength, level=1, durability=100,
                 utility = 100,value = 50, staminaCost = 10,requirements=None,
                 isBuyable = True, isSellable = True):
        Item.__init__(self,name,level=1, durability=100,
                 utility = 100,value = 50,requirements=None,
                 isBuyable = True, isSellable = True)
        self._strength = strength
        self._staminaCost = staminaCost
        self._causesBleeding = False


    def getStrength(self):
        """Calculate the strength done by the weapon"""
        return round((self._strength + (self._level * (self._strength * (.05)))) *
                     (self._durability / self._maxDurability))

    def getStaminaCost(self):
        return self._staminaCost    

    def __repr__(self):
        return "Name: " + self._name + \
               "\nType: " + "Weapon" + \
               Item.__repr__(self) + \
                "\nBase Strength: " + str(round(self._strength))
               #"\nBase strength: " + str(round(self._strength + (self._level * (self._strength * (.05)))))
               
class Stick(Weapon,Drawable):

    def __init__(self,strength = 10, level=1, durability=100,
                 utility = 100,value = 50, staminaCost = 10,requirements=None,
                 isBuyable = True, isSellable = True):
        Weapon.__init__(self,"Stick", strength, level, durability,
                 utility,value, staminaCost,requirements,
                 isBuyable, isSellable)
        Drawable.__init__(self,"stick.png",(0,0))
        

class Spear(Weapon,Drawable):

    def __init__(self,strength = 15, level=1, durability=100,
                 utility = 100,value = 150, staminaCost = 10,requirements=None,
                 isBuyable = True, isSellable = True):
        Weapon.__init__(self,"Spear", strength, level, durability,
                 utility,value, staminaCost,requirements,
                 isBuyable, isSellable)
        Drawable.__init__(self,"spear.png",(0,0))

class IronSword(Weapon,Drawable):

    def __init__(self,strength = 25, level=1, durability=100,
                 utility = 100,value = 450, staminaCost = 10,requirements=None,
                 isBuyable = True, isSellable = True):
        Weapon.__init__(self,"Iron Sword", strength, level, durability,
                 utility,value, staminaCost,requirements,
                 isBuyable, isSellable)
        Drawable.__init__(self,"sword.png",(0,0))

########################################################
#################### Armor #############################
########################################################

class Armor(Item):

    def __init__(self,name, strength, level=1, durability=100,
                 utility = 100,value = 50,requirements=None,
                 isBuyable = True, isSellable = True):
        Item.__init__(self,name,level=1, durability=100,
                 utility = 100,value = 50,requirements=None,
                 isBuyable = True, isSellable = True)
        self._strength = strength

    def getStrength(self):
        return round((self._strength + (self._level * (self._strength * (.05)))) *
                     (self._durability / self._maxDurability))

    def __repr__(self):
        return "Name: " + self._name + \
               "\nType: " + "Armor" + \
               Item.__repr__(self) + \
               "\nBase Strength: " + str(round(self._strength))
               #"\nBase strength: " + str(round(self._strength + (self._level * (self._strength * (.05)))))

class HideArmor(Armor,Drawable):
    
    def __init__(self,strength = 8, level=1, durability=100,
                 utility = 100,value = 75,requirements=None,
                 isBuyable = True, isSellable = True):
        Armor.__init__(self,"Hide Armor", strength, level, durability,
                 utility,value,requirements,
                 isBuyable, isSellable)

        Drawable.__init__(self,"hide_armor.png",(0,0))

class LeatherArmor(Armor,Drawable):
    
    def __init__(self,strength = 13, level=1, durability=100,
                 utility = 100,value = 175,requirements=None,
                 isBuyable = True, isSellable = True):
        Armor.__init__(self,"Leather Armor", strength, level, durability,
                 utility,value,requirements,
                 isBuyable, isSellable)
        Drawable.__init__(self,"leather_armor.png",(0,0))

class IronArmor(Armor,Drawable):
    
    def __init__(self,strength = 21, level=1, durability=100,
                 utility = 100,value = 475,requirements=None,
                 isBuyable = True, isSellable = True):
        Armor.__init__(self,"Iron Armor", strength, level, durability,
                 utility,value,requirements,
                 isBuyable, isSellable)
        Drawable.__init__(self,"iron_armor.png",(0,0))
        

########################################################
#################### Food ##############################
########################################################

class Food(Item):

    def __init__(self,name, healthBoost, hungerBoost, level=1, durability=100,
                 utility = 100,value = 50,requirements=None,
                 isBuyable = True, isSellable = True):
        Item.__init__(self,name,level=1, durability=100,
                 utility = 100,value = 50,requirements=None,
                 isBuyable = True, isSellable = True)
        self._healthBoost = healthBoost
        self._hungerBoost = hungerBoost

    def __repr__(self):
        return "Name: " + self._name + \
               "\nType: " + "Food" + \
               Item.__repr__(self) + \
               "\nBase Health Boost: " + str(round(self._healthBoost))

class Berries(Food,Drawable):

    def __init__(self, healthBoost=5, hungerBoost=2, level=1, durability=100,
                 utility = 100,value = 15,requirements=None,
                 isBuyable = True, isSellable = True):
        Food.__init__(self,"Berries", healthBoost, hungerBoost, level,
                         durability, utility,value,requirements, isBuyable,
                         isSellable)
        Drawable.__init__(self,"berries.png",(0,0))

class NutSoup(Food,Drawable):

    def __init__(self, healthBoost = 8, hungerBoost=4, level=1, durability=100,
                 utility = 100,value = 20,requirements=None,
                 isBuyable = True, isSellable = True):
        Food.__init__(self,"Nut Soup", healthBoost, hungerBoost, level,
                         durability, utility,value,requirements, isBuyable,
                         isSellable)
        Drawable.__init__(self,"nutsoup.png",(0,0))

class PecanPie(Food,Drawable):

    def __init__(self, healthBoost = 13, hungerBoost=6, level=1, durability=100,
                 utility = 100,value = 45,requirements=None,
                 isBuyable = True, isSellable = True):
        Food.__init__(self,"Pecan Pie", healthBoost, hungerBoost, level,
                         durability, utility,value,requirements, isBuyable,
                         isSellable)
        Drawable.__init__(self,"pecanpie.png",(0,0))

########################################################
#################### Tool ##############################
########################################################

class Tool(Item):

    def __init__(self,name, strength, level=1, durability=100,
                 utility = 100,value = 50, staminaCost = 10, acornBoost = .1,
                 requirements=None, isBuyable = True, isSellable = True):
        Item.__init__(self,name,level=1, durability=100,
                 utility = 100,value = 50,requirements=None,
                 isBuyable = True, isSellable = True)
        self._strength = strength
        self._staminaCost = staminaCost
        self._acornBoost = acornBoost

    def __repr__(self):
        return "Name: " + self._name + \
               "\nType: " + "Tool" + \
               "\nAcorn Bonus: " + str(self._acornBoost/0.01) + "%" + \
               Item.__repr__(self) + \
               "\nBase Strength: " + str(round(self._strength))

class Shovel(Tool,Drawable):

    def __init__(self, strength = 3, level=1, durability=100,
                 utility = 100,value = 40,staminaCost = 10, acornBoost = .1,
                 requirements=None, isBuyable = True, isSellable = True):
        Tool.__init__(self,"Shovel", strength, level,
                         durability, utility,value,staminaCost,acornBoost,requirements, isBuyable,
                         isSellable)
        Drawable.__init__(self,"shovel.png",(0,0))

    def acornModifier(self):
        return 1.1 + self._level*.1

class PickAx(Tool,Drawable):

    def __init__(self, strength = 5, level=1, durability=100,
                 utility = 100,value = 65,staminaCost = 10, acornBoost = .2,
                 requirements=None, isBuyable = True, isSellable = True):
        Tool.__init__(self,"Pick Ax", strength, level,
                         durability, utility,value,staminaCost,acornBoost,requirements, isBuyable,
                         isSellable)
        Drawable.__init__(self,"pickax.png",(0,0))

    def acornModifier(self):
        return 1.1 + self._level*.1

class CrowBar(Tool,Drawable):

    def __init__(self, strength = 8, level=1, durability=100,
                 utility = 100,value = 95,staminaCost = 10, acornBoost = .3,
                 requirements=None, isBuyable = True, isSellable = True):
        Tool.__init__(self,"Crowbar", strength, level,
                         durability, utility,value,staminaCost,acornBoost,requirements, isBuyable,
                         isSellable)
        Drawable.__init__(self,"crowbar.png",(0,0))

    def acornModifier(self):
        return 1.1 + self._level*.1


########################################################
#################### Potions ###########################
########################################################

class Potions(Item,Drawable):

    def __init__(self, healthBoost = 25,level=1, durability=100,
                 utility = 100,value = 50, staminaCost = 10,
                 requirements=None, isBuyable = True, isSellable = True):
        super().__init__("Health Potions",level=1, durability=100,
                 utility = 100,requirements=None,
                 isBuyable = True, isSellable = True)
        Drawable.__init__(self,"healthpotion.png",(0,0))
        self._healthBoost = healthBoost
        self._value = self._healthBoost*10

    def getHealthBoost(self):
        return self._healthBoost

    def __repr__(self):
        return "Name: " + self._name + \
               "\nType: " + "Potions" + \
               Item.__repr__(self) + \
               "\nHealth Boost: " + str(round(self._healthBoost))
    
