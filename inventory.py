"""
Author: Trevor Stalnaker, Justin Pusztay
File: inventory.py

In this class we create an inventory object.
"""

class Inventory():

    def __init__(self, size=9):
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

    def getAvailableSpace(self):
        """Returns the available space of the inventory"""
        return self.getMaxCapacity() - self.getCurrentCapacity()

    def hasSpace(self):
        """Determines if there is an empty slot in the inventory"""
        return self._currentCapacity < self._maxCapacity

    def addItem(self, item):
        """Adds an item to the inventory if possible"""
        if self.hasSpace():
            self._items.append(item)
            self._currentCapacity += 1

    def addItems(self, items):
        """Adds multiple items"""
        assert len(items) < self.getAvailableSpace()
        for item in items:
            self.addItem(item)

    def removeItem(self, item):
        """Removes an item from the inventory if possible"""
        if (item in self._items):
            self._items.remove(item)
            self._currentCapacity -= 1

    def hasItem(self, item):
        """Return true if inventory contains item, false otherwise"""
        return item in self._items

    def increaseMaxCapacity(self, increase):
        """Increases the max capacity of the inventory"""
        self._maxCapacity += increase

    def clear(self):
        """Clears the inventory."""
        self._items = list()

    def __iter__(self):
        """Allows iteration over an inventory"""
        for item in self._items:
            yield item

    def __len__(self):
        """Returns the lenght of the inventory."""
        return len(self._items)

    def __getitem__(self, index):
        """Allows indexing of the inventory"""
        return self._items[index]

    def __setitem__(self, index, item):
        """Allows items to be set via indexing of the inventory"""
        self._items[index] = item

    def __repr__(self):
        return str(self._items)
        
