"""
Author: Trevor Stalnaker
File: xpmanager.py

The user interface for managing xp
"""

import pygame
from polybius.graphics import *

class XPManager(Window):

    def __init__(self, pos, player):
        """Initializes the XP Manager interface"""

        Window.__init__(self)

        self._player = player

        font = pygame.font.SysFont("Times New Roman", 24)

        attributes = ["Memory","Charisma","Digging Skill","Cheek Capacity","Stealth"]

        self._availXP = TextBox("Available XP: " + str(player.getXP()),
                                (0,0), font, (0,0,0))

        attStartPos = (pos[0] + 10,pos[1] + 40)
        self._attrs = []
        for i, a in enumerate(attributes):
            self._attrs.append(AttributeManager((attStartPos[0],(i*52)+attStartPos[1]),
                                                (230,50), a, player))

        self._availXP.setPosition(((pos[0] + self._attrs[0].getWidth()//2 -
                                    self._availXP.getWidth()//2) + 10,
                                   pos[1] + 5))

        self._banner = Banner(pos,(100,100,100),(((len(attributes)+1)*52),
                                              self._attrs[0].getWidth()+20),
                              (0,0,0), 1)

    def draw(self, surf):
        """Draws the XP manager to the screen"""
        self._banner.draw(surf)
        self._availXP.draw(surf)
        for a in self._attrs:
            a.draw(surf)

    def handleEvent(self, event):
        """Handles events on the XP Manager"""
        for a in self._attrs:
            a.handleEvent(event)
            ret = a.getReturn()
            if ret != None: break
        self.updateManager()
        return ret

    def updateManager(self):
        """Updates the XP manager interface"""
        self._availXP.setText("Available XP: " + str(self._player.getXP()))


class AttributeManager(Drawable):

    def __init__(self, pos, dimensions, attribute, player):
        """Initiates an attribute manager"""

        Drawable.__init__(self, "", pos, worldBound=False)

        self._player = player
        self._attr = attribute

        self._font = pygame.font.SysFont("Times New Roman", 24)

        self._width = dimensions[0]
        self._height = dimensions[1]

        self._backgroundColor = (200,200,200)
        self._borderColor = (0,0,0)
        self._borderWidth = 1

        self._buttonDim = 20
        
        self._plusButton = Button("+", (200,(self._height//2 - self._buttonDim//2)-2),
                                  self._font, (0,0,0), (0,255,0),
                                  self._buttonDim,self._buttonDim,(0,0,0),1)
        self._text = TextBox(attribute, (0,0), self._font, (0,0,0))
        self._text.setPosition((5, self._height//2 - self._text.getHeight()//2))
        self._current = TextBox(str(eval("player.get"+attribute.title().replace(" ","")+"()")),
                                (0,0), self._font, (0,0,0))
        self._current.setPosition(((self._width - self._current.getWidth() - (self._buttonDim*2)),
                                   self._height//2 - self._current.getHeight()//2))

        self._ret = None

        self.updateAttribute()

    def handleEvent(self, event):
        """Handles events on the attribute manager"""
        self._plusButton.handleEvent(event, self.incrementStat, offset=self._position)
        self.updateAttribute()

    def incrementStat(self):
        """Increment the stat of the attribute"""
        if self._player.getXP() <= 0:
            self._ret = (0,)
        else:
            a = self._attr.replace(" ","")
            eval("self._player.set" + a + "(self._player.get" + a + "() + 1)")
            self._player.setXP(self._player.getXP()-1)
            self._ret = (1, self._attr)

    def getReturn(self):
        """Return the return value created by incrementStat"""
        ret = self._ret
        self._ret = None
        return ret
                   
    def updateAttribute(self):
        """Update the display of the attribute"""

        self._current = TextBox(str(eval("self._player.get"+self._attr.title().replace(" ","")+"()")),
                                (0,0), self._font, (0,0,0))
        self._current.setPosition(((self._width - self._current.getWidth() - (self._buttonDim*2)),
                                   self._height//2 - self._current.getHeight()//2))

        # Draw the border
        surfBack = pygame.Surface((self._width, self._height))
        surfBack.fill(self._borderColor)

        # Draw the background
        surf = pygame.Surface((self._width - (self._borderWidth * 2),
                              self._height - (self._borderWidth * 2)))
        surf.fill(self._backgroundColor)

        # Draw widgets
        self._plusButton.draw(surf)
        self._text.draw(surf)
        self._current.draw(surf)
        
        # Blit the widget layer onto the back surface
        surfBack.blit(surf, (self._borderWidth, self._borderWidth))
        self._image = surfBack
