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

        buttonWidth  = 3 * (self._width // 4)
        buttonHeight = (self._height-30) // 4

        buttonXpos = self._width//2 - buttonWidth // 2
        
        self._resumeButton = Button("Resume", (buttonXpos,15),
                                    self._font, (0,0,0), (0,255,0),
                                    buttonHeight, buttonWidth, (0,0,0), 2)
        self._howToPlayButton = Button("How To Play", (buttonXpos, 15 + buttonHeight),
                                    self._font, (0,0,0), (120,120,150),
                                    buttonHeight, buttonWidth, (0,0,0), 2)
        self._controlsButton = Button("Controls", (buttonXpos, 15 + (2*buttonHeight)),
                                    self._font, (0,0,0), (120,120,150),
                                    buttonHeight, buttonWidth, (0,0,0), 2)
        self._quitButton = Button("Quit", (buttonXpos, 15 + (3*buttonHeight)),
                                    self._font, (0,0,0), (255,0,0),
                                    buttonHeight, buttonWidth, (0,0,0), 2)

        self._selection = None

        self.updateMenu()

    def handleEvent(self, event):
        """Handles events on the pause menu"""
        self._resumeButton.handleEvent(event, self.resume, offset=self._offset)
        self._howToPlayButton.handleEvent(event, self.howToPlay, offset=self._offset)
        self._controlsButton.handleEvent(event, self.showControls, offset=self._offset)
        self._quitButton.handleEvent(event, self.quit, offset=self._offset)
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
        self._resumeButton.draw(surf)
        self._howToPlayButton.draw(surf)
        self._controlsButton.draw(surf)
        self._quitButton.draw(surf)
        
        # Blit the widget layer onto the back surface
        surfBack.blit(surf, (self._borderWidth, self._borderWidth))
        self._image = surfBack
