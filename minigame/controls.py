"""
Author: Trevor Stalnaker
File: controls.py

A class for displaying the games controls
"""

import pygame
from graphics import *

class Controls(Window):

    def __init__(self, pos, height):
        """Initializes the controls interface"""

        Window.__init__(self)

        self._font = pygame.font.SysFont("Courier", 18)
        self._backgroundColor = (0,0,0)
        self._fontColor = (255,255,255)

        stringLen = 35

        controls = [("a","Move Left"),
                    ("d","Move Right"),
                    ("w","Move Up"),
                    ("s","Move Down"),
                    ("b","Dig an Acorn Pile"),
                    ("e","Open Pack Manager"),
                    ("r","Open XP Manager"),
                    ("esc","Pause"),
                    ("left click","Interact with World"),
                    ("right click","Use item"),
                    ("space","Eat an Acorn"),
                    ("num keys","Toggle active item"),
                    ("scroll wheel","Toggle active item"),]

        t = ""
        for i, cont in enumerate(controls):
            t += cont[0]
            t += "." * (stringLen - (len(cont[0]) + len(cont[1])))
            t += cont[1]
            if i < len(controls)-1:
                t += "\n"

        text = makeMultiLineTextBox(t, (5,5), self._font, self._fontColor,
                                    self._backgroundColor)

        width = text.getWidth() + 20

        self._scrollBox = ScrollBox(pos, (height, width), text, (255,255,255), 1)

        self._header = TextBox("Controls", (pos[0]+5, pos[1]-20),self._font, self._fontColor)

        self._closeButton = Button("X", (pos[0] + width - 19,pos[1] - 21),self._font,
                                   (0,0,0),(100,100,100),18,18,(0,0,0), 1)

        self._banner = Banner((pos[0], pos[1]-23),(0,0,0), (21, width), (255,255,255), 1)

    def draw(self, surface):
        """Draws the control interface to the screen"""
        self._banner.draw(surface)
        self._header.draw(surface)
        self._closeButton.draw(surface)
        self._scrollBox.draw(surface)
        

    def handleEvent(self, event):
        """Handles events on the control interface"""
        self._scrollBox.move(event)
        self._closeButton.handleEvent(event, self.close)        
