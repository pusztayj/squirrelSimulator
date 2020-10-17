"""
Author: Trevor Stalnaker
File: packmanager.py

A user interface that allows the player to alter and adjust their pack
"""

from polybius.graphics import Drawable, Window, Button, TextBox, ProgressBar, Menu
from managers import USER_INTERFACE
from polybius.managers import CONSTANTS
from minigame.threexthreeinventory import threeXthreeInventory
from minigame.itemblock import ItemBlock
from economy.acorn import Acorn
from player import Player
import pygame, copy
from graphics import ItemCard
from graphics.tradeMenu import TradeMenu

digitLen = {1:33, 2:38, 3:45, 4:55}

class PackManager(Drawable, Window):

    def __init__(self, pack, screensize):
        """Initializes the pack manager interface"""
        
        Window.__init__(self)

        self._display = False

        self._pack = pack
        self._cardWidth = 300
        self._cardHeight = 275 + 75

        self._copyReference = copy.copy(self._pack.getMembers())

        pos = ((screensize[0]//2)-((self._cardWidth*3)//2),
               (screensize[1]//2)-(self._cardHeight//2))

        Drawable.__init__(self, "", pos, worldBound=False)

        itemCardSize = (3*(self._cardHeight // 4), 5*(self._cardWidth // 4))
        itemCardPos = ((((3*self._cardWidth)//2)+self.getX()) - (itemCardSize[1]//2),
                             ((self._cardHeight//2)+self.getY())-(itemCardSize[0]//2))

        CONSTANTS.addConstant("itemCardSize", itemCardSize)
        CONSTANTS.addConstant("itemCardPos", itemCardPos)
        
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
                tile._remove = False
                return (9, tile.getEntity())
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            self.close()
        
    def draw(self, surface):
        """Draws the tiles of the packmanager to the screen"""
        for tile in self._tiles:
            tile.draw(surface)
        for tile in self._tiles:
            tile.drawPopups(surface)
    
    def update(self, ticks):
        """Updates the timer on the pack manager"""
        self._timeSinceClosed += ticks
        # Only redraw the cards if the pack has changed
        if not self._copyReference == self._pack.getMembers():
            self.redraw()
            self._copyReference = copy.copy(self._pack.getMembers())
        for tile in self._tiles:
            tile.updateCard()

    def redraw(self):
        for i, creature in enumerate(self._pack):
            self._tiles[i].setEntity(creature)

##    def redraw(self):
##        """Redraws the pack manager"""
##        self._tiles = []
##        for i, creature in enumerate(self._pack):
##            self._tiles.append(MemberCard(creature, (self.getX() + (i * self._cardWidth),
##                                                     self.getY())))

    def close(self):
        """Closes the pack manager interface"""
        self._display = False
        self._timeSinceClosed = 0
        # Remove item management dropdowns
        for tile in self._tiles:
            tile._itemMenu = None
            tile._dropdown = None

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

        self.setEntity(self._entity)

        self._remove = False

        self.createBack()

        # Variables for item management
        self._menuType = ""
        self._dropType = ""
        self._itemMenu = None
        self._dropDownTemplate = USER_INTERFACE.getControlsForMenu("dropDownTemplate")[0]
        self._dropdown = None

        # Variables for the popup item card
        self._itemCard = None
        self._itemCardSize = CONSTANTS.get("itemCardSize")
        self._itemCardPos = CONSTANTS.get("itemCardPos")

        self._exitButton = Button("X", (self._itemCardPos[0] + self._itemCardSize[1] - 40
                                        ,self._itemCardPos[1] + 10),
                                  self._font,(0,0,0),(100,100,100),25,25,(0,0,0), 1)

        self._tradeMenu = None
        
    def setEntity(self, entity):

        self._entity = entity
        
        if self._entity != None:

            self._pack = entity.getPack()

            self._avatar = entity.getDefaultImage()
            self._imHeight = entity.getHeight()

            self._offset = self.getPosition()

            # Buttons
            removePos = (190 + self.getX(), 207 + self._avHeight + self.getY())
            self._removeButton = Button("Remove", removePos, self._font, (0,0,0),
                                       (255,0,0), 35, 100, (0,0,0), 1)

            # Inventory Items
            invPos = (10 + self.getX(), 80 + self._avHeight + self.getY())
            self._inventory = threeXthreeInventory(invPos, (175,175), entity)

            weapPos = (190 + self.getX(), 80 + self._avHeight + self.getY())
            self._weapon = ItemBlock(weapPos,(50,50), item=entity.getEquipItem())

            armPos = (190 + self.getX(), 140 + self._avHeight + self.getY())
            self._armor = ItemBlock(armPos,(50,50), item=entity.getArmor())

            # Progress Bars
            healthBarPos = (10 + self.getX(), 45 + self._avHeight + self.getY())
            self._healthBar = ProgressBar(healthBarPos, self._width//4,
                                          entity.getBaseHealth(),
                                          entity.getHealth(),
                                          height=5)
            hungerBarPos = (10 + self.getX(), 55 + self._avHeight + self.getY())
            self._hungerBar = ProgressBar(hungerBarPos, self._width//4,
                                          entity.getBaseHunger(),
                                          entity.getHunger(),
                                          barColor=(235,125,52),
                                          height=5)
            staminaBarPos = (10 + self.getX(), 65 + self._avHeight + self.getY())
            self._staminaBar = ProgressBar(staminaBarPos, self._width//4,
                                          entity.getBaseStamina(),
                                          entity.getStamina(),
                                          barColor=(0,0,255),
                                          height=5)

            # Text Information
            namePos = (20 + self.getX(), 5 + self.getY())
            self._name = TextBox(entity.getName(), namePos, self._fontlarge, (0,0,0))

            # Acorn Information
            self._acorn = Acorn((0,0))
            self._acorn.scale(.68)
            self._acorn = self._acorn.getImage()

            self._acornCount = TextBox("", (self._width-50, 4),
                                        self._fontsmall, (0,0,0))
            acorns = str(entity.getAcorns())
            self._acornCount.setText(acorns)
            acPos = ((self._width - (145 + digitLen[len(acorns)])) + self.getX(), 50 + self._avHeight + self.getY())
            self._acornCount.setPosition(acPos)

    def draw(self, surf):

        Drawable.draw(self, surf)
        
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

            surf.blit(self._avatar, (20 + self.getX(), self.getY() + 42 + ((75//2) - (self._imHeight//2))))
            surf.blit(self._acorn, (self.getX() + (self._width-160), 50 + self._avHeight + self.getY()))

    def drawPopups(self, surf):
        if self._entity != None:
            # Item management menus
            if self._itemMenu != None:
                self._itemMenu.draw(surf)
            if self._dropdown != None:
                self._dropdown.draw(surf)
            if self._itemCard != None:
                self._itemCard.draw(surf)
                self._exitButton.draw(surf)
            if self._tradeMenu != None and self._tradeMenu.getDisplay():
                self._tradeMenu.draw(surf)

    def handleEvent(self, event):
        """"Handles events on the member card"""
        
        if self._entity != None:

            if self._itemCard != None:
                self._itemCard.move(event)
                self._exitButton.handleEvent(event, self.closeItemCard)

            if self._tradeMenu != None and self._tradeMenu.getDisplay():
                self._tradeMenu.handleEvent(event)
            
            if type(self._entity) != Player and self._itemMenu==None:
                self._removeButton.handleEvent(event, self.remove)
            self.updateCard()

            if self._itemMenu != None:

                e = self._itemMenu.handleEvent(event)

                # Create the dropdown for sharing and gifting items
                if (e in (1, 2, 3) and self._menuType=="playerItem") or \
                   (e == 3 and self._menuType=="itemBorrowedByPack"):

                   # Find the position of the new dropdown
                   dropdown_y = self._itemMenu.getButtonByPosition(e-1).getY()
                   dropdown_x = self._itemMenu.getX() + self._itemMenu.getWidth()

                   # Create the commands for the new dropdown
                   dropdown_commands = []
                   for an in self._pack.getTrueMembers():
                      if an != self._pack.getLeader():
                         temp = copy.copy(self._dropDownTemplate)
                         temp["text"] = an.getName()
                         dropdown_commands.append(temp)

                   # Create the new menu
                   i = len(dropdown_commands)
                   if i > 0:
                      dropDownHeight = 2 + (2*(i-1)) + (23*i)
                      self._dropdown = Menu((dropdown_x,dropdown_y),(120, dropDownHeight),
                                      dropdown_commands, padding=(1,1), spacing=2,
                                      color=(120,120,120), borderWidth=0, orientation="vertical")

                mouse_pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button in (1,3):
                   if not self._itemMenu.getCollideRect().collidepoint(mouse_pos) and \
                   (self._dropdown == None or not self._dropdown.getCollideRect().collidepoint(mouse_pos)):
                      self._itemMenu = None
                      self._dropdown = None

                if e == 1:
                    
                   if self._menuType == "playerItem":
                      self._dropType = "share"
                      
                   elif self._menuType == "itemBorrowedByPlayer":
                      tup = self._item.getAttribute("owner").reclaimItem(self._item,
                                                                         self._entity)
                      # Player returns a borrowed item
                      if tup[0]:
                          self._entity.getInventory().removeItem(self._item)
                          self._item.getAttribute("owner").getInventory().addItem(self._item)
                      print(tup[1])
                      self._itemMenu = None
                      
                   elif self._menuType == "itemBorrowedByPack":
                      # Player reclaims a borrowed item
                      if self._pack.getLeader().getInventory().hasSpace():
                          self._pack.getLeader().getInventory().addItem(self._item)
                          self._entity.getInventory().removeItem(self._item)
                      self._itemMenu = None

                   elif self._menuType == "packItem":
                      # Player borrows an item from a pack member
                      tup = self._entity.loanItem(self._item, self._pack.getLeader())
                      if tup[0]:
                          self._pack.getLeader().getInventory().addItem(self._item)
                          self._entity.getInventory().removeItem(self._item)
                      print(tup[1])
                      self._itemMenu = None
                        

                if e == 2:
                    if self._menuType == "playerItem":
                        self._dropType = "gift"
                    elif self._menuType in "itemBorrowedByPlayer":
                        tup = self._item.getAttribute("owner").giveOwnershipItem(self._item,
                                                                                 self._pack.getLeader())
                        if tup[0]:
                            self._item.setOwner(self._pack.getLeader())
                        print(tup[1])
                        self._itemMenu = None
                    elif self._menuType == "itemBorrowedByPack":
                        tup = self._entity.takeOwnership(self._item, self._pack.getLeader())
                        if tup[0]:
                            self._item.setOwner(self._entity)
                        print(tup[1])
                        self._itemMenu = None
                    elif self._menuType == "packItem":
                        tup = self._entity.giveOwnershipItem(self._item, self._pack.getLeader())
                        if tup[0]:
                            self._entity.getInventory().removeItem(self._item)
                            self._pack.getLeader().getInventory().addItem(self._item)
                            self._item.setOwner(self._pack.getLeader())
                        print(tup[1])
                        self._itemMenu = None
                if e == 3:
                    if self._menuType in ("playerItem", "itemBorrowedByPack"):
                        self._dropType = "trade"
                    else:
                        self._tradeMenu = TradeMenu((50,50), (1050, 400), self._pack.getLeader(),
                                                    self._item.getAttribute("owner"), self._item)
                        self._tradeMenu.center()
                        self._itemMenu = None
                if e == 4:
                    self._itemCard = ItemCard(self._item, self._itemCardPos,
                                              self._itemCardSize).getCard()
                    self._itemMenu = None

            item = self._inventory.handleEvent(event)
            if item != None and self._itemCard == None:

               self._item = item
               
               mouse_pos = pygame.mouse.get_pos()

               owner = item.getAttribute("owner")
               leader = self._pack.getLeader()
               if owner == leader and self._inventory.getEntity() == leader:
                  item_commands = USER_INTERFACE.getControlsForMenu("playerItemManagement")
                  self._menuType = "playerItem"
               elif owner != leader and self._inventory.getEntity() == leader:
                  item_commands = USER_INTERFACE.getControlsForMenu("playerItemBorrowedManagement")
                  self._menuType = "itemBorrowedByPlayer"
               elif owner == leader and self._inventory.getEntity() != leader:
                  item_commands = USER_INTERFACE.getControlsForMenu("packItemBorrowedManagement")
                  self._menuType = "itemBorrowedByPack"
               elif owner != leader and self._inventory.getEntity() != leader:
                  item_commands = USER_INTERFACE.getControlsForMenu("packItemManagement")
                  self._menuType = "packItem"
                  
               self._itemMenu = Menu(mouse_pos,(120, 102), item_commands, padding=(4,3), spacing=2,
                        color=(120,120,120), borderWidth=1, orientation="vertical")
               
            if self._dropdown != None:

                de = self._dropdown.handleEvent(event)
                if de != None:
                    creature = [an for an in self._pack.getTrueMembers()
                               if not an == self._pack.getLeader()][de-1]
                    if self._dropType == "share":
                       # Share an item with a pack member
                       tup = creature.borrowItem(self._item, self._pack.getLeader())
                       if tup[0]:
                           self._pack.getLeader().getInventory().removeItem(self._item)
                           creature.getInventory().addItem(self._item)
                       print(tup[1])
                    elif self._dropType == "gift":
                        # Give an item to a pack member
                        tup = creature.takeOwnership(self._item, self._pack.getLeader())
                        if tup[0]:
                            self._pack.getLeader().getInventory().removeItem(self._item)
                            creature.getInventory().addItem(self._item)
                            self._item.setOwner(creature)
                        print(tup[1])
                    elif self._dropType == "trade":
                        self._tradeMenu = TradeMenu((50,50), (1050, 400), self._pack.getLeader(),
                                                    creature, self._item)
                        self._tradeMenu.center()
                    
                    self._dropdown = None
                    self._itemMenu = None

                if self._dropdown != None and self._itemMenu != None:
                    # Remove the dropdown if the mouse moves away
                    mouse_pos = pygame.mouse.get_pos()
                    if not self._itemMenu.getCollideRect().collidepoint(mouse_pos) and \
                       not self._dropdown.getCollideRect().collidepoint(mouse_pos):
                       self._dropdown = None

    def remove(self):
        """Sets the remove flag to true"""
        self._remove = True

    def shouldRemove(self):
        """Returns the boolean remove flag"""
        return self._remove

    def getEntity(self):
        return self._entity

    def closeItemCard(self):
        self._itemCard = None

    def createBack(self):
        # Draw the border
        surfBack = pygame.Surface((self._width, self._height))
        surfBack.fill(self._borderColor)

         # Draw the background
        surf = pygame.Surface((self._width - (self._borderWidth * 2),
                              self._height - (self._borderWidth * 2)))
        surf.fill(self._backgroundColor)

        # Blit the widget layer onto the back surface
        surfBack.blit(surf, (self._borderWidth, self._borderWidth))
        self._image = surfBack
        
    def updateCard(self):
        """Updates the member card display"""
        if self._entity != None:
            self._inventory.update()
            self._healthBar.setProgress(self._entity.getHealth())
            self._hungerBar.setProgress(self._entity.getHunger())
            self._staminaBar.setProgress(self._entity.getStamina())

             # Acorn Information
            self._acorn = Acorn((0,0))
            self._acorn.scale(.68)
            self._acorn = self._acorn.getImage()

            self._acornCount = TextBox("", (self._width-50, 4),
                                        self._fontsmall, (0,0,0))
            acorns = str(self._entity.getAcorns())
            self._acornCount.setText(acorns)
            acPos = ((self._width - (145 + digitLen[len(acorns)])) + self.getX(), 50 + self._avHeight + self.getY())
            self._acornCount.setPosition(acPos)
        
