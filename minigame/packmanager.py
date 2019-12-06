"""
Author: Trevor Stalnaker
File: packmanager.py

A user interface that allows the player to alter and adjust their pack
"""

from modules.drawable import Drawable
from graphics import Window, Button, TextBox, ProgressBar
from .threexthreeinventory import threeXthreeInventory
from .itemblock import ItemBlock
from economy.acorn import Acorn
from player import Player
import pygame

digitLen = {1:33, 2:38, 3:45, 4:55}

class PackManager(Drawable, Window):

    def __init__(self, pack, screensize):
        """Initializes the pack manager interface"""
        
        Window.__init__(self)

        self._display = False

        self._pack = pack
        self._cardWidth = 300
        self._cardHeight = 275 + 75

        pos = ((screensize[0]//2)-((self._cardWidth*3)//2),
               (screensize[1]//2)-(self._cardHeight//2))

        Drawable.__init__(self, "", pos, worldBound=False)
        
        self._tiles = []
        for i, creature in enumerate(pack):
            self._tiles.append(MemberCard(creature, (self.getX() + (i * self._cardWidth),
                                                     self.getY())))

        self._timeSinceClosed = 100 # Arbitrary high value at start
        self._delay = .1 #Delay between opening and closing the window

    def handleEvent(self, event):
        """Handles events on the pack manager"""
        for tile in self._tiles:
            tile.handleEvent(event)
            if tile.shouldRemove():
                return (9, tile.getEntity())
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            self.close()
        
    def draw(self, surface):
        """Draws the tiles of the packmanager to the screen"""
        for tile in self._tiles:
            tile.draw(surface)

    def update(self, ticks):
        """Updates the timer on the pack manager"""
        self._timeSinceClosed += ticks
        self.redraw()

    def redraw(self):
        """Redraws the pack manager"""
        self._tiles = []
        for i, creature in enumerate(self._pack):
            self._tiles.append(MemberCard(creature, (self.getX() + (i * self._cardWidth),
                                                     self.getY())))

    def close(self):
        """Closes the pack manager interface"""
        self._display = False
        self._timeSinceClosed = 0

class MemberCard(Drawable, Window):

    def __init__(self, entity, pos=(50,25)):
        """Initializes a member card"""

        Drawable.__init__(self, "", pos, worldBound=False)
        Window.__init__(self)

        self._entity = entity

        self._avHeight = 75 # Height of largest sprite

        # Style Attributes
        self._fontlarge = pygame.font.SysFont("Times New Roman", 28)
        self._font = pygame.font.SysFont("Times New Roman", 24)
        self._fontsmall = pygame.font.SysFont("Times New Roman", 18)
        self._borderColor = (0,0,0)
        self._borderWidth = 1
        self._width = 300
        self._height = 275 + self._avHeight
        self._backgroundColor = (139,79,59)

        if entity != None:

            self._avatar = entity.getDefaultImage()
            self._imHeight = entity.getHeight()

            self._offset = self.getPosition()

            # Buttons
            self._removeButton = Button("Remove", (190,207 + self._avHeight), self._font, (0,0,0),
                                       (255,0,0), 35, 100, (0,0,0), 1)

            # Inventory Items
            self._inventory = threeXthreeInventory((10,80 + self._avHeight), (175,175), entity)
            self._weapon = ItemBlock((190,80 + self._avHeight),(50,50), item=entity.getEquipItem())
            self._armor = ItemBlock((190,140 + self._avHeight),(50,50), item=entity.getArmor())

            # Progress Bars
            self._healthBar = ProgressBar((10,45 + self._avHeight), self._width//4,
                                          entity.getBaseHealth(),
                                          entity.getHealth(),
                                          height=5)
            self._hungerBar = ProgressBar((10,55 + self._avHeight), self._width//4,
                                          entity.getBaseHunger(),
                                          entity.getHunger(),
                                          barColor=(235,125,52),
                                          height=5)
            self._staminaBar = ProgressBar((10,65 + self._avHeight), self._width//4,
                                          entity.getBaseStamina(),
                                          entity.getStamina(),
                                          barColor=(0,0,255),
                                          height=5)

            # Text Information
            self._name = TextBox(entity.getName(), (20,5), self._fontlarge, (0,0,0))

            # Acorn Information
            self._acorn = Acorn((0,0))
            self._acorn.scale(.68)
            self._acorn = self._acorn.getImage()

            self._acornCount = TextBox("", (self._width-50, 4),
                                        self._fontsmall, (0,0,0))
            acorns = str(entity.getAcorns())
            self._acornCount.setText(acorns)
            self._acornCount.setPosition((self._width - (145 + digitLen[len(acorns)]),
                                          50 + self._avHeight))

        self._remove = False

        self.updateCard()


    def handleEvent(self, event):
        """"Handles events on the member card"""
        if self._entity != None:
            if type(self._entity) != Player:
                self._removeButton.handleEvent(event, self.remove, offset=self._offset)
            self.updateCard()

    def remove(self):
        """Sets the remove flag to true"""
        self._remove = True

    def getEntity(self):
        """Returns the entity linked to member card"""
        return self._entity

    def shouldRemove(self):
        """Returns the boolean remove flag"""
        return self._remove

    def updateCard(self):
        """Updates the member card display"""
        
        # Draw the border
        surfBack = pygame.Surface((self._width, self._height))
        surfBack.fill(self._borderColor)

         # Draw the background
        surf = pygame.Surface((self._width - (self._borderWidth * 2),
                              self._height - (self._borderWidth * 2)))
        surf.fill(self._backgroundColor)

        if self._entity != None:
            # Draw widgets
            self._name.draw(surf)
            self._inventory.draw(surf)
            self._armor.draw(surf)
            self._weapon.draw(surf)
            self._healthBar.draw(surf)
            self._hungerBar.draw(surf)
            self._staminaBar.draw(surf)
            if type(self._entity) != Player:
                self._removeButton.draw(surf)
            self._acornCount.draw(surf)

            surf.blit(self._avatar, (20,42 + ((75//2) - (self._imHeight//2))))
            surf.blit(self._acorn, (self._width-160,50 + self._avHeight))

        # Blit the widget layer onto the back surface
        surfBack.blit(surf, (self._borderWidth, self._borderWidth))
        self._image = surfBack
