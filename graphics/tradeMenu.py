
import pygame
from polybius.graphics import AbstractGraphic, ScrollSelector, MultiLineTextBox

class TradeMenu(AbstractGraphic):

    def __init__(self, pos, dimensions, entityOne, entityTwo, tradable):
        
        AbstractGraphic.__init__(self, pos)

        self._image = pygame.Surface(dimensions)
        self._image.fill((139,79,59))

        self._trade = {entityOne:[], entityTwo:[]}
        self._entityOne = entityOne
        self._entityTwo = entityTwo

        if entityOne == tradable.getAttribute("owner"):
            self._trade[entityOne].append(tradable)
        if entityTwo == tradable.getAttribute("owner"):
            self._trade[entityTwo].append(tradable)

        self.updateTradeDisplay() 

        # Create labels for the different scroll selectors
        font = pygame.font.SysFont("Times New Roman", 22)
        
        self._e1InvText = MultiLineTextBox(entityOne.getName() + "'s\nInventory", (100,30), font, (0,0,0), padding = (5,5))
        self._e1InvText.center(surface=self._e1ItemSelect, cen_point=(1/2, None), multisprite=True)

        self._e2InvText = MultiLineTextBox(entityTwo.getName() + "'s\nInventory", (100,30), font, (0,0,0), padding = (5,5))
        self._e2InvText.center(surface=self._e2ItemSelect, cen_point=(1/2, None), multisprite=True)

        self._e1OfferText = MultiLineTextBox(entityOne.getName() + "'s\nTrade", (100,30), font, (0,0,0), padding = (5,5))
        self._e1OfferText.center(surface=self._e1OfferSelect, cen_point=(1/2, None), multisprite=True)

        self._e2OfferText = MultiLineTextBox(entityTwo.getName() + "'s\nTrade", (100,30), font, (0,0,0), padding = (5,5))
        self._e2OfferText.center(surface=self._e2OfferSelect, cen_point=(1/2, None), multisprite=True)

          

    def addItemToTrade(self,entity,item):
        self._trade[entity].append(item)
        self.updateTradeDisplay()
    
    def removeItemFromTrade(self,entity,item):
        self._trade[entity].remove(item)
        self.updateTradeDisplay()

    def updateTradeDisplay(self):

        # Items in entity one's inventory
        e1Items = [{"text": item.getAttribute("name"),"func": self.addItemToTrade,"args":(self._entityOne, item)} \
                      for item in self._entityOne.getInventory() if item not in self._trade[self._entityOne]]
        self._e1ItemSelect = ScrollSelector((100,100),(200,300),30,e1Items,(0,0,0))

        # Trading offer proposed by the entity one
        e1Offer = [{"text": item.getAttribute("name"),"func": self.removeItemFromTrade,"args":(self._entityOne, item)} \
                   for item in self._trade[self._entityOne]]
        self._e1OfferSelect = ScrollSelector((320,100),(200,300),30,e1Offer,(0,0,0))

        # Trading offer proposed by the entity two
        e2Offer = [{"text": item.getAttribute("name"),"func": self.removeItemFromTrade,"args":(self._entityTwo, item)} \
                    for item in self._trade[self._entityTwo]]   
        self._e2OfferSelect = ScrollSelector((540,100),(200,300),30,e2Offer,(0,0,0))
        
        # Items in entity two's inventory
        e2Items = [{"text": item.getAttribute("name"),"func": self.addItemToTrade,"args":(self._entityTwo, item)} \
                    for item in self._entityTwo.getInventory() if item not in self._trade[self._entityTwo]]
        self._e2ItemSelect = ScrollSelector((760,100),(200,300),30,e2Items,(0,0,0))
        
    def draw(self, surface):
        super().draw(surface)
        self._e1ItemSelect.draw(surface)
        self._e1OfferSelect.draw(surface)
        self._e2OfferSelect.draw(surface)
        self._e2ItemSelect.draw(surface)
        self._e1InvText.draw(surface)
        self._e2InvText.draw(surface)
        self._e1OfferText.draw(surface)
        self._e2OfferText.draw(surface)
        

    def handleEvent(self, event):
        self._e1ItemSelect.handleEvent(event)
        self._e1OfferSelect.handleEvent(event)
        self._e2OfferSelect.handleEvent(event)
        self._e2ItemSelect.handleEvent(event)
