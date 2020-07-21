from graphics.mysurface import MySurface
from graphics.textbox import TextBox
from graphics.scrollbox import ScrollBox
from graphics.multilinetextbox import MultiLineTextBox
from items.item import Item
import pygame, copy

class ItemCard(object):

    def __init__(self, item,position = (471,166),scrollBoxSize = (155,300)):
        """
        Creates an item card for the object, this works for both items and GUIs.

        Defaults is set for the merchant GUI which needs to be changed.
        """
        self._item = item
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
        s = pygame.Surface((240,600))
        s.fill((0,0,0))
        a = copy.copy(entity)
        a.setWorldBound(False)
        a.setPosition((10,50))
        if a.isFlipped():
            a.flip()
        a.scale(4)
        TextBox(a.getAttribute("name"), (10,10), nameFont, (255,255,255)).draw(s)
        a.draw(s)
        MultiLineTextBox(str(a), (10,200), detailsFont,
                             (255,255,255), (0,0,0)).draw(s)
        s = MySurface(s)
        return ScrollBox(position, scrollBoxSize, s, borderWidth=2)
