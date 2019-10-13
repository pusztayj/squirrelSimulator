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
    
    def __init__(self,name, damage, level=1, durability=100,
                 utility = 100,value = 50, staminaCost = 10,requirements=None,
                 isBuyable = True, isSellable = True):
        Item.__init__(self,name,level=1, durability=100,
                 utility = 100,value = 50,requirements=None,
                 isBuyable = True, isSellable = True)
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
        return "Name: " + self._name + \
               "\nType: " + "Weapon" + \
               Item.__repr__(self) + \
                "\nBase Damage: " + str(round(self._damage))
               #"\nBase Damage: " + str(round(self._damage + (self._level * (self._damage * (.05)))))
               
class Stick(Weapon,Drawable):

    def __init__(self,damage = 10, level=1, durability=100,
                 utility = 100,value = 50, staminaCost = 10,requirements=None,
                 isBuyable = True, isSellable = True):
        Weapon.__init__(self,"Stick", damage, level, durability,
                 utility,value, staminaCost,requirements,
                 isBuyable, isSellable)
        Drawable.__init__(self,"",(0,0))
        

class Spear(Weapon,Drawable):

    def __init__(self,damage = 15, level=1, durability=100,
                 utility = 100,value = 150, staminaCost = 10,requirements=None,
                 isBuyable = True, isSellable = True):
        Weapon.__init__(self,"Spear", damage, level, durability,
                 utility,value, staminaCost,requirements,
                 isBuyable, isSellable)
        Drawable.__init__(self,"",(0,0))

class IronSword(Weapon,Drawable):

    def __init__(self,damage = 25, level=1, durability=100,
                 utility = 100,value = 450, staminaCost = 10,requirements=None,
                 isBuyable = True, isSellable = True):
        Weapon.__init__(self,"Iron Sword", damage, level, durability,
                 utility,value, staminaCost,requirements,
                 isBuyable, isSellable)
        Drawable.__init__(self,"",(0,0))

########################################################
#################### Armor #############################
########################################################

class Armor(Item):

    def __init__(self,name, protection, level=1, durability=100,
                 utility = 100,value = 50,requirements=None,
                 isBuyable = True, isSellable = True):
        Item.__init__(self,name,level=1, durability=100,
                 utility = 100,value = 50,requirements=None,
                 isBuyable = True, isSellable = True)
        self._protection = protection

    def getProtection(self):
        return round((self._protection + (self._level * (self._protection * (.05)))) *
                     (self._durability / self._maxDurability))

    def __repr__(self):
        return "Name: " + self._name + \
               "\nType: " + "Armor" + \
               Item.__repr__(self) + \
               "\nBase Protection: " + str(round(self._protection))
               #"\nBase Protection: " + str(round(self._protection + (self._level * (self._protection * (.05)))))

class HideArmor(Armor,Drawable):
    
    def __init__(self,protection = 8, level=1, durability=100,
                 utility = 100,value = 75,requirements=None,
                 isBuyable = True, isSellable = True):
        Armor.__init__(self,"Hide Armor", protection, level, durability,
                 utility,value,requirements,
                 isBuyable, isSellable)

        Drawable.__init__(self,"",(0,0))

class LeatherArmor(Armor,Drawable):
    
    def __init__(self,protection = 13, level=1, durability=100,
                 utility = 100,value = 175,requirements=None,
                 isBuyable = True, isSellable = True):
        Armor.__init__(self,"Leather Armor", protection, level, durability,
                 utility,value,requirements,
                 isBuyable, isSellable)
        Drawable.__init__(self,"",(0,0))

class IronArmor(Armor,Drawable):
    
    def __init__(self,protection = 21, level=1, durability=100,
                 utility = 100,value = 475,requirements=None,
                 isBuyable = True, isSellable = True):
        Armor.__init__(self,"Iron Armor", protection, level, durability,
                 utility,value,requirements,
                 isBuyable, isSellable)
        Drawable.__init__(self,"",(0,0))
        

########################################################
#################### Food ##############################
########################################################

class Food(Item):

    def __init__(self,name, healthBoost, level=1, durability=100,
                 utility = 100,value = 50,requirements=None,
                 isBuyable = True, isSellable = True):
        Item.__init__(self,name,level=1, durability=100,
                 utility = 100,value = 50,requirements=None,
                 isBuyable = True, isSellable = True)
        self._healthBoost = healthBoost

    def __repr__(self):
        return "Name: " + self._name + \
               "\nType: " + "Food" + \
               Item.__repr__(self) + \
               "\nBase Health Boost: " + str(round(self._healthBoost))

class Berries(Food,Drawable):

    def __init__(self, healthBoost = 5, level=1, durability=100,
                 utility = 100,value = 15,requirements=None,
                 isBuyable = True, isSellable = True):
        Food.__init__(self,"Berries", healthBoost, level,
                         durability, utility,value,requirements, isBuyable,
                         isSellable)
        Drawable.__init__(self,"",(0,0))

class NutSoup(Food,Drawable):

    def __init__(self, healthBoost = 8, level=1, durability=100,
                 utility = 100,value = 20,requirements=None,
                 isBuyable = True, isSellable = True):
        Food.__init__(self,"Nut Soup", healthBoost, level,
                         durability, utility,value,requirements, isBuyable,
                         isSellable)
        Drawable.__init__(self,"",(0,0))

class PecanPie(Food,Drawable):

    def __init__(self, healthBoost = 13, level=1, durability=100,
                 utility = 100,value = 45,requirements=None,
                 isBuyable = True, isSellable = True):
        Food.__init__(self,"Pecan Pie", healthBoost, level,
                         durability, utility,value,requirements, isBuyable,
                         isSellable)
        Drawable.__init__(self,"",(0,0))

########################################################
#################### Tool ##############################
########################################################

class Tool(Item):

    def __init__(self,name, damage, level=1, durability=100,
                 utility = 100,value = 50, staminaCost = 10, acornBoost = .1,
                 requirements=None, isBuyable = True, isSellable = True):
        Item.__init__(self,name,level=1, durability=100,
                 utility = 100,value = 50,requirements=None,
                 isBuyable = True, isSellable = True)
        self._damage = damage
        self._staminaCost = staminaCost
        self._acornBoost = acornBoost

    def __repr__(self):
        return "Name: " + self._name + \
               "\nType: " + "Tool" + \
               "\nAcorn Bonus: " + str(self._acornBoost/0.01) + "%" + \
               Item.__repr__(self) + \
               "\nBase Damage: " + str(round(self._damage))

class Shovel(Tool,Drawable):

    def __init__(self, damage = 3, level=1, durability=100,
                 utility = 100,value = 40,staminaCost = 10, acornBoost = .1,
                 requirements=None, isBuyable = True, isSellable = True):
        Tool.__init__(self,"Shovel", damage, level,
                         durability, utility,value,staminaCost,acornBoost,requirements, isBuyable,
                         isSellable)
        Drawable.__init__(self,"",(0,0))

    def acornModifier(self):
        return 1.1 + self._level*.1

class PickAx(Tool,Drawable):

    def __init__(self, damage = 5, level=1, durability=100,
                 utility = 100,value = 65,staminaCost = 10, acornBoost = .2,
                 requirements=None, isBuyable = True, isSellable = True):
        Tool.__init__(self,"Pick Ax", damage, level,
                         durability, utility,value,staminaCost,acornBoost,requirements, isBuyable,
                         isSellable)
        Drawable.__init__(self,"",(0,0))

    def acornModifier(self):
        return 1.1 + self._level*.1

class CrowBar(Tool,Drawable):

    def __init__(self, damage = 8, level=1, durability=100,
                 utility = 100,value = 95,staminaCost = 10, acornBoost = .3,
                 requirements=None, isBuyable = True, isSellable = True):
        Tool.__init__(self,"Shovel", damage, level,
                         durability, utility,value,staminaCost,acornBoost,requirements, isBuyable,
                         isSellable)
        Drawable.__init__(self,"",(0,0))

    def acornModifier(self):
        return 1.1 + self._level*.1


########################################################
#################### Potions ###########################
########################################################

class Potions(Item,Drawable):

    def __init__(self, healthBoost = 10,level=1, durability=100,
                 utility = 100,value = 50, staminaCost = 10,
                 requirements=None, isBuyable = True, isSellable = True):
        super().__init__("Health Potions",level=1, durability=100,
                 utility = 100,requirements=None,
                 isBuyable = True, isSellable = True)
        Drawable.__init__(self,"",(0,0))
        self._healthBoost = healthBoost
        self._value = self._healthBoost*10

    def __repr__(self):
        return "Name: " + self._name + \
               "\nType: " + "Potions" + \
               Item.__repr__(self) + \
               "\nHealth Boost: " + str(round(self._healthBoost))
    
