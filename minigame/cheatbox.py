"""
Author: Trevor Stalnaker
File: cheats.py

A class that models a cheats box
"""

import pygame
from polybius.graphics import TextInput
from .cheats import *
from managers import ITEMS

class CheatBox():

    def __init__(self, screenDimensions):
        """Initializes the cheat interface"""
        self._font = pygame.font.SysFont("Times New Roman", 16)
        textDimensions = (200,30)
        self._input = TextInput((0,screenDimensions[1]-textDimensions[1]),
                                self._font, textDimensions, maxLen=30)
        self._code = None
        self._display = False
        self._delay = .1 # Without the delay the input starts with an initial c

    def handleEvent(self, event):
        """Handles events on the cheat box"""
        if self._delay < 0:
            self._input.handleEvent(event, self._input.getInput(), func=self.getCheatCode,
                                clearOnEnter=True)
        if self._code != None:
            c = self._code
            self._code = None
            return c

    def toggleDisplay(self):
        """Toggles the cheat display"""
        self._display = not self._display
        if self._display:
            self._input._active = True
            self._input.displayActive()
            self._delay = .1
        else:
            self._input._active = False

    def isDisplayed(self):
        """Returns true if cheats are displayed, false otherwise"""
        return self._display

    def getCheatCode(self, cheat):
        """Sets code to the current cheat if it is valid"""
        terms = cheat.split()
        if len(terms) == 2:
            if terms[0] == "giveAcorns":
                if terms[1].isdigit():
                    self._code = (1,int(terms[1]))
            if terms[0] == "giveXP":
                if terms[1].isdigit():
                    self._code = (2,int(terms[1]))
            if terms[0] == "setHealth":
                if terms[1].isdigit():
                    self._code = (5,int(terms[1]))
            if terms[0] == "giveItem":
                if terms[1].lower() in ITEMS.getItems():
                    self._code = (7,terms[1].lower())
        elif len(terms) == 3:
            if terms[0] == "spawnMerchant":
                if terms[1].isdigit() and terms[2].isdigit():
                    self._code = (3, (int(terms[1]),int(terms[2])))
            if terms[0] == "fastForward":
                if terms[1].isdigit() and terms[2] in ["hours","days"]:
                    self._code = (4,(int(terms[1]),terms[2]))
            if terms[0] == "giveItem":
                if terms[1].lower() in ITEMS.getItems():
                    if terms[2].isdigit():
                        self._code = (7,terms[1].lower(),int(terms[2]))
        elif len(terms) == 5:
            if terms[0] == "spawnAnimal":
                if terms[1].lower() in ("chipmunk","fox","bear","hedgehog","deer","rabbit","shmoo"):
                    if terms[2].isdigit() and terms[3].isdigit():
                        if terms[4].isdigit():
                            self._code = (6,terms[1],(int(terms[2]),int(terms[3])),int(terms[4]))

    def draw(self, screen):
        """Draws the cheat input to the screen"""
        self._input.draw(screen)

    def update(self, ticks):
        """Updates the delay on the cheat input"""
        if self._delay >= 0:
            self._delay -= ticks

    def execute(self, tup):
       """Execute a provided cheat code"""
       codes[tup[0]](*tup[1:])

    def getCodesByType(self, t):
       return types[t]
            


