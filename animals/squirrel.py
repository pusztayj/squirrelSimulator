
from animal import Animal
from animated import Animated
from vector2D import Vector2
import pygame

class Squirrel(Animal, Animated):

    def __init__(self, name="", pos=(0,0)):

        Animal.__init__(self, name)
        Animated.__init__(self, "tempSquirrel.png", pos)

   

    
        

    
