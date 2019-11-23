
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
                #self._image = copy.copy(self._realImage)
                popup = Popup(self.getName(), (pos[0]+5,pos[1]+5),
                                popupFont)
                popup.draw(screen)
                break

    def healLogic(self,opponents):
        # opponents is a list
        damage = [(x,attackComputation(self,x),x.getHealth())
                  for x in opponents if x!=None]
        # calculates damage done and health an animal has
        attacks = [x for x in damage if x[1] >= x[2]]
        # checks to see if the animal can kill an opponent
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
                  for x in opponents if x!=None]
            #calculates the amount of damage that can be done vs the health
            attacks = [x for x in damage if x[1] <= 5]
            # runs a list comp that calculates if there are any animals that
            # the current animal will do less than 5 damamge against. 
            if len(attacks) == len(opponents):
                # checks to see if it can't do more than 5 damage to an animal
                self._combatStatus = self.getName() + " has fortified!"
                return True
            elif 6 < random.randint(0,9): # 33% random change of fortifying 
                self._combatStatus = self.getName() + " has fortified!"
                return True
            else:
                return False
        else:
            return False

    def attackLogic(self,opponents):
        damage = [(x,attackComputation(self,x),x.getHealth()) \
                  for x in opponents if x!=None]
        kills = [x for x in damage if x[1] >= x[2]] # calculates the kills
        random.shuffle(kills) # shuffles the kill so it's not always the player
        if len(kills) > 0:
            a = kills[0][0]
            self._combatStatus = self.getName() + " has killed " + a.getName()
            return kills[0][0]
        else:
            damage.sort(key = lambda x: x[1]) #could shuffle to make more stupid
            # sorts the damage from lowest to highest
            self._combatStatus = self.getName() + " did " + str(damage[-1][1])+ " damage to " + \
                                 (damage[-1][0]).getName()
            return damage[-1][0] #returns the highest damage animal

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
                self._velocity.x = 0
                self._velocity.y = 0
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

    def followPlayer(self, ticks, target, flank=1):
        follow_x = random.randint(45,55)
        follow_y = random.randint(45,55)
        self._velocity = target._velocity
        if target._velocity.x != 0 or target._velocity.y != 0:
            if abs(self._velocity.y) > abs(self._velocity.x):
                if self._velocity.y > 0:
                    self._nFrames = self._forwardFrames
                    self._row = self._forwardRow
                    if target._position.y < self._position.y + follow_y:
                        self._velocity.y -= target._velocity.y//2
                else:
                    self._nFrames = self._backwardFrames
                    self._row = self._backwardRow
                    if target._position.y > self._position.y - follow_y:
                        self._velocity.y -= target._velocity.y//2
                if flank == 1:
                    if self._position.x + follow_x > target._position.x:
                        self._velocity.x -= follow_x//2
                else:
                    if self._position.x - follow_x < target._position.x:
                        self._velocity.x += follow_x//2
            else:
                if self._velocity.x < 0:
                    if not self.isFlipped():
                        self.flip()
                    if target._position.x > self._position.x - follow_x:
                        self._velocity.x -= target._velocity.x//2
                if self._velocity.x > 0:
                    if self.isFlipped():
                        self.flip()
                    if target._position.x < self._position.x + follow_x:
                        self._velocity.x -= target._velocity.x//2
                if flank == 1:
                    if self._position.y + follow_y > target._position.y:
                        self._velocity.y -= follow_y//2
                else:
                    if self._position.y - follow_y < target._position.y:
                        self._velocity.y += follow_y//2
                        
                self._nFrames = self._walkFrames
                self._row = self._walkRow
            self.updateAnimation(ticks)
        elif target._velocity.x == 0 and target._velocity.y==0:
            self._row = self._standRow
            self._nFrames = self._standFrames
            self.updateAnimation(ticks)
        
        self._position += (self._velocity*ticks)


    def follow(self, ticks, target):
        self._velocity = target._velocity
        if abs(self._velocity.y) > abs(self._velocity.x):
            if self._velocity.y > 0:
                self._nFrames = self._forwardFrames
                self._row = self._forwardRow
            else:
                self._nFrames = self._backwardFrames
                self._row = self._backwardRow
        else:
            if self._velocity.x < 0:
                if not self.isFlipped():
                    self.flip()
            if self._velocity.x > 0:
                if self.isFlipped():
                    self.flip()         
            self._nFrames = self._walkFrames
            self._row = self._walkRow
        if target._velocity.x == 0 and target._velocity.y==0:
            self._row = self._standRow
            self._nFrames = self._standFrames
        self.updateAnimation(ticks)
        self._position += (self._velocity * ticks)
        
