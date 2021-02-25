
import pygame
from polybius.graphics import AbstractGraphic, ScrollSelector, \
     MultiLineTextBox, MySurface, TextBox, Incrementer, Button, ScrollBox, \
     Window
from economy.acorn import Acorn
from graphics import ItemCard

class TradeMenu(AbstractGraphic, Window):

    def __init__(self, pos, dimensions, entityOne, entityTwo, tradable):
        
        AbstractGraphic.__init__(self, pos)
        Window.__init__(self)

        self._width = dimensions[0]
        self._height = dimensions[1]

        borderWidth = 2
        borderColor = (0,0,0)

        backSurf = pygame.Surface(dimensions)
        backSurf.fill(borderColor)

        surf = pygame.Surface((self._width-2*borderWidth,
                               self._height-2*borderWidth))
        surf.fill((139,79,59))

        backSurf.blit(surf, (borderWidth, borderWidth))

        self._image = backSurf

        # Get the entities' tradable items
        self._items = {entityOne:[], entityTwo:[]}
        for creature in entityOne.getPack().getTrueMembers():
            for item in creature.getInventory():
                if item.getAttribute("owner") == entityOne:
                    self._items[entityOne].append(item)
                elif item.getAttribute("owner") == entityTwo:
                    self._items[entityTwo].append(item)

        # Set up lists to hold the items to trade
        self._trade = {entityOne:[], entityTwo:[]}
        self._entityOne = entityOne
        self._entityTwo = entityTwo

        if entityOne == tradable.getAttribute("owner"):
            self._trade[entityOne].append(tradable)
        if entityTwo == tradable.getAttribute("owner"):
            self._trade[entityTwo].append(tradable)

        incValueFont = pygame.font.SysFont("Time New Roman", 28)
        btnFont = pygame.font.SysFont("Arial", 14)

        self._entityOneIncrementer = Incrementer((100,400),
                 spacing=3, defaultValue=0,
                 minValue=0, boxDims=(50,30), buttonFont=btnFont,
                 maxValue=self._entityOne.getAcorns(),
                 buttonText=["MIN","<<","<",">",">>","MAX"], increments=[1,5,"all"],
                 buttonBorderWidth=2, buttonDims=(15,20),
                 valueBoxBorderWidth=0,valueBoxBackgroundColor=None,
                 valueBoxAntialias=False,valueFont=incValueFont,
                 padding=(0,0),activeTextInput=False)

        self._entityTwoIncrementer = Incrementer((100,400),
                     defaultValue=0, spacing=3,
                     minValue=0, boxDims=(50,30), buttonFont=btnFont,
                     maxValue=self._entityTwo.getAcorns(),
                     buttonText=["MIN","<<","<",">",">>","MAX"], increments=[1,5,"all"],
                     buttonBorderWidth=2, buttonDims=(15,20),
                     valueBoxBorderWidth=0,valueBoxBackgroundColor=None,
                     valueBoxAntialias=False,valueFont=incValueFont,
                     padding=(0,0),activeTextInput=False)

        self._viewItem = None

        self.updateElementPositions()

    def setViewItem(self, item):
        self._viewItem = item
        owner = self._viewItem.getAttribute("owner")
        if self._viewItem in self._trade[owner]:
            self._moveItemButton.setText("Remove Item from Trade")
        else:
            self._moveItemButton.setText("Add Item to Trade")
        self._itemCard = ItemCard(item, self._itemCard.getPosition(),
                                  (self._itemCardWidth,self._itemCardWidth),
                                  center=True)._card

    def addItemToTrade(self,entity,item):
        self._trade[entity].append(item)
        self.updateTradeDisplay()
    
    def removeItemFromTrade(self,entity,item):
        self._trade[entity].remove(item)
        self.updateTradeDisplay()

    def updateTradeDisplay(self):
        
        y_pos = self._textBoxYPos + self._e1InvText.getHeight() + 5

        # Items in entity one's inventory
        x_pos = self.getX() + self._spacing
        e1Items = [{"text": item.getAttribute("name"),"func": self.setViewItem,"args":(item,)} \
                      for item in self._items[self._entityOne] if item not in self._trade[self._entityOne]]
        self._e1ItemSelect = ScrollSelector((x_pos, y_pos),(self._scrollBoxWidth,self._scrollBoxHeight),30,e1Items,(0,0,0))

        # Trading offer proposed by the entity one
        x_pos = self.getX() + (2*self._spacing) + self._scrollBoxWidth
        e1Offer = [{"text": item.getAttribute("name"),"func": self.setViewItem,"args":(item,)} \
                   for item in self._trade[self._entityOne]]
        self._e1OfferSelect = ScrollSelector((x_pos, y_pos),(self._scrollBoxWidth,self._scrollBoxHeight),30,e1Offer,(0,0,0))

        # Trading offer proposed by the entity two
        x_pos = self.getX() + (6*self._spacing) + (2*self._scrollBoxWidth) + self._itemCardWidth
        e2Offer = [{"text": item.getAttribute("name"),"func": self.setViewItem,"args":(item,)} \
                    for item in self._trade[self._entityTwo]]   
        self._e2OfferSelect = ScrollSelector((x_pos, y_pos),(self._scrollBoxWidth,self._scrollBoxHeight),30,e2Offer,(0,0,0))
        
        # Items in entity two's inventory
        x_pos = self.getX() + (7*self._spacing) + (3*self._scrollBoxWidth) + self._itemCardWidth
        e2Items = [{"text": item.getAttribute("name"),"func": self.setViewItem,"args":(item,)} \
                    for item in self._items[self._entityTwo] if item not in self._trade[self._entityTwo]]
        self._e2ItemSelect = ScrollSelector((x_pos, y_pos),(self._scrollBoxWidth,self._scrollBoxHeight),30,e2Items,(0,0,0))
        
    def draw(self, surface):
        super().draw(surface)
        self._titleText.draw(surface)
        self._e1ItemSelect.draw(surface)
        self._e1OfferSelect.draw(surface)
        self._e2OfferSelect.draw(surface)
        self._e2ItemSelect.draw(surface)
        self._e1InvText.draw(surface)
        self._e2InvText.draw(surface)
        self._e1OfferText.draw(surface)
        self._e2OfferText.draw(surface)
        self._itemCard.draw(surface)
        self._spriteOne.draw(surface)
        self._spriteTwo.draw(surface)
        self._entityOneIncrementer.draw(surface)
        self._entityTwoIncrementer.draw(surface)
        self._tb1.draw(surface)
        self._tb2.draw(surface)
        
        x_pos = ((self._e1OfferSelect.getX() + self._e1OfferSelect.getWidth()) + \
                self._itemCard.getX()) // 2
        pygame.draw.line(surface, (82,20,0), (x_pos,self.getY()),
                         (x_pos,self.getY()+self.getHeight()-1),2)

        x_pos = ((self._e2OfferSelect.getX() + self._itemCard.getWidth()) + \
        self._itemCard.getX()) // 2
        pygame.draw.line(surface, (82,20,0), (x_pos,self.getY()),
                         (x_pos,self.getY()+self.getHeight()-1),2)

        self._cancelButton.draw(surface)
        self._proposeTradeButton.draw(surface)
        
        if self._viewItem != None:
            self._moveItemButton.draw(surface)
        
    def handleEvent(self, event):
        self._e1ItemSelect.handleEvent(event)
        self._e1OfferSelect.handleEvent(event)
        self._e2OfferSelect.handleEvent(event)
        self._e2ItemSelect.handleEvent(event)
        self._entityOneIncrementer.handleEvent(event)
        self._entityTwoIncrementer.handleEvent(event)
        self._cancelButton.handleEvent(event, self.cancelTrade)
        self._proposeTradeButton.handleEvent(event, self.proposeTrade)

        if self._viewItem != None:
            self._moveItemButton.handleEvent(event, self.moveItem)

        if type(self._itemCard) == ScrollBox:
            self._itemCard.move(event)

    def proposeTrade(self):
        ##ADD LOGIC THAT PREVENTS ENTITIES FOR TRADING##
        ##FOR MORE ITEMS THAN THEY CAN HOLD##
        if True: # Add trade logic
            self.executeTrade()
        self.close()

    def executeTrade(self):

        # Transfer the traded items
        for item in self._trade[self._entityOne]:
            self._entityOne.getInventory().removeItem(item)
            self._entityTwo.getInventory().addItem(item)
            item.setOwner(self._entityTwo)
        for item in self._trade[self._entityTwo]:
            self._entityTwo.getInventory().removeItem(item)
            self._entityOne.getInventory().addItem(item)
            item.setOwner(self._entityOne)

        # Transfer the traded acorns
        e1a = int(self._entityOneIncrementer.getValue())
        e2a = int(self._entityTwoIncrementer.getValue())
        e1Acorns = (self._entityOne.getAcorns() - e1a) + e2a
        e2Acorns = (self._entityTwo.getAcorns() - e2a) + e1a
        self._entityOne.setAcorns(e1Acorns)
        self._entityTwo.setAcorns(e2Acorns)
        
        
        

    def cancelTrade(self):
        self.close()

    def moveItem(self):
        owner = self._viewItem.getAttribute("owner")
        if self._viewItem in self._trade[owner]:
            self.removeItemFromTrade(owner, self._viewItem)
        else:
            self.addItemToTrade(owner, self._viewItem)
        self._viewItem = None
        self._itemCard = self._itemCard = MySurface(pygame.Surface((self._itemCardWidth, self._itemCardWidth)),
                                   self._itemCard.getPosition())

    def updateElementPositions(self):

        self._itemCardWidth = 200

        self._scrollBoxWidth = 150
        self._maxSpriteWidth = 50
        self._scrollBoxHeight = 175
        self._spacing = (self._width - self._itemCardWidth - \
                         (4*self._scrollBoxWidth)) // 8

         # Create the title for the trade menu
        titleFont = pygame.font.SysFont("Times New Roman", 28)
        titleBoxYPos = 10 + self.getY()
        self._titleText = TextBox("Trade Negotiation", (100,titleBoxYPos),
                                  titleFont, (0,0,0))

        # Create sprites for the traders
        spritePadding_h = 10
        spritePadding_v = (self._titleText.getY() + self._titleText.getHeight())//4#8
        maxSpriteHeight = 75
        self._spriteOne = MySurface(self._entityOne.getDefaultImage())
        self._spriteTwo = MySurface(pygame.transform.flip(self._entityTwo.getDefaultImage(), True, False))

        sprite_y = ((maxSpriteHeight//2) - (self._spriteOne.getHeight()//2)) + self.getY() + spritePadding_v
        sprite_x = self._spacing + self.getX()
        self._spriteOne.setPosition((sprite_x, sprite_y))

        sprite_y = ((maxSpriteHeight//2) - (self._spriteTwo.getHeight()//2)) + self.getY() + spritePadding_v
        sprite_x = ((self.getWidth() - self._spacing) - self._spriteTwo.getWidth()) + self.getX()
        self._spriteTwo.setPosition((sprite_x, sprite_y))

        # Find the y-positioning of the acorn trade displays
        y_pos = max(self._spriteOne.getHeight(), self._spriteTwo.getHeight()) + self._spriteOne.getY() + 10
        self._entityOneIncrementer.setPosition((0, y_pos))
        self._entityTwoIncrementer.setPosition((0, y_pos))
        

        # Create labels for the different scroll selectors
        font = pygame.font.SysFont("Times New Roman", 20)
        self._textBoxYPos = self._entityOneIncrementer.getY() + self._entityOneIncrementer.getHeight() + 10
        
        self._e1InvText = MultiLineTextBox(self._entityOne.getName() + "'s Items", (100,self._textBoxYPos),
                                           font, (0,0,0), padding = (5,5), antialias=False)
        self._e2InvText = MultiLineTextBox(self._entityTwo.getName() + "'s Items", (100,self._textBoxYPos),
                                           font, (0,0,0), padding = (5,5), antialias=False)
        self._e1OfferText = MultiLineTextBox(self._entityOne.getName() + "'s Trade", (100,self._textBoxYPos),
                                             font, (0,0,0), padding = (5,5), antialias=False)
        self._e2OfferText = MultiLineTextBox(self._entityTwo.getName() + "'s Trade", (100,self._textBoxYPos),
                                             font, (0,0,0), padding = (5,5), antialias=False)

        acornFont = pygame.font.SysFont("Times New Roman", 18)
        self._tb1 = TextBox("Acorns to Trade:", (0,0), acornFont, (0,0,0))
        self._tb2 = TextBox("Acorns to Trade:", (0,0), acornFont, (0,0,0))

        self.updateTradeDisplay()

        itemCardPadding_v = 10
        self._itemCard = MySurface(pygame.Surface((self._itemCardWidth, self._itemCardWidth)),
                                   (0,self._titleText.getHeight()+self._titleText.getY() + itemCardPadding_v))
        self._itemCard.center(cen_point=(1/2,None))

        buttonFont = pygame.font.SysFont("Times New Roman", 18)
        
        button_y = self._itemCard.getHeight() + self._itemCard.getY() + 20
        self._moveItemButton = Button("Add Item To Trade",(0,button_y),buttonFont,
                                      fontColor=(255,255,255),
                                      backgroundColor=(34,67,120),
                                      dims=(210,35),
                                      borderWidth=3,
                                      borderColor=self.shiftRGBValues((34,67,120), (-30,-30,-30)))
        self._moveItemButton.center(self._itemCard, (1/2,None), True)

        button_y = ((self.getHeight() - 35) - 15) + self.getY()
        self._proposeTradeButton = Button("Propose Trade",(0,button_y),buttonFont,
                                          fontColor=(255,255,255),
                                          backgroundColor=(25,130,30),
                                          dims=(120,35),
                                          borderWidth=3,
                                          borderColor=self.shiftRGBValues((25,130,30), (-30,-30,-30)))
        self._cancelButton = Button("Cancel Trade",(0,button_y),buttonFont,
                                    fontColor=(255,255,255),
                                    backgroundColor=(255,0,0),
                                    dims=(110,35),
                                    borderWidth=3,
                                    borderColor=self.shiftRGBValues((255,0,0), (-30,-30,-30)))
        
        self._proposeTradeButton.center(self._itemCard, (1/5,None), True)
        self._cancelButton.center(self._itemCard, (4/5,None), True)
        

        # Center the title
        self._titleText.center(surface=self, cen_point=(1/2,None), multisprite=True)

        # Center labels on the scroll selectors
        self._e1InvText.center(surface=self._e1ItemSelect, cen_point=(1/2, None), multisprite=True)
        self._e2InvText.center(surface=self._e2ItemSelect, cen_point=(1/2, None), multisprite=True)
        self._e1OfferText.center(surface=self._e1OfferSelect, cen_point=(1/2, None), multisprite=True)
        self._e2OfferText.center(surface=self._e2OfferSelect, cen_point=(1/2, None), multisprite=True)

        # Center the incrementers
        self._entityOneIncrementer.center(self._e1OfferSelect, (1/3,None), True)
        self._entityTwoIncrementer.center(self._e2ItemSelect, (1/3,None), True)

        # Position the acorn texts
        self._tb1.center(self._entityOneIncrementer, (None, 1/2), True)
        self._tb2.center(self._entityTwoIncrementer, (None, 1/2), True)
        self._tb1.center(self._e1ItemSelect, (1/3,None), True)
        self._tb2.center(self._e2OfferSelect, (1/3,None), True)

    def center(self, surface=None, cen_point=(1/2,1/2), multisprite=False):
        super().center(surface, cen_point, multisprite)
        self.updateElementPositions()
