
import pygame
from graphics import *
from modules.drawable import Drawable

class XPManager(Window):

    def __init__(self, pos, player):

        Window.__init__(self)

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
        self._banner.draw(surf)
        self._availXP.draw(surf)
        for a in self._attrs:
            a.draw(surf)

    def handleEvent(self, event):
        for a in self._attrs:
            a.handleEvent(event)


class AttributeManager(Drawable):

    def __init__(self, pos, dimensions, attribute, player):

        Drawable.__init__(self, "", pos, worldBound=False)

        self._player = player

        font = pygame.font.SysFont("Times New Roman", 24)

        self._width = dimensions[0]
        self._height = dimensions[1]

        self._backgroundColor = (200,200,200)
        self._borderColor = (0,0,0)
        self._borderWidth = 1

        buttonDim = 20
        
        self._plusButton = Button("+", (200,(self._height//2 - buttonDim//2)-2),
                                  font, (0,0,0), (0,255,0),
                                  buttonDim,buttonDim,(0,0,0),1)
        self._text = TextBox(attribute, (0,0), font, (0,0,0))
        self._text.setPosition((5, self._height//2 - self._text.getHeight()//2))
        self._current = TextBox(str(eval("player.get"+attribute.title().replace(" ","")+"()")),
                                (0,0), font, (0,0,0))
        self._current.setPosition(((self._width - self._current.getWidth() - (buttonDim*2)),
                                   self._height//2 - self._current.getHeight()//2))

        self.updateAttribute()

    def handleEvent(self, event):
        self._plusButton.handleEvent(event, self.incrementStat, offset=self._position)
        self.updateAttribute()

    def incrementStat(self):
        pass
        
    def updateAttribute(self):

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
