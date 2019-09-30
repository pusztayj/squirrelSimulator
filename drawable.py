"""
Author: Trevor Stalnaker
File Name: drawable.py
Date: 22 September 2019
Project 2

A super class with methods subclasses like Orb and Star inherit from
"""

import pygame
from vector2D import Vector2
from frameManager import FRAMES

class Drawable():

    # Class Variable
    WINDOW_OFFSET = Vector2(0,0)

    @classmethod
    def updateOffset(cls, trackingObject, screenSize, worldSize):
        """
       Calculates the offset for the camera
       """
        Drawable.WINDOW_OFFSET = Vector2(max(0,
                                   min(trackingObject.getX() + \
                                   (trackingObject.getWidth() // 2) - \
                                   (screenSize[0] // 2),
                                    worldSize[0] - screenSize[0])),
                                max(0,
                                    min(trackingObject.getY() + \
                                    (trackingObject.getHeight() // 2) - \
                                    (screenSize[1] // 2),
                                    worldSize[1] - screenSize[1])))
           
    @classmethod
    def adjustMousePos(cls, mousePos):
        """
        Given a mouse position relative to the screen coordinates, this method returns
        the mouse position adjusted to world coordinates using WINDOW_OFFSET
        """
        return Vector2(mousePos[0], mousePos[1]) + Drawable.WINDOW_OFFSET

    def __init__(self, imageName, position, offset=None, worldBound=True):
        """
        Sets up the drawable instance variables. If rect is None, then the entire
        image is used, otherwise the sub-area indicated by rect is used. If transparent
        is true, a color key is set from the pixel at position (0,0), otherwise no
        transparency key is set.
        """
        if imageName != "":
            self._imageName = imageName
            self._image = FRAMES.getFrame(self._imageName, offset)  
        self._position = Vector2(position[0], position[1])
        self._worldBound = worldBound
        self._isFlipped = False

    def getWidth(self):
        """Returns the width of the image surface"""
        return self._image.get_rect().size[0]

    def getHeight(self):
        """Returns the height of the image surface"""
        return self._image.get_rect().size[1]

    def getPosition(self):
        """Returns the current position"""
        return self._position

    def setPosition(self, newPosition):
        """Updates the position of the drawable to a new position"""
        self._position = newPosition

    def getX(self):
        """Returns the x coordinate of the current position"""
        return self._position[0]

    def getY(self):
        """Returns the y coordinate of the current position"""
        return self._position[1]

    def getSize(self):
        """Returns the size of the image surface"""
        return self._image.get_rect().size

    def getCollideRect(self):
        """Returns a Rect variable representing the collision
        area of the current object
        """
        return self._image.get_rect().move(self.getX(), self.getY())

    def draw(self, surface):
        """Draws the orb's image at the current position on the given surface"""
        if self._worldBound:
            (x,y) = Vector2(self._position[0],self._position[1]) - Drawable.WINDOW_OFFSET
        else:
            (x,y) = self._position
        surface.blit(self._image, (x,y))

    def flip(self):
        self._isFlipped = not self._isFlipped
        self._image = pygame.transform.flip(self._image, True, False)

    def isFlipped(self):
        return self._isFlipped
        
     
