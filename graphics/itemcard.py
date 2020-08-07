from polybius.graphics import MySurface, TextBox, ScrollBox, MultiLineTextBox
from items.item import Item
import pygame, copy

class ItemCard(object):

    def __init__(self, item,position = (471,166),scrollBoxSize = (155,300),
                 center=False):
        """
        Creates an item card for the object, this works for both items and GUIs.

        Defaults is set for the merchant GUI which needs to be changed.
        """
        self._item = item
        self._center = center
        self._card = self.generate(item,position,scrollBoxSize)
        

    def getItem(self):
        """
        Returns the item that the item card is representing
        """
        return self._item

    def getCard(self):
        """
        Returns the scorllbox that is the item. 
        """
        return self._card

    def generate(self,entity, position,scrollBoxSize):
        """
        Generates the item that is the in the item card.
        """
        nameFont = pygame.font.SysFont("Times New Roman", 32)
        detailsFont = pygame.font.SysFont("Times New Roman", 16)
        
        a = copy.copy(entity)
        a.setWorldBound(False)
        a.setPosition((10,50))
        if a.isFlipped():
            a.flip()
        a.scale(4)
        name = TextBox(a.getAttribute("name"), (10,10), nameFont, (255,255,255))
        info = MultiLineTextBox(str(a), (10,200), detailsFont,
                             (255,255,255), (0,0,0))

        s_height = name.getHeight() + info.getHeight() + a.getHeight() + 50
        s = pygame.Surface((scrollBoxSize[0],s_height))
        s.fill((0,0,0))
        
        if self._center:
            name.center(s, (1/2, None), False)
            #a.center(s, (1/2, None), False)
            a.setPosition(((scrollBoxSize[0] // 2) - (a.getWidth() // 2), 50))
            info.center(s, (1/2,None), False)
            
        name.draw(s)
        a.draw(s)
        info.draw(s)
        
        s = MySurface(s)
        return ScrollBox(position, scrollBoxSize, s, borderWidth=2)
