"""
Author: Trevor Stalnaker
File window.py

An abstract class containing methods for basic windows
"""

class Window():

    def __init__(self):
        self._display = True

    def close(self):
        self._display = False

    def getDisplay(self):
        return self._display
