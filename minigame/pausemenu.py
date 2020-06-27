"""
Author: Trevor Stalnaker
File: pausemenu.py

The menu that displays when the game is paused
"""

import pygame
from graphics import *
from modules.drawable import Drawable

class PauseMenu(Drawable, Window):

    def __init__(self, pos, dimensions):
        """Initializes the pause menu"""

        Drawable.__init__(self, "", pos, worldBound=False)
        Window.__init__(self)

        self._offset = (pos[0], pos[1])

        self._width  = dimensions[0]
        self._height = dimensions[1]

        self._font = pygame.font.SysFont("Times New Roman", 24)
        self._borderColor = (0,0,0)
        self._borderWidth = 2
        self._backgroundColor = (80,80,80)

        commands = [("Resume",self.resume,(0,255,0)),
                    ("Mute",self.mute,(120,120,150)),
                    ("How To Play",self.howToPlay,(120,120,150)),
                    ("Controls",self.showControls,(120,120,150)),
                    ("Quit",self.quit,(255,0,0))]

        buttonWidth  = 3 * (self._width // 4)
        buttonHeight = (self._height-30) // len(commands)

        buttonXpos = self._width//2 - buttonWidth // 2

        self._buttons = []
        for x, b in enumerate(commands):
            self._buttons.append((Button(b[0],(buttonXpos,15 + (x*buttonHeight)),
                                    self._font, (0,0,0), b[2],
                                    buttonHeight, buttonWidth, (0,0,0), 2),
                                 b[1]))

        self._selection = None

        self.updateMenu()

    def handleEvent(self, event):
        """Handles events on the pause menu"""
        for b in self._buttons:
            b[0].handleEvent(event,b[1],offset=self._offset)
        self.updateMenu()
        return self.getSelection()

    def resume(self):
        """Sets the selection to resume"""
        self.close()
        self._selection = 1

    def showControls(self):
        """Sets the selecton to controls"""
        self._selection = 3

    def howToPlay(self):
        """Sets the selection to how to play"""
        self._selection = 2

    def mute(self):
        """Sets the selection to mute"""
        self._selection = 5
        if self._buttons[1][0]._text == "Mute":
            self._buttons[1][0].setText("Unmute")
        else:
            self._buttons[1][0].setText("Mute")

    def quit(self):
        """Sets the selectoin to quit"""
        self.close()
        self._selection = 4

    def getSelection(self):
        """Returns the current selection and resets it to None"""
        sel = self._selection
        self._selection = None
        return sel

    def updateMenu(self):
        """Updates the display of the pause menu"""

        # Draw the border
        surfBack = pygame.Surface((self._width, self._height))
        surfBack.fill(self._borderColor)

        # Draw the background
        surf = pygame.Surface((self._width - (self._borderWidth * 2),
                              self._height - (self._borderWidth * 2)))
        surf.fill(self._backgroundColor)

        # Draw widgets
        for b in self._buttons:
            b[0].draw(surf)
        
        # Blit the widget layer onto the back surface
        surfBack.blit(surf, (self._borderWidth, self._borderWidth))
        self._image = surfBack
