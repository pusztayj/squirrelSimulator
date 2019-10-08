"""
Author: Trevor Stalnaker
File: guiUtils

A file containing various utility functions for the creation
of GUIs
"""
from graphics.mysurface import MySurface
from graphics.textbox import TextBox
from graphics.scrollbox import ScrollBox
import pygame, copy

def makeMultiLineTextBox(text, position, font, color, backgroundColor):
    """
    Used to create multiline text boxes which are not native to
    pygame.  The user supplies the same information to this function
    that they would supplied to the TextBox Class. The function will
    split the text along new-lines and return a MySurface object
    containing all of the text formatted as desired.
    """
    width = TextBox(text, position, font, color).getWidth()
    height = font.get_height()
    lines = text.split("\n")
    surf = pygame.Surface((width,height*len(lines)))
    surf.fill(backgroundColor)
    p = (0,0)
    for line in lines:
        TextBox(line, p, font, color).draw(surf)
        p = (0, p[1] + height)
    return MySurface(surf, position)

def getInfoCard(animal, position):
    nameFont = pygame.font.SysFont("Times New Roman", 32)
    detailsFont = pygame.font.SysFont("Times New Roman", 16)
    s = pygame.Surface((500,500))
    s.fill((0,0,0))
    a = copy.copy(animal)
    a.setPosition((10,50))
    if a.isFlipped():
        a.flip()
    TextBox(a.getName(), (10,10), nameFont, (255,255,255)).draw(s)
    a.draw(s)
    makeMultiLineTextBox(str(a), (10,200), detailsFont,
                         (255,255,255), (0,0,0)).draw(s)
    s = MySurface(s)
    return ScrollBox(position, (200,300), s, borderWidth=2)
    
    

    
