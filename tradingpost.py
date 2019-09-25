"""
@author: Justin Pusztay

Creates a trading post class.
"""

import random
from inventory import Inventory
from item import Item

races = ['Beaver','Turtle','Squirrel','Hedgehog']

class TradingPost(object):

    def __init__(self,merchantName):
        """
        Creates the merchant, their race, and the amount of money that
        they have. Also generates an invetory. 
        """
        self._merchantName = merchantName
        self._race = random.choice(races)
        self._money = random.randint(500,1500)
        self._inventory = Inventory(100)
        self._openForBuying = True
        #self.generateInventory()

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
        pass
        
    def getRace(self):
        """Returns the race of the merchant."""
        return self._race

    def getMerchantName(self):
        """Returns the name of the merchant."""
        return self._merchantName

    def getMoney(self):
        """Returns the money of the merchant."""
        return self._money
        
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
        if self._money >= cost and item.isBuyable() and \
           self._openForBuying == True:
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
        if item in self._inventory and item.isSellable():
            self._inventory.removeItem(item)
            self._money = self._money + price

    def moneyGeneration(self,rate = 1.01):
        """
        Merchants will generate money back as they will do business
        with other animals at a rate of 1% of their current amount.
        """
        self._money = round(self._money * rate)

    def minimumMoney(self):
        """
        When the merchant has less than a uniquely random generated number
        of acorns, the merchant will simply not buy any items.
        """
        if self._money < random.randint(450,700):
            self._openForBuying = False
            

        
            
