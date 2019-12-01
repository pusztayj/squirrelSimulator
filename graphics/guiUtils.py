"""
Author: Trevor Stalnaker, Justin Pusztay
File: guiUtils

A file containing various utility functions for the creation
of GUIs
"""
from graphics.mysurface import MySurface
from graphics.textbox import TextBox
from graphics.scrollbox import ScrollBox
from animals.animal import Animal
from items.item import Item
import pygame, copy

def makeMultiLineTextBox(text, position, font, color, backgroundColor):
    """
    Used to create multiline text boxes which are not native to
    pygame.  The user supplies the same information to this function
    that they would supplied to the TextBox Class. The function will
    split the text along new-lines and return a MySurface object
    containing all of the text formatted as desired.
    """
    lines = text.split("\n")
    width = TextBox(max(lines, key=len),position, font, color).getWidth() + 10
    height = font.get_height()
    surf = pygame.Surface((width,height*len(lines)))
    surf.fill(backgroundColor)
    p = (0,0)
    for line in lines:
        t = TextBox(line, p, font, color)
        center = width // 2 - t.getWidth() // 2
        t.setPosition((center, t.getY()))
        t.draw(surf)
        p = (0, p[1] + height)
    return MySurface(surf, position)


def getInfoCard(animal, position,scrollBoxSize = (200,300)):
    """
    Most likely an obsolete function. However, not sure. JKP.
    """
    nameFont = pygame.font.SysFont("Times New Roman", 32)
    detailsFont = pygame.font.SysFont("Times New Roman", 16)
    s = pygame.Surface((200,600))
    s.fill((0,0,0))
    a = copy.copy(animal)
    a.setPosition((10,50))
    if a.isFlipped():
        a.flip()
    TextBox(a.getName(), (10,10), nameFont, (255,255,255)).draw(s)
    if issubclass(type(animal), Animal): 
        a.draw(s)
    makeMultiLineTextBox(str(a), (10,200), detailsFont,
                         (255,255,255), (0,0,0)).draw(s)
    s = MySurface(s)
    return ScrollBox(position, scrollBoxSize, s, borderWidth=2)

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
        s = pygame.Surface((200,600))
        s.fill((0,0,0))
        a = copy.copy(entity)
        a.setWorldBound(False)
        a.setPosition((10,50))
        if a.isFlipped():
            a.flip()
        a.scale(4)
        TextBox(a.getName(), (10,10), nameFont, (255,255,255)).draw(s)
##        if issubclass(type(entity), Animal) or issubclass(type(entity), Item): 
        a.draw(s)
        makeMultiLineTextBox(str(a), (10,200), detailsFont,
                             (255,255,255), (0,0,0)).draw(s)
        s = MySurface(s)
        return ScrollBox(position, scrollBoxSize, s, borderWidth=2)
