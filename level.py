"""
Author: Trevor Stalnaker, Justin Pusztay
File: level.py

An abstract class containing general methods for levels
"""
class Level():

    def __init__(self):
        self._active = True

    def isActive(self):
        """
        Returns if the level is active
        """
        return self._active

    def setActive(self, boolean):
        """
        Sets the active state of the tab
        """
        self._active = boolean
