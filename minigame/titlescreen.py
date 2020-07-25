"""
Author: Trevor Stalnaker
File: titlescreen.py

The start screen of the game
"""

import pygame
from polybius.managers import FRAMES, CONTROLS
from graphics import *

class TitleScreen():

    def __init__(self, screensize):
        """Initializes the title screen"""

        self._titleCard = FRAMES.getFrame("title.png")
        self._font = pygame.font.SysFont("Times New Roman", 28)
        self._text = TextBox("Press Space to Start", (0,0), self._font,
                             (255,255,255))
        pos = ((screensize[0]//2) - (self._text.getWidth()//2),
               screensize[1]-125)
        self._text.setPosition(pos)

        self._background = pygame.Surface(screensize)
        self._background.fill((0,0,0))
        
        self._state = 0
        self._textStates = ["Press Space to Start",""]
        self._dotTime = .5
        self._timer = self._dotTime

        self._displayed = True

    def isDisplayed(self):
        """Returns true if the title screen is displayed, false otherwise"""
        return self._displayed

    def handleEvent(self, event):
        """Handles events on the title screen"""
        if CONTROLS.get("start").check(event):
            self._displayed = False

    def draw(self, screen):
        """Draws the title screen to the screen"""
        screen.blit(self._background, (0,0))
        tpos = (self._background.get_width()//2 - self._titleCard.get_width()//2,
                -25)
        screen.blit(self._titleCard, tpos)
        self._text.draw(screen)

    def update(self, ticks):
        """Updates the flashing press space to start"""
        if self._timer < 0:
            self._timer = self._dotTime
            self._state += 1
            self._text.setText(self._textStates[self._state%2])
        else:
            self._timer -= ticks
        

