
from modules.drawable import Drawable
from graphics import Window, Button, TextBox, ProgressBar
from economy.acorn import Acorn
from .threexthreeinventory import threeXthreeInventory
from .itemblock import ItemBlock
import pygame

digitLen = {1:33, 2:38, 3:45, 4:55}

class Interaction(Drawable, Window):

    def __init__(self, entity):
        Drawable.__init__(self, "", (50,25), worldBound=False)
        Window.__init__(self)

        self._entity = entity

        self._avatar = entity.getDefaultImage()
        self._imHeight = entity.getHeight()
        self._avHeight = 75

        # Style Attributes
        self._fontlarge = pygame.font.SysFont("Times New Roman", 32)
        self._font = pygame.font.SysFont("Times New Roman", 24)
        self._fontsmall = pygame.font.SysFont("Times New Roman", 16)
        self._borderColor = (0,0,0)
        self._borderWidth = 5
        self._width = 400
        self._height = 275 + self._avHeight
        self._backgroundColor = (139,79,59)

        self._offset = self.getPosition()

        # Buttons
        self._fightButton = Button("Fight", (15,75 + self._avHeight), self._font, (0,0,0),
                                   (255,0,0), 35, 125, (0,0,0), 2)
        self._befriendButton = Button("Befriend", (15,120 + self._avHeight), self._font, (0,0,0),
                                   (0,255,0), 35, 125, (0,0,0), 2)
        self._stealButton = Button("Steal", (15,165 + self._avHeight), self._font, (0,0,0),
                                   (40,80,150), 35, 125, (0,0,0), 2)
        self._bribeButton = Button("Bribe", (15,210 + self._avHeight), self._font, (0,0,0),
                                   (255,215,0), 35, 125, (0,0,0), 2)

        self._exitButton = Button("X", (self._width-45,10),self._font,(0,0,0),(100,100,100),25,25,
               (0,0,0), 1)

        self._selection = None

        # Inventory Items
        self._inventory = threeXthreeInventory((200,75 + self._avHeight), (175,175), entity)
        self._weapon = ItemBlock((262,20 + self._avHeight),(50,50), item=entity.getEquipItem())
        self._armor = ItemBlock((322,20 + self._avHeight),(50,50), item=entity.getArmor())

        # Progress Bars
        self._healthBar = ProgressBar((266,55), self._width//4,
                                      entity.getBaseHealth(),
                                      entity.getHealth(),
                                      height=5)
        self._hungerBar = ProgressBar((266,65), self._width//4,
                                      entity.getBaseHunger(),
                                      entity.getHunger(),
                                      barColor=(235,125,52),
                                      height=5)
        self._staminaBar = ProgressBar((266,75), self._width//4,
                                      entity.getBaseStamina(),
                                      entity.getStamina(),
                                      barColor=(0,0,255),
                                      height=5)

        # Text Information
        self._name = TextBox(entity.getName(), (20,5), self._fontlarge, (0,0,0))

        p = []
        for animal in entity.getPack():
            if animal != entity and animal != None:
                p.append(animal.getName())
        packTxt = "Pack: " + ", ".join(p)
        if packTxt == "Pack: ":
            packTxt += " N/A"

        self._pack = TextBox(packTxt, (20,40 + self._avHeight), self._font, (0,0,0))

        # Acorn Information
        self._acorn = Acorn((0,0))
        self._acorn.scale(.68)
        self._acorn = self._acorn.getImage()

        self._acornCount = TextBox("", (self._width-50, 4),
                                    self._fontsmall, (0,0,0))
        acorns = str(entity.getAcorns())
        self._acornCount.setText(acorns)
        self._acornCount.setPosition((self._width - (65 + digitLen[len(acorns)]), 20))

        self.updateInteraction()

    def handleEvent(self, event):
        self._fightButton.handleEvent(event, self.fight, offset=self._offset)
        self._befriendButton.handleEvent(event, self.befriend, offset=self._offset)
        self._stealButton.handleEvent(event, self.nothing,  offset=self._offset)
        self._bribeButton.handleEvent(event, self.nothing,  offset=self._offset)
        self._exitButton.handleEvent(event, self.close, offset=self._offset)
        self.updateInteraction()

    def fight(self):
        self._selection = 2

    def befriend(self):
        self._selection = 3

    def getSelection(self):
        sel = self._selection
        self._selection = None
        return sel

    def nothing(self):
        pass

    def getEntity(self):
        return self._entity

    def updateInteraction(self):

        # Draw the border
        surfBack = pygame.Surface((self._width, self._height))
        surfBack.fill(self._borderColor)

        # Draw the background
        surf = pygame.Surface((self._width - (self._borderWidth * 2),
                              self._height - (self._borderWidth * 2)))
        surf.fill(self._backgroundColor)

        # Draw widgets
        self._name.draw(surf)
        self._pack.draw(surf)
        self._fightButton.draw(surf)
        self._befriendButton.draw(surf)
        self._stealButton.draw(surf)
        self._bribeButton.draw(surf)
        self._exitButton.draw(surf)
        self._inventory.draw(surf)
        self._armor.draw(surf)
        self._weapon.draw(surf)
        self._healthBar.draw(surf)
        self._hungerBar.draw(surf)
        self._staminaBar.draw(surf)
        self._acornCount.draw(surf)

        surf.blit(self._avatar, (20,42 + ((75//2) - (self._imHeight//2))))
        surf.blit(self._acorn, (self._width-85, 17))

        # Blit the widget layer onto the back surface
        surfBack.blit(surf, (self._borderWidth, self._borderWidth))
        self._image = surfBack
