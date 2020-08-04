
import pygame
from polybius.graphics import AbstractGraphic, ScrollSelector, MultiLineTextBox, MySurface, TextBox

class TradeMenu(AbstractGraphic):

    def __init__(self, pos, dimensions, entityOne, entityTwo, tradable):
        
        AbstractGraphic.__init__(self, pos)

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

        self.updateElementPositions()

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
        e1Items = [{"text": item.getAttribute("name"),"func": self.addItemToTrade,"args":(self._entityOne, item)} \
                      for item in self._items[self._entityOne] if item not in self._trade[self._entityOne]]
        self._e1ItemSelect = ScrollSelector((x_pos, y_pos),(self._scrollBoxWidth,self._scrollBoxHeight),30,e1Items,(0,0,0))

        # Trading offer proposed by the entity one
        x_pos = self.getX() + (2*self._spacing) + self._scrollBoxWidth
        e1Offer = [{"text": item.getAttribute("name"),"func": self.removeItemFromTrade,"args":(self._entityOne, item)} \
                   for item in self._trade[self._entityOne]]
        self._e1OfferSelect = ScrollSelector((x_pos, y_pos),(self._scrollBoxWidth,self._scrollBoxHeight),30,e1Offer,(0,0,0))

        # Trading offer proposed by the entity two
        x_pos = self.getX() + (6*self._spacing) + (2*self._scrollBoxWidth) + self._itemCardWidth
        e2Offer = [{"text": item.getAttribute("name"),"func": self.removeItemFromTrade,"args":(self._entityTwo, item)} \
                    for item in self._trade[self._entityTwo]]   
        self._e2OfferSelect = ScrollSelector((x_pos, y_pos),(self._scrollBoxWidth,self._scrollBoxHeight),30,e2Offer,(0,0,0))
        
        # Items in entity two's inventory
        x_pos = self.getX() + (7*self._spacing) + (3*self._scrollBoxWidth) + self._itemCardWidth
        e2Items = [{"text": item.getAttribute("name"),"func": self.addItemToTrade,"args":(self._entityTwo, item)} \
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
        
    def handleEvent(self, event):
        self._e1ItemSelect.handleEvent(event)
        self._e1OfferSelect.handleEvent(event)
        self._e2OfferSelect.handleEvent(event)
        self._e2ItemSelect.handleEvent(event)

    def updateElementPositions(self):

        self._itemCardWidth = 200

        self._scrollBoxWidth = 150
        self._maxSpriteWidth = 50
        self._scrollBoxHeight = 150
        self._spacing = (self._width - self._itemCardWidth - \
                         (4*self._scrollBoxWidth)) // 8

         # Create the title for the trade menu
        titleFont = pygame.font.SysFont("Times New Roman", 26)
        titleBoxYPos = 10 + self.getY()
        self._titleText = TextBox("Trade Negotiation", (100,titleBoxYPos),
                                  titleFont, (0,0,0))

        # Create sprites for the traders
        spritePadding_h = 10
        spritePadding_v = 8
        maxSpriteHeight = 75
        self._spriteOne = MySurface(self._entityOne.getDefaultImage())
        self._spriteTwo = MySurface(pygame.transform.flip(self._entityTwo.getDefaultImage(), True, False))

        sprite_y = ((maxSpriteHeight//2) - (self._spriteOne.getHeight()//2)) + self.getY() + spritePadding_v
        sprite_x = self.getX() + ((self._scrollBoxWidth + (self._spacing)) - (self._spriteOne.getWidth()//2))
        self._spriteOne.setPosition((sprite_x, sprite_y))

        sprite_y = ((maxSpriteHeight//2) - (self._spriteTwo.getHeight()//2)) + self.getY() + spritePadding_v
        sprite_x = self.getX() + (((3*self._scrollBoxWidth) + (7*self._spacing) + self._itemCardWidth) - \
                                  (self._spriteOne.getWidth()//2))
##        sprite_x = self.getX() + (self.getWidth() - self._maxSpriteWidth) + \
##                   (self._maxSpriteWidth//2 - self._spriteTwo.getWidth()//2)  - spritePadding_h
        self._spriteTwo.setPosition((sprite_x, sprite_y))
        

        # Create labels for the different scroll selectors
        font = pygame.font.SysFont("Times New Roman", 20)
        self._textBoxYPos = max(self._spriteOne.getHeight(), self._spriteTwo.getHeight()) + self.getY()
        
        self._e1InvText = MultiLineTextBox(self._entityOne.getName() + "'s Items", (100,self._textBoxYPos),
                                           font, (0,0,0), padding = (5,5), antialias=False)
        self._e2InvText = MultiLineTextBox(self._entityTwo.getName() + "'s Items", (100,self._textBoxYPos),
                                           font, (0,0,0), padding = (5,5), antialias=False)
        self._e1OfferText = MultiLineTextBox(self._entityOne.getName() + "'s Trade", (100,self._textBoxYPos),
                                             font, (0,0,0), padding = (5,5), antialias=False)
        self._e2OfferText = MultiLineTextBox(self._entityTwo.getName() + "'s Trade", (100,self._textBoxYPos),
                                             font, (0,0,0), padding = (5,5), antialias=False)

        self.updateTradeDisplay()

        itemCardPadding_v = 10
        self._itemCard = MySurface(pygame.Surface((self._itemCardWidth, self._itemCardWidth)),
                                   (0,self._titleText.getHeight()+self._titleText.getY() + itemCardPadding_v))
        self._itemCard.center(cen_point=(1/2,None))

        # Center the title
        self._titleText.center(surface=self, cen_point=(1/2,None), multisprite=True)

        # Center labels on the scroll selectors
        self._e1InvText.center(surface=self._e1ItemSelect, cen_point=(1/2, None), multisprite=True)
        self._e2InvText.center(surface=self._e2ItemSelect, cen_point=(1/2, None), multisprite=True)
        self._e1OfferText.center(surface=self._e1OfferSelect, cen_point=(1/2, None), multisprite=True)
        self._e2OfferText.center(surface=self._e2OfferSelect, cen_point=(1/2, None), multisprite=True)

    def center(self, surface=None, cen_point=(1/2,1/2), multisprite=False):
        super().center(surface, cen_point, multisprite)
        self.updateElementPositions()
