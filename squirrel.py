
from animal import Animal
from animated import Animated
from vector2D import Vector2
import pygame

class Squirrel(Animal, Animated):

    def __init__(self):

##        Animal.__init__()
        Animated.__init__(self, "tempSquirrel.png", (0,0))
  
        #Stats that effect Squirrel movement     
        self._diggingSkill = None
        self._canFly = False

        #Nut storage stats     
        self._memory = None
        self._cheekCapacity = None
        self._burrowingSkill = None

        #Other stats
        self._sight = None
        self._luck = None
        self._charisma = None

        self._velocity = Vector2(0,0)
        self._maxVelocity = 100
        self._acceleration = 0.5
        self._movement = {pygame.K_UP:False,
                          pygame.K_DOWN:False,
                          pygame.K_LEFT:False,
                          pygame.K_RIGHT:False}

    def move(self, event):
        """
        Given an event, changes the appropriate value
        in _movement, if necessary.
        """
        if event.type == pygame.KEYDOWN:
            self._movement[event.key] = True
        elif event.type == pygame.KEYUP:
            self._movement[event.key] = False

    def update(self, worldInfo, ticks):
        """Updates the position of the star"""
        
        #Update the velocity of the star based on the keyboard inputs
        if self._movement[pygame.K_UP]:
            self._velocity.y -= self._acceleration
        elif self._movement[pygame.K_DOWN]:
            self._velocity.y += self._acceleration
        elif self._movement[pygame.K_LEFT]:
            self._velocity.x -= self._acceleration
        elif self._movement[pygame.K_RIGHT]:
            self._velocity.x += self._acceleration

        #If the current velocity exceeds the maximum, scale it down
        if self._velocity.magnitude() > self._maxVelocity:
            self._velocity.scale(self._maxVelocity)

        #Update the position of the star based on its current velocity and ticks
        newPosition = self._position + (self._velocity * ticks)
        if newPosition[0] < 0 or \
           (newPosition[0] + self.getWidth()) > worldInfo[0]:
           self._velocity[0] *= -1
        if newPosition[1] < 0 or \
           (newPosition[1] + self.getHeight()) > worldInfo[1]:
           self._velocity[1] *= -1
        self._position += (self._velocity * ticks)

    
        

    
