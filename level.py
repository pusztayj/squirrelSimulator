"""
Author: Trevor Stalnaker
File: level.py

An abstract class containing general methods for levels
"""
class Level():

    def __init__(self):
        self._active = True

    def isActive(self):
        return self._active

    def setActive(self, boolean):
        self._active = boolean
