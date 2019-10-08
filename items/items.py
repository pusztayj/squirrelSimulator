"""
Filename: items.py

In this file we make all of our items.
"""

from item import Item

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
        super().__init__(name,level=1, durability=100,
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
               super().__repr__() + \
                "\nBase Damage: " + str(round(self._damage))
               #"\nBase Damage: " + str(round(self._damage + (self._level * (self._damage * (.05)))))
               
class Stick(Weapon):

    def __init__(self,damage = 10, level=1, durability=100,
                 utility = 100,value = 50, staminaCost = 10,requirements=None,
                 isBuyable = True, isSellable = True):
        super().__init__("Stick", damage, level, durability,
                 utility,value, staminaCost,requirements,
                 isBuyable, isSellable)

class Spear(Weapon):

    def __init__(self,damage = 15, level=1, durability=100,
                 utility = 100,value = 150, staminaCost = 10,requirements=None,
                 isBuyable = True, isSellable = True):
        super().__init__("Spear", damage, level, durability,
                 utility,value, staminaCost,requirements,
                 isBuyable, isSellable)

class IronSword(Weapon):

    def __init__(self,damage = 25, level=1, durability=100,
                 utility = 100,value = 450, staminaCost = 10,requirements=None,
                 isBuyable = True, isSellable = True):
        super().__init__("Iron Sword", damage, level, durability,
                 utility,value, staminaCost,requirements,
                 isBuyable, isSellable)

########################################################
#################### Armor #############################
########################################################

class Armor(Item):

    def __init__(self,name, protection, level=1, durability=100,
                 utility = 100,value = 50,requirements=None,
                 isBuyable = True, isSellable = True):
        super().__init__(name,level=1, durability=100,
                 utility = 100,value = 50,requirements=None,
                 isBuyable = True, isSellable = True)
        self._protection = protection

    def getProtection(self):
        return round((self._protection + (self._level * (self._protection * (.05)))) *
                     (self._durability / self._maxDurability))

    def __repr__(self):
        return "Name: " + self._name + \
               "\nType: " + "Armor" + \
               super().__repr__() + \
               "\nBase Protection: " + str(round(self._protection))
               #"\nBase Protection: " + str(round(self._protection + (self._level * (self._protection * (.05)))))

class HideArmor(Armor):
    
    def __init__(self,protection = 8, level=1, durability=100,
                 utility = 100,value = 75,requirements=None,
                 isBuyable = True, isSellable = True):
        super().__init__("Hide Armor", protection, level, durability,
                 utility,value,requirements,
                 isBuyable, isSellable)

class LeatherArmor(Armor):
    
    def __init__(self,protection = 13, level=1, durability=100,
                 utility = 100,value = 175,requirements=None,
                 isBuyable = True, isSellable = True):
        super().__init__("Leather Armor", protection, level, durability,
                 utility,value,requirements,
                 isBuyable, isSellable)

class IronArmor(Armor):
    
    def __init__(self,protection = 21, level=1, durability=100,
                 utility = 100,value = 475,requirements=None,
                 isBuyable = True, isSellable = True):
        super().__init__("Iron Armor", protection, level, durability,
                 utility,value,requirements,
                 isBuyable, isSellable)        

########################################################
#################### Food ##############################
########################################################

class Food(Item):

    def __init__(self,name, healthBoost, level=1, durability=100,
                 utility = 100,value = 50,requirements=None,
                 isBuyable = True, isSellable = True):
        super().__init__(name,level=1, durability=100,
                 utility = 100,value = 50,requirements=None,
                 isBuyable = True, isSellable = True)
        self._healthBoost = healthBoost

    def __repr__(self):
        return "Name: " + self._name + \
               "\nType: " + "Food" + \
               super().__repr__() + \
               "\nBase Health Boost: " + str(round(self._healthBoost))

class Berries(Food):

    def __init__(self, healthBoost = 5, level=1, durability=100,
                 utility = 100,value = 15,requirements=None,
                 isBuyable = True, isSellable = True):
        super().__init__("Berries", healthBoost, level,
                         durability, utility,value,requirements, isBuyable,
                         isSellable)

class NutSoup(Food):

    def __init__(self, healthBoost = 8, level=1, durability=100,
                 utility = 100,value = 20,requirements=None,
                 isBuyable = True, isSellable = True):
        super().__init__("Nut Soup", healthBoost, level,
                         durability, utility,value,requirements, isBuyable,
                         isSellable)

class PecanPie(Food):

    def __init__(self, healthBoost = 13, level=1, durability=100,
                 utility = 100,value = 45,requirements=None,
                 isBuyable = True, isSellable = True):
        super().__init__("Pecan Pie", healthBoost, level,
                         durability, utility,value,requirements, isBuyable,
                         isSellable)

########################################################
#################### Tool ##############################
########################################################

class Tool(Item):

    def __init__(self,name, damage, level=1, durability=100,
                 utility = 100,value = 50, staminaCost = 10, acornBoost = .1,
                 requirements=None, isBuyable = True, isSellable = True):
        super().__init__(name,level=1, durability=100,
                 utility = 100,value = 50,requirements=None,
                 isBuyable = True, isSellable = True)
        self._damage = damage
        self._staminaCost = staminaCost
        self._acornBoost = acornBoost

    def __repr__(self):
        return "Name: " + self._name + \
               "\nType: " + "Tool" + \
               "\nAcorn Bonus: " + str(self._acornBoost/0.01) + "%" + \
               super().__repr__() + \
               "\nBase Damage: " + str(round(self._damage))

class Shovel(Tool):

    def __init__(self, damage = 3, level=1, durability=100,
                 utility = 100,value = 40,staminaCost = 10, acornBoost = .1,
                 requirements=None, isBuyable = True, isSellable = True):
        super().__init__("Shovel", damage, level,
                         durability, utility,value,staminaCost,acornBoost,requirements, isBuyable,
                         isSellable)

    def acornModifier(self):
        return 1.1 + self._level*.1

class PickAx(Tool):

    def __init__(self, damage = 5, level=1, durability=100,
                 utility = 100,value = 65,staminaCost = 10, acornBoost = .2,
                 requirements=None, isBuyable = True, isSellable = True):
        super().__init__("Pick Ax", damage, level,
                         durability, utility,value,staminaCost,acornBoost,requirements, isBuyable,
                         isSellable)

    def acornModifier(self):
        return 1.1 + self._level*.1

class CrowBar(Tool):

    def __init__(self, damage = 8, level=1, durability=100,
                 utility = 100,value = 95,staminaCost = 10, acornBoost = .3,
                 requirements=None, isBuyable = True, isSellable = True):
        super().__init__("Shovel", damage, level,
                         durability, utility,value,staminaCost,acornBoost,requirements, isBuyable,
                         isSellable)

    def acornModifier(self):
        return 1.1 + self._level*.1


########################################################
#################### Potions ###########################
########################################################

class Potions(Item):

    def __init__(self, healthBoost = 10,level=1, durability=100,
                 utility = 100,value = 50, staminaCost = 10,
                 requirements=None, isBuyable = True, isSellable = True):
        super().__init__("Health Potions",level=1, durability=100,
                 utility = 100,requirements=None,
                 isBuyable = True, isSellable = True)
        self._healthBoost = healthBoost
        self._value = self._healthBoost*10

    def __repr__(self):
        return "Name: " + self._name + \
               "\nType: " + "Potions" + \
               super().__repr__() + \
               "\nHealth Boost: " + str(round(self._healthBoost))
    
