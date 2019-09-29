"""
Filename: itemslist.py

In this file we make all of our items.
"""

from item import Item, Weapon, Armor

########################################################

class Stick(Weapon):

    def __init__(self, level=1):
        super().__init__("Stick", 10, level, None, value = 50)

class Spear(Weapon):

    def __init__(self, level=1):
        super().__init__("Spear", 15, level, None, value = 150)

class IronSword(Weapon):

    def __init__(self, level=1):
        super().__init__("Iron Sword", 25, level, None, value = 450)

########################################################

class HideArmor(Armor):
    
    def __init__(self, level=1):
        super().__init__("Hide Armor", 8, level, None,value = 75)

class LeatherArmor(Armor):
    
    def __init__(self, level=1):
        super().__init__("Leather Armor", 13, level, None,value = 175)

class IronArmor(Armor):
    
    def __init__(self, level=1):
        super().__init__("Leather Armor", 21, level, None,value = 475)

########################################################

class Food(Item):

    def __init__(self, name,healthBoost):
        super.__init__(name)
        self._healthBosst = healthBoost

class Berries(Food):

    def __init__(self):
        super.__init__("Berries",5,value = 15)

class NutSoup(Food):

    def __init__(self):
        super.__init__("Nut Soup",8,value = 20)

class PecanPie(Food):

    def __init__(self):
        super.__init__("Pecan Pie",13, value = 45)

########################################################

class Tool(Item):

    def __init__(self,name,damage, level):
        super(). __init__(name,level)
        self._damage = damage

def Shovel(Tool):

    def __init__(self):
        super(). __init__("Shovel",3,1,value = 40)

    def acornModifier(self):
        return 1.1 + self._level*.1

def PickAx(Tool):

    def __init__(self):
        super(). __init__("Pick ax",5,1,value = 65)

    def acornModifier(self):
        return 1.2 + self._level*.1

def Crowbar(Tool):

    def __init__(self):
        super(). __init__("Crowbar",8,1,value = 95)

    def acornModifier(self):
        return 1.3 + self._level*.1

########################################################





    
