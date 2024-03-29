"""
@author: Trevor Stalnaker, Justin Pusztay

In this file we define the player class which holds all specific
data points that are fundamental for the player. 
"""


from animals.squirrel import Squirrel
from polybius.utils import Vector2, Timer
import pygame
from stateMachines import playerFSM
from polybius.managers import SOUNDS, CONTROLS


class Player(Squirrel):

    def __init__(self, name="", pos=(0,0)):
        """
        Here we intialize the player along with the starting stats that
        every player gets at the start of the game.
        """
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
        self._movement = {CONTROLS.get("walk_up").getKey():False,
                          CONTROLS.get("walk_left").getKey():False,
                          CONTROLS.get("walk_down").getKey():False,
                          CONTROLS.get("walk_right").getKey():False}

        self._fsm = playerFSM

        self._digTimer = Timer(1)
        self._eatTimer = Timer(0.5)

    def getXP(self):
        """
        Returns XP of the player
        """
        return self._xp

    def addXP(self, amount):
        """Add XP to the player's total"""
        self._xp += amount

    def getAcorns(self):
        """Returns the acorns of the player."""
        return self._acorns

    def setAcorns(self, acorns):
        """Sets the acorns of the players."""
        self._acorns = acorns

    def addAcorns(self, amount):
        """Add acorns to the player's total"""
        self._acorns += amount

    def getCheekCapacity(self):
        """Returns the cheek capacity."""
        return self._cheekCapacity

    def setCheekCapacity(self, capacity):
        """Sets the cheek capacity of the player."""
        self._cheekCapacity = capacity

    def getAvailableCheekSpace(self):
        """Return the available cheek space of the player"""
        return self.getCheekCapacity() - self.getAcorns()

    def getMemory(self):
        """Returns the memory of the player."""
        return self._memory

    def getCharisma(self):
        """Returns the charism of the player."""
        return self._charisma

    def getDiggingSkill(self):
        """Returns the digging skill of the player."""
        return self._diggingSkill

    def getStealth(self):
        """Returns the stealth of the player."""
        return self._stealth

    def setMemory(self, amount):
        """Sets the memory of the player."""
        self._memory = amount
        
    def setCharisma(self, amount):
        """Sets the charism of the player."""
        self._charisma = amount

    def setDiggingSkill(self, amount):
        """Sets the digging skill of the player."""
        self._diggingSkill = amount

    def setStealth(self, amount):
        """Sets the stealth."""
        self._stealth = amount

    def eatAcorn(self):
        """
        In this method we eat an acorn and properly change the acorn stash
        and hunger of the player. Also heals the player by 1HP if health bar
        is full. 
        """
        if self._fsm.getCurrentState() != "eating":
            if self._acorns > 0 and self._hunger < self._baseHunger:
                self._acorns -= 1
                self.increaseHunger()
                self._fsm.changeState("eat")
                SOUNDS.playSound("munch.ogg")
            elif self._acorns > 0 and self._hunger == self._baseHunger and \
                 self._health < self._baseHealth:
                self._acorns -= 1
                self.heal(1)
                self._fsm.changeState("eat")
                SOUNDS.playSound("munch.ogg")

    def eat(self, hungerAmount, healthAmount):
        """
        This runs the sound effect for the munch noise. 
        """
        self.increaseHunger(hungerAmount)
        self.heal(healthAmount)
        self._fsm.changeState("eat")
        SOUNDS.playSound("munch.ogg")

    def move(self, event, atm=None):
        """
        Given an event, changes the appropriate value
        in _movement, if necessary.
        """
        if event.type == pygame.KEYDOWN:
            self._movement[event.key] = True
        elif event.type == pygame.KEYUP:
            self._movement[event.key] = False
        if CONTROLS.get("eat").check(event):
            self.eatAcorn()

    def stop(self):
        for k in self._movement.keys(): self._movement[k] = False

    def changeStateToDone(self):
        self._fsm.changeState("done")

    def animateDig(self, ticks):
        self._row = 1
        self._nFrames = 2
        self.updateAnimation(ticks)
        self._digTimer.update(ticks, self.changeStateToDone)

    def animateWalk(self, ticks):
        vel = self._velocity
        movingVertically = abs(vel.y) > abs(vel.x)
        if movingVertically:
            if self._velocity.y > 0:
                self._row = 4
            else:
                self._row = 3
        else:
            self._row = 0
        self._nFrames = 4
        self.updateAnimation(ticks)

    def animateStanding(self, ticks):
        self._row = 0
        self._nFrames = 1
        self.updateAnimation(ticks)

    def animateEating(self, ticks):
        self._row = 2
        self._nFrames = 2
        self.updateAnimation(ticks)
        self._eatTimer.update(ticks, self.changeStateToDone)

    def manageAnimations(self, ticks):
        if self._fsm.getCurrentState() == "digging":
            self.animateDig(ticks)
        elif self._fsm.getCurrentState() == "walking":
            self.animateWalk(ticks)
        elif self._fsm.getCurrentState() == "standing":
            self.animateStanding(ticks)
        elif self._fsm.getCurrentState() == "eating":
            self.animateEating(ticks)

    def setVerticalMovement(self):
        if self._movement[CONTROLS.get("walk_up").getKey()]:
            self._velocity.y = -self._maxVelocity
            self._fsm.changeState("walk")
        elif self._movement[CONTROLS.get("walk_down").getKey()]:
            self._velocity.y = self._maxVelocity
            self._fsm.changeState("walk")
        else:
            self._velocity.y = 0

    def setHorizontalMovement(self):
        if self._movement[CONTROLS.get("walk_left").getKey()]:
            self._velocity.x = -self._maxVelocity
            self._fsm.changeState("walk")
            if not self.isFlipped():
                self.flip()
        elif self._movement[CONTROLS.get("walk_right").getKey()]:
            self._velocity.x = self._maxVelocity
            self._fsm.changeState("walk")
            if self.isFlipped():
                self.flip()
        else:
            self._velocity.x = 0

    def manageMovement(self):
        if self._fsm.getCurrentState() in ("digging", "eating"):
            self._velocity.x = 0
            self._velocity.y = 0
        else:
            self.setVerticalMovement()
            self.setHorizontalMovement()
            
        if self._velocity.x==0 and self._velocity.y==0:
            self._fsm.changeState("stop")
        self.scaleVelocity()

    def scaleVelocity(self):
        if self._velocity.magnitude() > self._maxVelocity:
            self._velocity.scale(self._maxVelocity)

    def updatePosition(self, ticks, worldInfo):
        newPosition = self._position + (self._velocity * ticks)
        if newPosition[0] < 0 or \
           (newPosition[0] + self.getWidth()) > worldInfo[0]:
           self._velocity[0] = 0
        if newPosition[1] < self._minYPos or \
           (newPosition[1] + self.getHeight()) > worldInfo[1]:
           self._velocity[1] = 0
        self._position += (self._velocity * ticks)
        
    def update(self, worldInfo, ticks):
        """Updates the animation and position of the player"""
        self.manageAnimations(ticks)
        self.manageMovement()
        self.updatePosition(ticks, worldInfo)
        self.manageFoodSpoilage(ticks)
        
        
