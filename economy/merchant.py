"""
@author: Justin Pusztay

In this class we create a merchant. This represents the logic
behind how buying and selling for the merchant work. It also handles
the transactions for the merchant with add/removing the item from the
inventory as well as adding/subtracting the appropriate acorns. 
"""

import random, items, shelve
from inventory import Inventory
from items.item import Item
from animals import NPC
from modules import Drawable
from animals.animalManager import ANIMALS
from items.itemManager import ITEMS

RACES = ANIMALS.getMerchantRaces()
ALL_ITEMS = ITEMS.getItems()

class Merchant(NPC, Drawable):

    def __init__(self,name = "", pos=(0,0), restockTimer=None):
        """
        Creates the merchant, their race, and the amount of acorns that
        they have. Also generates an invetory. 
        """
        Drawable.__init__(self, "merchant.png", pos)
        shelf = shelve.open("data")
        name = random.choice(shelf["names"])
        shelf.close()
        self._merchantName = name
        self._race = random.choice(RACES)
        self._acorns = random.randint(500,1500)
        self._inventory = Inventory(100)
        self._willTrade = True
        self._merchantSpeak = str()
        self._restockTimer = restockTimer
        self._restockTime = restockTimer
        self.generateInventory()

    def __iter__(self):
        """
        Creates an iterable item for the inventory.
        """
        for item in self._inventory:
            yield item

    def generateInventory(self):
        """
        Generates an inventory for the merchant. 
        """
        self._inventory.clear()
        for _ in range(3):
            for item in ALL_ITEMS:
                if 50 >= random.randint(0,100):
                    self._inventory.addItem(Item(item, self))

    def setRestockTimer(self, ticks):
        """Sets the restock time and timer for the merchant"""
        self._restockTimer = ticks
        self._restockTime = ticks

        
    def getRace(self):
        """Returns the race of the merchant."""
        return self._race

    def getName(self):
        """Returns the name of the merchant."""
        return self._merchantName

    def getAcorns(self):
        """Returns the acorns of the merchant."""
        return self._acorns

    def getMerchantSpeak(self):
        """Returns the buying logic of the merchant."""
        return self._merchantSpeak

    def getInventory(self):
        """Returns the inventory of the merchant."""
        return self._inventory

    def buyItem(self,item,cost):
        """
        Buys an item from the player and adds it to the merchant's
        inventory.

        Parameters
        ----------
        item: an Item object
        cost: an integer representing the cost
        """
        assert type(item) == Item
        assert type(cost) == int
        item.setUtility(100)
        self._inventory.addItem(item)
        self._acorns = self._acorns - cost
    

    def sellItem(self,item,price):
        """
        Sells an item to the player and removes it to the merchant's
        inventory.

        Parameters
        ----------
        item: an Item object
        cost: an integer representing the cost
        """
        assert type(item) == Item
        assert type(price) == int
        self._inventory.removeItem(item)
        self._acorns = self._acorns + price

    def acornsGeneration(self,rate = 1.01):
        """
        Merchants will generate acorns back as they will do business
        with other animals at a rate of 1% of their current amount.
        """
        self._acorns = round(self._acorns * rate)

    def buyLogic(self,item,cost):
        """
        In this method we will determine the logic of the merchant
        and will return a boolean
        """
        minimumacorns = random.randint(450,700)
        minimumUtility = random.randint(30,50)
        if self._acorns >= cost:
            if item.isBuyable() == True and item.getAttribute("name") != "Health Potion":
                if self._acorns - cost >= minimumacorns:
                    if item.getAttribute("utility") >= minimumUtility:
                        self._merchantSpeak = "Item Sold" 
                        return True
                    else:
                        self._merchantSpeak = "The item did not have enough utility"
                        return False 
                else:
                    self._merchantSpeak = "Merchant does not want to spend too many acorns"
                    return False
            else:
                if item.getAttribute("name") != "Health Potion":
                    self._merchantSpeak = "Item is not buyable."
                else:
                    self._merchantSpeak = "You can't sell health potions."
                return False 
        else:
            self._merchantSpeak = "Merchant did not have enough acorns."
            return False

    def sellLogic(self,item,cost):
        """Returns a boolean whether or not the tradiing post wants
        to sell."""
        if item in self._inventory and item.isSellable():
            self._merchantSpeak = "Item bought"
            return True
        else:
            self._merchantSpeak = "Item not sellable"
            return False

    def __repr__(self):
        """
        Returns a string representation of the merchant. 
        """
        return "Name:          " + self._merchantName + \
               "\nSpecies:       " + self._race + \
               "\nAcorns:        " + str(self._acorns) + \
               "\nInventory:     " + str(self._inventory)

    def update(self, ticks):
        """Updates the merchant's inventory based on ticks"""
        if self._restockTimer != None:
            self._restockTimer -= ticks
            if self._restockTimer <= 0:
                self.generateInventory()
                self._restockTimer = self._restockTime

               


            
                    
