"""
@author: Justin Pusztay

Creates a merchant class.
"""

import random, items
from inventory import Inventory
from item import Item
from items import *
from npc import NPC

races = ['Beaver','Turtle','Squirrel','Hedgehog']

class Merchant(object):

    def __init__(self,merchantName):
        """
        Creates the merchant, their race, and the amount of money that
        they have. Also generates an invetory. 
        """
        self._merchantName = merchantName
        self._race = random.choice(races)
        self._money = random.randint(500,1500)
        self._inventory = Inventory(100)
        self._willTrade = True
        self._merchantSpeak = str()
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
        for x in range(3):
            for x in items.__all__:
                if 50 >= random.randint(0,100):
                    self._inventory.addItem(globals()[x]())
        
    def getRace(self):
        """Returns the race of the merchant."""
        return self._race

    def getMerchantName(self):
        """Returns the name of the merchant."""
        return self._merchantName

    def getMoney(self):
        """Returns the money of the merchant."""
        return self._money

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
        assert issubclass(type(item),Item)
        assert type(cost) == int
        item.setUtility(100)
        self._inventory.addItem(item)
        self._money = self._money - cost
    

    def sellItem(self,item,price):
        """
        Sells an item to the player and removes it to the merchant's
        inventory.

        Parameters
        ----------
        item: an Item object
        cost: an integer representing the cost
        """
        assert issubclass(type(item),Item)
        assert type(price) == int
        self._inventory.removeItem(item)
        self._money = self._money + price

    def moneyGeneration(self,rate = 1.01):
        """
        Merchants will generate money back as they will do business
        with other animals at a rate of 1% of their current amount.
        """
        self._money = round(self._money * rate)

    def buyLogic(self,item,cost):
        """
        In this method we will determine the logic of the merchant
        and will return a boolean
        """
        minimumMoney = random.randint(450,700)
        minimumUtility = random.randint(30,50)
        if self._money >= cost:
            if item.isBuyable() == True:
                if self._money - cost >= minimumMoney:
                    if item.getUtility() >= minimumUtility:
                        self._merchantSpeak = "Item bought" 
                        return True
                    else:
                        self._merchantSpeak = "The item did not have enough utility"
                        return False 
                else:
                    self._merchantSpeak = "Merchant does not want to spend too many acorns"
                    return False
            else:
                self._merchantSpeak = "Item is not buyable."
                return False 
        else:
            self._merchantSpeak = "Merchant did not have enough money."
            return False

    def sellLogic(self,item,cost):
        """Returns a boolean whether or not the tradiing post wants
        to sell."""
        if item in self._inventory and item.isSellable():
            return True
        else:
            return False
            
                    
