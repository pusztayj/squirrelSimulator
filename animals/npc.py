
from .animal import Animal
from graphics.popup import Popup
import random, pygame, copy
from items.items import *
from combatUtils import *
from modules.animated import Animated
from modules.vector2D import Vector2
from stateMachines import npcFSM

class NPC(Animal, Animated):

    def __init__(self, name, image, pos, agression, speed, endurance,strength):

        Animated.__init__(self, image, pos)
        
        Animal.__init__(self, name=name,
                         health=100,
                         speed=random.randint(speed[0],speed[1]),
                         endurance=random.randint(endurance[0],endurance[1]),
                         strength = strength)
        
        self._aggressionLevel = agression
        self._combatStatus = ""

        self._fsm = npcFSM
        
        self._velocity = Vector2(0,0)
        self._wanderRange = self.getWidth() * 3
        self._wanderRect= ((pos[0]-self._wanderRange,pos[0]+self._wanderRange),
                           (pos[1]-self._wanderRange,pos[1]+self._wanderRange))

        self._walkTimer = 0
        self._idleTimer = 0

    def getCombatStatus(self):
        return self._combatStatus

    def handleEvent(self, event, screen):     
        popupFont = pygame.font.SysFont("Times New Roman", 16)
        x,y = self.getPosition()
        pos = pygame.mouse.get_pos()
        for rect in self.getCollideRects(): 
            r = rect.move(x,y)
            if r.collidepoint(pos):
                print("yeah")
                #self._image = copy.copy(self._realImage)
                popup = Popup(self.getName(), (pos[0]+5,pos[1]+5),
                                popupFont)
                popup.draw(screen)
                break

    def healLogic(self,opponents):
        # opponents is a list
        damage = [(x,attackComputation(self,x),x.getHealth()) \
                  for x in opponents]
        attacks = [x for x in damage if x[1] >= x[2]]
        if self._health <= 20 and len(attacks) == 0:
            for x in self._inventory:
                if type(x) == type(Potions()) and self._health <= 20:
                    self._combatStatus = self.getName() + "healed with a potion!"
                    return True
                    
            return False
        else:
            return False
        
    def fortifyLogic(self,opponents):
        if self.getHealth() >= 20 and self.getHealth() <= 75:
            damage = [(x,attackComputation(self,x),x.getHealth()) \
                      for x in opponents]
            attacks = [x for x in damage if x[1] <= 5]
            if len(attacks) == len(opponents):
                self._combatStatus = self.getName() + "has fortified!"
                return True
            elif 6 < random.randint(0,9):
                self._combatStatus = self.getName() + "has fortified!"
                return True
            else:
                return False
        else:
            return False

    def attackLogic(self,opponents):
        damage = [(x,attackComputation(self,x),x.getHealth()) \
                  for x in opponents]
        kills = [x for x in damage if x[1] >= x[2]]
        if len(kills) > 0:
            a = kills[0][0]
            self._combatStatus = self.getName() + "has killed " + a.getName()
            return kills[0][0]
        else:
            damage.sort(key = lambda x: x[1])
            self._combatStatus = self.getName() + " did " + str(damage[-1][1])+ " damage to " + \
                                 (damage[-1][0]).getName()
            return damage[-1][0]

    def getWanderRect(self):
        return pygame.Rect(self._wanderRect[0][0], self._wanderRect[1][0],
                           self._wanderRange*2, self._wanderRange*2)

    def wander(self, ticks):

        # Check if done walking
        if self._walkTimer <= 0:
            self._row = self._walkRow
            self._nFrames = self._walkFrames
            # Check if done idleing 
            if self._idleTimer <= 0:
                # Reset the walk cycle
                self._velocity.x = 0
                self._velocity.y = 0
                self._walkTimer = random.randint(1,2)
                w_x = random.randint(self._wanderRect[0][0],self._wanderRect[0][1]) - self._position[0]
                if w_x < 0 and not self.isFlipped():
                    self.flip()
                if w_x > 0 and self.isFlipped():
                    self.flip()
                w_y = random.randint(self._wanderRect[1][0],self._wanderRect[1][1]) - self._position[1]
                self._velocity.x = w_x // self._walkTimer
                self._velocity.y = w_y // self._walkTimer
                
                #If the current velocity exceeds the maximum, scale it down
                if self._velocity.magnitude() > self._maxVelocity:
                    self._velocity.scale(self._maxVelocity)
                    
                # Reset the idle timer
                self._idleTimer = random.randint(1,3)
            # Update to an idle animation
            else:
                self._row = self._standRow
                self._nFrames = self._standFrames
                self._idleTimer -= ticks
                self.updateAnimation(ticks)
        # Update to the wandering animation and update position
        else:
            # Check if the fox is running straight up or down
            if abs(self._velocity.y) > abs(self._velocity.x):
                if self._velocity.y > 0:
                    self._nFrames = self._forwardFrames
                    self._row = self._forwardRow
                else:
                    self._nFrames = self._backwardFrames
                    self._row = self._backwardRow
            else:
                self._nFrames = self._walkFrames
                self._row = self._walkRow
            self._position += (self._velocity*ticks)
            self._walkTimer -= ticks
            self.updateAnimation(ticks)
        
