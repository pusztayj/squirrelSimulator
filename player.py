from animals.squirrel import Squirrel
from modules.vector2D import Vector2
import rectmanager
import pygame
from stateMachines import playerFSM
from modules.soundManager import SoundManager


class Player(Squirrel):

    def __init__(self, name="", pos=(0,0)):
        super().__init__(name, pos)

        self._acorns = 0

        #Stats that effect Squirrel movement     
        self._diggingSkill = 1
        self._canFly = False

        #Nut storage stats     
        self._memory = 3
        self._cheekCapacity = 50
        self._burrowingSkill = None

        #Other stats
        self._sight = None
        self._luck = None
        self._charisma = 1
        self._stealth = 1
        self._xp = 0

        self._strength = 12

        self._minYPos = 0 

        self._velocity = Vector2(0,0)
        self._maxVelocity = 100
        self._acceleration = 0.5
        self._movement = {pygame.K_w:False,
                          pygame.K_s:False,
                          pygame.K_a:False,
                          pygame.K_d:False}

        self._fsm = playerFSM

        self._digTime = 1
        self._digClock = self._digTime

        self._eatTime = .5
        self._eatClock = self._eatTime

    def getXP(self):
        return self._xp

    def getAcorns(self):
        return self._acorns

    def setAcorns(self, acorns):
        self._acorns = acorns

    def getCheekCapacity(self):
        return self._cheekCapacity

    def setCheekCapacity(self, capacity):
        self._cheekCapacity = capacity

    def getMemory(self):
        return self._memory

    def getCharisma(self):
        return self._charisma

    def getDiggingSkill(self):
        return self._diggingSkill

    def getStealth(self):
        return self._stealth

    def setMemory(self, amount):
        self._memory = amount
        
    def setCharisma(self, amount):
        self._charisma = amount

    def setDiggingSkill(self, amount):
        self._diggingSkill = amount

    def setStealth(self, amount):
        self._stealth = amount

    def eatAcorn(self):
        if self._fsm.getCurrentState() != "eating":
            if self._acorns > 0 and self._hunger < self._baseHunger:
                self._acorns -= 1
                self.increaseHunger()
                self._fsm.changeState("eat")
                SoundManager.getInstance().playSound("munch.ogg")
            elif self._acorns > 0 and self._hunger == self._baseHunger and \
                 self._health < self._baseHealth:
                self._acorns -= 1
                self.heal(1)
                self._fsm.changeState("eat")
                SoundManager.getInstance().playSound("munch.ogg")

    def eat(self, hungerAmount, healthAmount):
        self.increaseHunger(hungerAmount)
        self.heal(healthAmount)
        self._fsm.changeState("eat")
        SoundManager.getInstance().playSound("munch.ogg")

    def move(self, event, atm=None):
        """
        Given an event, changes the appropriate value
        in _movement, if necessary.
        """
        if event.type == pygame.KEYDOWN:
            self._movement[event.key] = True
        elif event.type == pygame.KEYUP:
            self._movement[event.key] = False
        if event.type == pygame.KEYDOWN and event.key==pygame.K_SPACE and \
           (atm == None or not atm.getDisplay()):
            self.eatAcorn()
##        if event.type == pygame.KEYDOWN and event.key==pygame.K_b:
##            self._fsm.changeState("bury")

    def update(self, worldInfo, ticks):
        """Updates the position of the star"""

        if self._fsm.getCurrentState() == "digging":
            self._row = 1
            self._nFrames = 2
            self.updateAnimation(ticks)
            self._digClock -= ticks
            if self._digClock <= 0:
                self._fsm.changeState("done")
                self._digClock = self._digTime
        elif self._fsm.getCurrentState() == "walking":
            if abs(self._velocity.y) > abs(self._velocity.x):
                if self._velocity.y > 0:
                    self._row = 4
                else:
                    self._row = 3
            else:
                self._row = 0
            self._nFrames = 4
            self.updateAnimation(ticks)
        elif self._fsm.getCurrentState() == "standing":
            self._row = 0
            self._nFrames = 1
            self.updateAnimation(ticks)
        elif self._fsm.getCurrentState() == "eating":
            self._row = 2
            self._nFrames = 2
            self._eatClock -= ticks
            self.updateAnimation(ticks)
            if self._eatClock <= 0:
                self._fsm.changeState("done")
                self._eatClock = self._eatTime

        if self._fsm.getCurrentState() == "digging" or \
           self._fsm.getCurrentState() == "eating":
            self._velocity.x = 0
            self._velocity.y = 0
        else:
            #Update the velocity of the star based on the keyboard inputs
            if self._movement[pygame.K_w]:
                self._velocity.y = -self._maxVelocity
                self._fsm.changeState("walk")
            elif self._movement[pygame.K_s]:
                self._velocity.y = self._maxVelocity
                self._fsm.changeState("walk")
            else:
                self._velocity.y = 0
                
            if self._movement[pygame.K_a]:
                self._velocity.x = -self._maxVelocity
                self._fsm.changeState("walk")
                if not self.isFlipped():
                    self.flip()
            elif self._movement[pygame.K_d]:
                self._velocity.x = self._maxVelocity
                self._fsm.changeState("walk")
                if self.isFlipped():
                    self.flip()
            else:
                self._velocity.x = 0

            if self._velocity.x==0 and self._velocity.y==0:
                self._fsm.changeState("stop")

            #If the current velocity exceeds the maximum, scale it down
            if self._velocity.magnitude() > self._maxVelocity:
                self._velocity.scale(self._maxVelocity)

        #Update the position of the star based on its current velocity and ticks
        newPosition = self._position + (self._velocity * ticks)
        if newPosition[0] < 0 or \
           (newPosition[0] + self.getWidth()) > worldInfo[0]:
           self._velocity[0] = 0
        if newPosition[1] < self._minYPos or \
           (newPosition[1] + self.getHeight()) > worldInfo[1]:
           self._velocity[1] = 0
        self._position += (self._velocity * ticks)
        
