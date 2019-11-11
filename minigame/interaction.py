
from modules.drawable import Drawable
from graphics.window import Window
from graphics.button import Button
import pygame

class Interaction(Drawable, Window):

    def __init__(self):
        Drawable.__init__(self, "", (50,25), worldBound=False)
        Window.__init__(self)

        # Style Attributes
        self._font = pygame.font.SysFont("Times New Roman", 24)
        self._fontsmall = pygame.font.SysFont("Times New Roman", 16)
        self._borderColor = (0,0,0)
        self._borderWidth = 5
        self._width = 400
        self._height = 250
        self._backgroundColor = (139,79,59)

        self._offset = self.getPosition()

        # Buttons
        self._fightButton = Button("Fight", (10,50), self._font, (0,0,0),
                                   (255,0,0), 35, 125, (0,0,0), 2)
        self._befriendButton = Button("Befriend", (10,95), self._font, (0,0,0),
                                   (0,255,0), 35, 125, (0,0,0), 2)
        self._stealButton = Button("Steal", (10,140), self._font, (0,0,0),
                                   (40,80,150), 35, 125, (0,0,0), 2)
        self._bribeButton = Button("Bribe", (10,185), self._font, (0,0,0),
                                   (255,215,0), 35, 125, (0,0,0), 2)

        self._exitButton = Button("X", (self._width-45,10),self._font,(0,0,0),(100,100,100),25,25,
               (0,0,0), 1)

        self._selection = None

        self.updateInteraction()

    def handleEvent(self, event):
        self._fightButton.handleEvent(event, self.fight, offset=self._offset)
        self._befriendButton.handleEvent(event, self.nothing, offset=self._offset)
        self._stealButton.handleEvent(event, self.nothing,  offset=self._offset)
        self._bribeButton.handleEvent(event, self.nothing,  offset=self._offset)
        self._exitButton.handleEvent(event, self.close, offset=self._offset)
        self.updateInteraction()

    def fight(self):
        self._selection = 2

    def getSelection(self):
        return self._selection

    def nothing(self):
        pass

    def updateInteraction(self):

        # Draw the border
        surfBack = pygame.Surface((self._width, self._height))
        surfBack.fill(self._borderColor)

        # Draw the background
        surf = pygame.Surface((self._width - (self._borderWidth * 2),
                              self._height - (self._borderWidth * 2)))
        surf.fill(self._backgroundColor)

        # Draw widgets
        self._fightButton.draw(surf)
        self._befriendButton.draw(surf)
        self._stealButton.draw(surf)
        self._bribeButton.draw(surf)
        self._exitButton.draw(surf)

        # Blit the widget layer onto the back surface
        surfBack.blit(surf, (self._borderWidth, self._borderWidth))
        self._image = surfBack
