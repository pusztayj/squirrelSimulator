"""
Author: Trevor Stalnaker
File: menu.py

A general class for creating menus

Parameters:
    pos - (x,y) position for the top-left corner of the menu
    dims - (width, height) pixels of the menu
    commands - list of dictionaries specifying the button attributes
    padding - (horizontal, vertical) padding between border and buttons
    spacing - space in pixels between buttons
    color - rgb color of the menu background (None for transparent)
    borderColor - rgb color value for border
    borderWidth - pixel width for the border
    font - Supplied as a pygame font
"""

import pygame
from graphics import *
from modules.drawable import Drawable

class Menu(Drawable, Window):

    def __init__(self, pos, dims, commands, padding=0, spacing=0,
                 color=(80,80,80), borderColor=(0,0,0),
                 borderWidth=2, font=None):
        """Initializes the menu"""

        Drawable.__init__(self, "", pos, worldBound=False)
        Window.__init__(self)

        self._offset = (pos[0], pos[1])

        self._width  = dims[0]
        self._height = dims[1]

        h_padding = padding[0]
        v_padding = padding[1]

        if font == None:
            self._font = pygame.font.SysFont("Times New Roman", 24)
        else:
            self._font = font
            
        self._borderColor = borderColor
        self._borderWidth = borderWidth
        self._backgroundColor = color

        n = len(commands)

        buttonWidth  = self._width - (2*h_padding) - (2*borderWidth)
        buttonHeight = (self._height - (2*v_padding) - \
                       ((n-1)*spacing) - (2*borderWidth)) // n

        xStart = h_padding
        yStart = v_padding

        self._buttons = []
        for x, b in enumerate(commands):
            self._buttons.append((Button(b["text"],
                                         (xStart + self._offset[0],
                                          yStart + (x*buttonHeight) + \
                                          (x*spacing) + self._offset[1]),
                                    self._font, b["fontColor"], b["color"],
                                    buttonHeight, buttonWidth, b["borderColor"],
                                         b["borderWidth"]),
                                  x+1, b["closeOnPress"]))

        self._selection = None

        self.createDisplay()

    def handleEvent(self, event):
        """Handles events on the pause menu"""
        for b in self._buttons:
            b[0].handleEvent(event,self.select,b[1],b[2])#,offset=self._offset)
        self.updateMenu()
        return self.getSelection()

    def select(self, selection, closeOnPress):
        """Sets the current selection"""
        if closeOnPress:
            self.close()
        self._selection = selection


    def getSelection(self):
        """Returns the current selection and resets it to None"""
        sel = self._selection
        self._selection = None
        return sel

    def draw(self, screen):
        """Draws the menu on the screen"""
        super().draw(screen)
        # Draw buttons
        for b in self._buttons:
            b[0].draw(screen)

    def createDisplay(self):
        """Create the display of the menu"""

        # Draw the border
        surfBack = pygame.Surface((self._width, self._height))
        surfBack.fill(self._borderColor)

        # Draw the background
        surf = pygame.Surface((self._width - (self._borderWidth * 2),
                              self._height - (self._borderWidth * 2)))

        # Apply the background color or make transparent
        if self._backgroundColor == None:
            surf.fill((1,1,1))
            surfBack.set_colorkey((1,1,1))
        else:
            surf.fill(self._backgroundColor)

        # Blit the widget layer onto the back surface
        surfBack.blit(surf, (self._borderWidth, self._borderWidth))
        
        self._image = surfBack
