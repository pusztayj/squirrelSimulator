"""
@authors: Trevor Stalnaker, Justin Pusztay

In this file we create an NPC class. All animal NPCs inherit from this
class where they obtain certain methods such as wandering and friend scores.

We also create methods for how an NPC can be cloned.
"""

from .animal import Animal
from polybius.graphics import Animated, Popup
import random, pygame, copy
from polybius.utils.vector2D import Vector2
from stateMachines import npcFSM

from minigame.combat.utils.combatfunctions import *

class NPC(Animal, Animated):

    def __init__(self, name, image, pos, aggression, speed, endurance,strength):

        Animated.__init__(self, image, pos)
        
        Animal.__init__(self, name=name,
                         health=100,
                         speed=random.randint(speed[0],speed[1]),
                         endurance=random.randint(endurance[0],endurance[1]),
                         strength = strength)

        # The friend score is a metric of how much an
        # NPC likes the player
        self._minFriendScore = 0
        self._maxFriendScore = 100
        self._friendScore = random.randint(10,90)
        
        self._aggressionLevel = min(random.randint(0,100) +
                                    random.randint(aggression[0],aggression[1]),
                                    100)

        self._fsm = npcFSM
        
        self._velocity = Vector2(0,0)
        self._wanderRange = self.getWidth() * 3
        # sets up the wander rect, which is the set of points an NPC can move to.
        self._wanderRect= ((pos[0]-self._wanderRange,pos[0]+self._wanderRange),
                           (pos[1]-self._wanderRange,pos[1]+self._wanderRange))

        self._walkTimer = 0
        self._idleTimer = 0

    def getFriendScore(self):
        """Returns the friend score."""
        return self._friendScore

    def setFriendScore(self, score):
        """Sets the friend score."""
        self._friendScore = score

    def changeFriendScore(self, change):
        """Changes the friend score to a certain modifer."""
        self._friendScore = max(0, min(100, self._friendScore + change))

    def getAggression(self):
        """Returns the aggression stat for the animal"""
        return self._aggressionLevel

    def handleEvent(self, event, screen):
        """Handle events for NPCs"""
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

    def getWanderRect(self):
        """
        This method returns the wander rect. This is the rectangle that the
        NPC can pick points inside of to move to. This is for the main world
        so NPCs can move around on. 

        This is only necessary for a leader of a pack because followers will
        use the follow methods. 
        """
        return pygame.Rect(self._wanderRect[0][0], self._wanderRect[1][0],
                           self._wanderRange*2, self._wanderRange*2)

    def resetWanderRect(self):
        """
        This method resets the wander rect of the NPC.
        """
        posx, posy = self._position
        self._wanderRect= ((round(posx)-self._wanderRange,round(posx)+self._wanderRange),
                           (round(posy)-self._wanderRange,round(posy)+self._wanderRange))

    def wander(self, ticks):
        """
        This method automates the movement of an animal and the animation
        that goes with it.

        Here we pick the points that the animal will moves towards, sets the
        appropriate velocity and computes the appropriate animation that needs
        to be shown. 
        """
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
        """
        This method automates the movement of an NPC with respect to the player
        and the animation that goes with it.

        Here we compute the position that NPC needs to be so that it follows
        the player around. We also compute the appropriate velocity that
        we need based on the player movement. Also updates the appropriate
        animation.
        """
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
        """
        This method automates the movement of an NPC with respect an NPC pack
        leader and the animation that goes with it.

        Here we compute the position that NPC needs to be so that it follows
        the animal around. We also compute the appropriate velocity that we
        need based on the player movement. Also updates the appropriate
        animation.
        """
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


    def move(self,opponents):
        """
        Tests the animal logic so the NPC can decide their move.
        """
        if self.healLogic(opponents):
            potions = [x for x in self.getInventory() if x.getAttribute("type") == "potion"] 
            potions.sort(key = lambda x: x.getHealthBoost())
            if len(potions) != 0:
                heal(self,potions[-1])
        elif self.fortifyLogic(opponents):
            fortify(self)
        else:
            an = self.attackLogic(opponents)
            attack(self,an)

    def clone(self):
        """
        Creates an identical copy of the NPC. 
        """
        pos = self.getPosition()
        c = type(self)(self._species, self.getName(), (round(pos[0]),round(pos[1])))
        c.setAcorns(self.getAcorns())
        c.setFriendScore(self.getFriendScore())
        c.setHealth(self.getHealth())
        c.setHunger(self.getHunger())
        c.setStamina(self.getStamina())
        c.equipArmor(self.getArmor())
        c.equipItem(self.getEquipItem())
        c.setInventory(self.getInventory())
        for item in c.getInventory().getItems():
            if item.getAttribute("owner") == self:
                item.setOwner(c)
        return c

    def borrowItem(self,item,otherCreature):
        """
        Returns boolean based on NPC's logic of wanting
        to borrow an item.
        """
        if not item.isShareable():
            return (False,"Item is not shareable")
        if self.getInventory().hasSpace() == False: # NPC inventory is full so they can't accept
            return (False,str(self.getName())+ " has no room in their inventory") 
        if item.getAttribute("durability") < 20:
            return (False,"Your " + str(item.getAttribute("name")) + "'s durability is too low for " +str(self.getName()))
        if item.getAttribute("utility") < 20:
            return (False,"Your " + str(item.getAttribute("name")) + "'s utility is too low for " +str(self.getName()))
        return (True,str(self.getName()) + " has borrowed the "+str(item.getAttribute("name")))

    def loanItem(self,item,otherCreature):
        """
        Returns boolean based on NPC's logic of wanting
        to loan an item. 
        """
        if not item.isShareable():
            return (False,"Item is not shareable")
        if otherCreature.getInventory().hasSpace() == False: # Other inventory is full so they can't accept
            return (False,"You have no space in your inventory")
        
        inventoryTypes = [x.getAttribute("type") for x in self.getAllItems() if x != None]
        numOfTypes = {x:inventoryTypes.count(x) for x in inventoryTypes}

        if item.getAttribute("item") == "healthPotion": # If health potion don't trade
            return (False, "Health Potions are not loanable")
        
        if item.getAttribute("type") == "food": # If food don't trade
            return (False, "Food is not loanable")
        
        if numOfTypes[item.getAttribute("type")] == 1: # NPC will not trade item if they only have 1 of that type
            return (False,str(self.getName())+ " only has one " + str(item.getAttribute("type")) + " in their inventory")

        return (True,str(self.getName()) + " has loaned the "+ str(item.getAttribute("name")))

    def reclaimItem(self,item,otherCreature):
        """
        Returns boolean based on NPC's logic of wanting
        to reclaim an item.
        """
        if not item.isShareable():
            return (False,"Item is not shareable")
        if otherCreature.getInventory().hasSpace() == False: # NPC inventory is full so they can't accept
            return (False,"You have no space in your inventory")
        return (True,str(self.getName()) + " has reclaimed the "+str(item.getAttribute("name")))

    def giveOwnershipItem(self,item,otherCreature):
        """
        Returns boolean based on NPC's logic of wanting
        to give ownership of an item to someone else.
        """
        if not item.isShareable():
            return (False,"Item is not shareable")
        # NPC inventory is full so they can't accept
        if otherCreature.getInventory().hasSpace() == False and \
           not (item in otherCreature.getAllItems()): 
            return (False,str(self.getName())+ " has no room in their inventory")

        inventoryTypes = [x.getAttribute("type") for x in self.getAllItems() if x != None]
        numOfTypes = {x:inventoryTypes.count(x) for x in inventoryTypes}
        
        if numOfTypes[item.getAttribute("type")] == 1: # NPC will not trade item if they only have 1 of that type
            return (False,str(self.getName())+ " only has one " + str(item.getAttribute("type")) + " in their inventory. They will not give it.")

        if item.getAttribute("durability") > 80:
            return (False,str(self.getName())+ " does not want to give ownership.")
        if item.getAttribute("utility") > 80:
            return (False,str(self.getName())+ " does not want to give ownership.")
        
        return (True,str(self.getName()) + " has given the "+str(item.getAttribute("name")))

    def takeOwnership(self,item,otherCreature):
        """
        Returns boolean based on NPC's logic of wanting
        to take ownership of an item.
        """
        if not item.isShareable():
            return (False,"Item is not shareable")
        # NPC inventory is full so they can't accept
        if self.getInventory().hasSpace() == False and \
           not (item in self.getInventory().getItems()): 
            return (False,str(self.getName())+ " has no room in their inventory")
        return (True, ("%s has taken ownership of the item" % self.getName()))

    def manageState(self):
        self.manageHunger()
        self.manageEquippedItems()
        self.manageHealthRestoreItems()

    def manageEquippedItems(self):
        bestWeapon = None
        bestArmor = None
        # Find the best armor and weapons
        for i in self.getAllItems():
            if i.getAttribute("holdable"):
                if bestWeapon == None:
                    bestWeapon = i
                else:
                    itemStrength = i.getAttribute("strength")
                    bestStrength = bestWeapon.getAttribute("strength")
                    if itemStrength > bestStrength:
                        bestWeapon = i
            elif i.getAttribute("type") == "armor":
                if bestArmor == None:
                    bestArmor = i
                else:
                    itemStrength = i.getAttribute("strength")
                    bestStrength = bestArmor.getAttribute("strength")
                    if itemStrength > bestStrength:
                        bestArmor = i             
        if bestWeapon != None:
            if not self.isEquipped():
                self.equipItem(bestWeapon)
                self.getInventory().removeItem(bestWeapon)
            elif self.getEquipItem().getAttribute("item") != \
                 bestWeapon.getAttribute("item"):
                oldItem = self.getEquipItem()
                self.getInventory().removeItem(bestWeapon)
                self.getInventory().addItem(oldItem)
                self.equipItem(bestWeapon)
        if bestArmor != None:
            if not self.hasArmor():
                self.equipArmor(bestArmor)
                self.getInventory().removeItem(bestArmor)
            elif self.getArmor().getAttribute("item") != \
                 bestArmor.getAttribute("item"):
                oldItem = self.getArmor()
                self.getInventory().removeItem(bestArmor)
                self.getInventory().addItem(oldItem)
                self.equipArmor(bestArmor)

    def manageHealthRestoreItems(self):
        currentHealthLevel = self.getHealth()
        damageSustained = self.getBaseHealth() - currentHealthLevel
        healingItems = []
        for i in self.getInventory():
            try:
                healthBoost = i.getAttribute("healthBoost")
                healingItems.append((i, healthBoost))
            except: 1
        healingItems.sort(key=lambda x: x[1])
        if currentHealthLevel < int(self.getBaseHealth() * .8):
            choosenItem = None
            for i in healingItems:
                healthBoost = i[1] 
                if healthBoost > damageSustained:
                    break
                else:
                    choosenItem = i[0]
            if choosenItem != None:
                self.getInventory().removeItem(choosenItem)
                self.heal(choosenItem.getAttribute("healthBoost"))

    def manageHunger(self):
        hasAcorns = self.getAcorns() > 0
        if self.isHungry() and hasAcorns:
            self._acorns -= 1
            self.increaseHunger()
            
                

                

    
        
