"""
Author: Trevor Stalnaker
File: inventory.py
"""

class Inventory():

    def __init__(self, size=10):
        self._maxCapacity = size
        self._currentCapacity = 0
        self._items = []

    def getCurrentCapacity(self):
        """Returns the current capacity of the inventory"""
        return self._currentCapacity

    def getMaxCapacity(self):
        """Returns the max capacity of the inventory"""
        return self._maxCapacity

    def setMaxCapacity(self, capacity):
        """Sets the max capacity of the inventory"""
        self._maxCapacity = capacity

    def hasSpace(self):
        """Determines if there is an empty slot in the inventory"""
        return self._currentCapacity < self._maxCapacity

    def addItem(self, item):
        """Adds an item to the inventory if possible"""
        if self.hasSpace():
            self._items.append(item)
            self._currentCapacity += 1

    def removeItem(self, item):
        """Removes an item from the inventory if possible"""
        if (item in self._items):
            self._items.remove(item)
            self._currentCapacity -= 1

    def increaseMaxCapacity(self, increase):
        """Increases the max capacity of the inventory"""
        self._maxCapacity += increase

    def __iter__(self):
        """Allows iteration over an inventory"""
        for item in self._items:
            yield item

    def __getitem__(self, index):
        """Allows indexing of the inventory"""
        return self._items[index]

    def __setitem__(self, index, item):
        """Allows items to be set via indexing of the inventory"""
        self._items[index] = item
        
