"""
Author: Trevor Stalnaker
File: guiUtils

A file containing various utility functions for the creation
of GUIs
"""
from mysurface import MySurface
from textbox import TextBox
import pygame

def makeMultiLineTextBox(text, position, font, color):
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
    p = (0,0)
    for line in lines:
        TextBox(line, p, font, color).draw(surf)
        p = (0, p[1] + height)
    return MySurface(surf, position)
        
