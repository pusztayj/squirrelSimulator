import pygame

class Box(object):

    def __init__(self,position,demensions,color,width):
        """
        Here we create a box. It needs a position and a demension
        to create a box that is not filled in with those demensions.
        You can also input the color and the width (thickness) of the
        lines. 
        """
        self._position = position
        self._demensions = demensions
        self._x = self._demensions[0]
        self._y = self._demensions[1]
        self._width = width
        self._color = color

    def draw(self,screen):
        """
        Will draw the box on the combat minigame gui.
        """ 
        pygame.draw.line(screen,self._color,(self._position[0],self._position[1]),
                         (self._position[0],self._position[1]+self._y),
                         self._width)
        pygame.draw.line(screen,self._color,self._position,
                         (self._position[0]+self._x,self._position[1]),
                         self._width)       
        pygame.draw.line(screen,self._color,(self._position[0],self._position[1]+self._y),
        (self._position[0]+self._x,self._position[1]+self._y),
        self._width)
        pygame.draw.line(screen,self._color,(self._position[0]+self._x,self._position[1]),
                         (self._position[0]+self._x,self._position[1]+self._y),
                         self._width)

    def setPosition(self,newPosition):
        """
        Sets a new position to the box.
        """
        self._position = newPosition
