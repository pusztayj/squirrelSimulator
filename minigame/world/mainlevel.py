"""
Author: Trevor Stalnaker
File: mainlevel.py
"""
import pygame, random, math
from polybius.graphics import *
from graphics import *
from .utils import *
from player import Player
from economy.acorn import Acorn
from economy.dirtpile import DirtPile
from animals import *
from minigame.level import Level
from minigame.merchant.utils import *
from minigame.inventoryhud import InventoryHUD
from items.item import Item
from minigame.itemblock import ItemBlock
from minigame.xpmanager import XPManager
from managers import ANIMALS, ITEMS
from polybius.managers import CONSTANTS, SOUNDS, CONTROLS

def createPack(pos):
    """Creates a random pack of a size between 1 and 3"""
    leader = Creature(random.choice(ANIMALS.getSpawnableAnimals()), pos=pos)
    p = Pack(leader)
    leader.setPack(p)
    for x in range(2):
        if random.random() < .25:
            c = Creature(random.choice(ANIMALS.getSpawnableAnimals()),
                         pos=(pos[0]+(((-1)**x)*30),
                         pos[1]+(((-1)**x)*30)))
            c.setPack(p)
            p.addMember(c)
    for creature in p:
        if creature != None:
            for _ in range(2):
                items = list(ITEMS.getItems())
                random.shuffle(items)
                for item in items:
                    if .08 >= random.random():
                        creature.getInventory().addItem(Item(item, creature))
            if random.random() < .33:
                creature.equipArmor(Item(random.choice(ITEMS.getItemsByType("armor")), creature))
            if random.random() < .33:
                creature.equipItem(Item(random.choice(ITEMS.getItemsByType("weapon")), creature))
            creature.loseHealth(random.randint(0,20))
            creature.setAcorns(random.randint(0,100))
    return p

def spawnPacks(spawnRange, spawnCount, collidables):
    """Spawns a given number of packs into the world avoiding overlaps"""
    spawns = []
    packs = []
    while len(packs) < spawnCount:
        e = createPack((random.randint(0,spawnRange[0]), random.randint(0,spawnRange[1])))
        if e.getLeader().getWanderRect().collidelist([x.getCollideRect() for x in spawns + collidables]) == -1:
            spawns.append(e.getLeader())
            packs.append(e)
    return packs

def spawn(spawnType, spawnRange, spawnCount, collidables, name=None, wanderer=False):
    """Spawns a given number of entities into the world avoiding overlaps"""
    spawns = []
    while len(spawns) < spawnCount:
        if name == None:
            e = spawnType(pos=(random.randint(0,spawnRange[0]),
                                 random.randint(0,spawnRange[1])))
        else:
            e = spawnType(name,(random.randint(0,spawnRange[0]),
                                 random.randint(0,spawnRange[1])))
        if not wanderer:
            if e.getCollideRect().collidelist([x.getCollideRect() for x in spawns + collidables]) == -1:
                spawns.append(e)
        else:
            if e.getWanderRect().collidelist([x.getCollideRect() for x in spawns + collidables]) == -1:
                spawns.append(e)
    return spawns

class MainLevel(Level):

    def __init__(self, player_pack, cheatBox):
        """Initializes the main level"""

        super().__init__()

        self._screen_size = CONSTANTS.get("screen_size")
        self._world_size = CONSTANTS.get("world_size")

        self._xpPerDay = CONSTANTS.get("xpPerDay")
        
        # Friendscore at which animals begin to attack
        self._attackThreshold = CONSTANTS.get("attackThreshold")
        
        # Agression level at which attacks will happen
        self._aggressionThreshold = CONSTANTS.get("aggressionThreshold") 

        # The number of packs in the game
        self._packPopulation = CONSTANTS.get("packPopulation")

        self._cheatBox = cheatBox

        # Fonts to be used in the main level
        self._font = pygame.font.SysFont("Times New Roman", 32)
        self._popupFont = pygame.font.SysFont("Times New Roman", 16)
        self._messageFont = pygame.font.SysFont("Times New Roman", 20)

        # Create a world clock
        self._worldClock = WorldClock(self._screen_size[0])

        # Set the player pack
        self._playerPack = player_pack
        self._packManager = PackManager(self._playerPack, self._screen_size)
        self._player = self._playerPack.getLeader()

        # Create the ground
        self._ground = Banner((0,0),CONSTANTS.get("groundColor"),
                              (self._world_size[1],self._world_size[0]))
        
        # Spawn some acorns at start of the game
        initialAcornRange = CONSTANTS.get("initialAcornRange")
        self._acorns = [Acorn((random.randint(0,self._world_size[0]),
                                       random.randint(0,self._world_size[1])))
                        for x in range(random.randint(*initialAcornRange))]

        # Create empty list for player dirt piles
        self._dirtPiles = []

        # Create empty list for abandoned piles
        self._spawnedPiles = []

        # Create timers
        self._acornSpawnTimer = random.randint(*CONSTANTS.get("acornSpawnTime"))
        self._pileSpawnTimer = random.randint(*CONSTANTS.get("pileSpawnTime"))
        self._acornLeakTimer = self._worldClock.getHourLength()
        self._hungerTimer = 2 * self._worldClock.getHourLength()
        self._starveTimer = 2 * self._worldClock.getHourLength()

        self._interactionDelay = 0.1 #Prevent buttons from being clicked when interaction opens
        self._interactionTimer = self._interactionDelay

        # Set the hover popup to None
        self._popup = None

        # Create the popup window
        self._popupWindow = PopupWindow("", (0,0), (288,100), self._messageFont,
                                        (255,255,255),(0,0,0), (120,120,120), (40,20),
                                        self._popupFont,(255,255,255), borderWidth=1)
        self._popupWindow.setPosition((self._screen_size[0]//2 - self._popupWindow.getWidth()//2,
                                       self._screen_size[1]//3 - self._popupWindow.getHeight()//2))
        self._popupWindow.close()

        # Create the confirmation window
        self._confirmationWindow = ConfirmationWindow("", (0,0), (288,150), self._messageFont,
                                        (255,255,255),(0,0,0), (120,120,120), (40,20),
                                        self._popupFont,(255,255,255), borderWidth=1)
        self._confirmationWindow.setPosition((self._screen_size[0]//2 - self._confirmationWindow.getWidth()//2,
                                       self._screen_size[1]//3 - self._confirmationWindow.getHeight()//2))
        self._confirmationWindow.close()
        self._confirmationProceedure = None

        # Create the player's stats display
        self._stats = StatDisplay((5,5),self._player)

        # Create the night filter
        self._nightFilter = Mask((0,0),self._screen_size,(20,20,50),150, False)

        # Set ATM and Interaction windows to None
        self._atm = None
        self._interaction = None

        # Add merchants to the world
        self._merchants = spawn(Merchant, (self._world_size[0]-128, self._world_size[1]+128),
                                random.randint(2,5), [])

        # Set the restocking rates for the merchants
        dayLen = self._worldClock.getDayLength()
        restockTime = CONSTANTS.get("restockTime")
        for merchant in self._merchants:
            merchant.setRestockTimer(random.randint(restockTime[0]*dayLen,
                                                    restockTime[1]*dayLen))

        # Add trees to the world
        self._trees = spawn(Drawable, (self._world_size[0]-128, self._world_size[1]+128),
                            30, self._merchants, name="tree.png")

        # Add packs to the world
        self._packs = spawnPacks((self._world_size[0]-128, self._world_size[1]+128),
                                 self._packPopulation,
                                 self._merchants + self._trees)           

        # Create the player's inventory hud
        self._hud = InventoryHUD(((self._screen_size[0]//2)-350,
                                  self._screen_size[1]-52), (700,50), self._player)

        # Create the player's armor and weapon display blocks
        self._weapon = ItemBlock((self._screen_size[0]-164,5))
        self._armor = ItemBlock((self._screen_size[0]-82,5))

        # Set the bribe and steal windows to None
        self._bribeWindow = None
        self._stealWindow = None

        # Set the fight flag to false initially
        self._fightFlag = (False,)

        # Initialize leak to False
        self._leak = False # A boolean flag for leaking acorns

        # Grace period (time between NPC attacks)
        self._gracePeriod = CONSTANTS.get("gracePeriod")
        self._graceTimer = self._gracePeriod

        # Create the XP Manager
        self._xpManager = XPManager((self._screen_size[0]//2 - 250//2, 80), self._player)
        self._xpManager.close()

        # Start playing music
        SOUNDS.manageSongs("main")
        
    def draw(self, screen):
        """Draws the level to the screen"""
        self.drawWorld(screen)
        self.drawInterfaces(screen)    

    def drawWorld(self, screen):
        """Draw the in-game objects to the screen"""
        #Draw the background to the screen
        self._ground.draw(screen)

        for acorn in self._acorns:
            acorn.draw(screen)

        for pile in self._dirtPiles:
            pile.draw(screen)

        for pile in self._spawnedPiles:
            pile.draw(screen)
            
        # Determine the layering of objects and 
        # draw them to the screen
        layering = self._trees + self._merchants + \
                  self._playerPack.getTrueMembers()
        for pack in self._packs:
            layering += pack.getTrueMembers()
        layering.sort(key=lambda x: x.getY()+x.getTrueBottom())
        for ob in layering:
            ob.draw(screen)

        self._nightFilter.draw(screen)

    def drawInterfaces(self, screen):
        """Draw huds, menus, and popups to the screen"""
        if self._popup != None:
            self._popup.draw(screen)

        self._stats.draw(screen)

        if self._atm != None and self._atm.getDisplay():
            self._atm.draw(screen)

        if self._interaction != None and self._interaction.getDisplay():
            self._interaction.draw(screen)

        self._worldClock.draw(screen)

        if self._packManager.getDisplay():
            self._packManager.draw(screen)

        self._hud.draw(screen)

        self._armor.draw(screen)
        self._weapon.draw(screen)

        if self._bribeWindow != None and self._bribeWindow.getDisplay():
            self._bribeWindow.draw(screen)

        if self._stealWindow != None and self._stealWindow.getDisplay():
            self._stealWindow.draw(screen)

        if self._xpManager.getDisplay():
            self._xpManager.draw(screen)

        if self._popupWindow.getDisplay():
            self._popupWindow.draw(screen)

        if self._confirmationWindow.getDisplay():
            self._confirmationWindow.draw(screen)

    def handleEvent(self, event):
        """Handles events for the main level"""

        # Handle events when various windows and displays are not open
        if (self._atm == None or not self._atm.getDisplay()) and \
           (self._interaction == None or not self._interaction.getDisplay()) and \
           (not self._packManager.getDisplay()) and \
           (not self._popupWindow.getDisplay()) and \
           (not self._confirmationWindow.getDisplay()) and \
           (not self._cheatBox.isDisplayed()):
            self._hud.handleEvent(event)
            self._player.move(event)
            
            # Allow the player to create dirt piles
            if CONTROLS.get("bury").check(event):
                # Check if the player can remember this new pile
                if len(self._dirtPiles) < self._player.getMemory():
                    self._player._fsm.changeState("bury")
                    if self._player.isFlipped():
                        dp = DirtPile((self._player.getX() - (3//4)*(self._player.getWidth() // 2),
                                self._player.getY() + (self._player.getHeight() // 3)),
                                      capacity=8+(self._player.getDiggingSkill()*2))
                    else:
                        dp = DirtPile((self._player.getX() + (self._player.getWidth() // 2),
                                self._player.getY() + (self._player.getHeight() // 3)),
                                      capacity=8+(self._player.getDiggingSkill()*2))
                    self._dirtPiles.append(dp)
                else:
                    self._confirmationWindow.setText("Are you sure you want to create\na new acorn pile?\nYou will forget an old one")
                    self._confirmationWindow.display()
                    self._confirmationProceedure = (1,) #Redirect neccessary information
                    # Stop the player's movement
                    self._player.stop()

            # Check if the left mouse button has been clicked
            if CONTROLS.get("select").check(event):

                # Check if the player has clicked on a dirtpile
                for pile in self._dirtPiles:
                    if pile.getCollideRect().collidepoint((event.pos[0] + Drawable.WINDOW_OFFSET[0],
                              event.pos[1] + Drawable.WINDOW_OFFSET[1])):
                        self._atm = ATM(self._player, pile, self._screen_size)

                # Check if the player has clicked on a creature
                for pack in self._packs:
                    for creature in pack:
                        if creature != None:
                            x,y = creature.getPosition()
                            for rect in creature.getCollideRects():
                                r = rect.move(x,y)
                                if r.collidepoint((event.pos[0] + Drawable.WINDOW_OFFSET[0],
                                                     event.pos[1] + Drawable.WINDOW_OFFSET[1])):
                                    self._interaction = Interaction(creature)
                                    self._interactionTimer = self._interactionDelay
                                    self._player.stop()

                # Check if the player has clicked on a merchant
                for merchant in self._merchants:
                    if merchant.getCollideRect().collidepoint((event.pos[0] + Drawable.WINDOW_OFFSET[0],
                                             event.pos[1] + Drawable.WINDOW_OFFSET[1])):
                        return (1, merchant) # Set Game Mode to Merchant and provide merchant

            # Check for a right click event
            if CONTROLS.get("use_item").check(event):

                # Get the current active item in the hud
                item = self._hud.getActiveItem()

                # Player eats a food item
                if item != None and item.getAttribute("type") == "food":
                    self._player.getInventory().removeItem(item)
                    self._player.eat(item.getAttribute("hungerBoost"), item.getAttribute("healthBoost"))

                # Use a tool to dig up an acorn pile
                if item != None and item.getAttribute("type") == "tool":
                    for pile in self._spawnedPiles:
                        if pile.getCollideRect().collidepoint((event.pos[0] + Drawable.WINDOW_OFFSET[0],
                              event.pos[1] + Drawable.WINDOW_OFFSET[1])):
                            if self._player.getAcorns() + pile.getAcorns() > self._player.getCheekCapacity():
                                self._confirmationWindow.setText("Are you sure you want to\n dig up this acorn pile?\nYou" + \
                                                                 " won't collect all the acorns")
                                self._confirmationWindow.display()
                                self._confirmationProceedure = (2, pile, item) #Redirect neccessary information
                                # Stop the player's movement
                                self._player.stop()
                            else:
                                self._spawnedPiles.remove(pile)
                                # Determine the number of acorns the player can collect
                                # based on the number in the pile and the tool being used
                                acorns = round(pile.getAcorns() * item.acornModifier())
                                self._player.setAcorns(min(self._player.getCheekCapacity(), self._player.getAcorns() + acorns))
                            
                    # Check if the player is trying to dig up their own pile
                    for pile in self._dirtPiles:
                        if pile.getCollideRect().collidepoint((event.pos[0] + Drawable.WINDOW_OFFSET[0],
                              event.pos[1] + Drawable.WINDOW_OFFSET[1])):
                            self._confirmationWindow.setText("Are you sure you want to\n dig up your acorn pile?")
                            self._confirmationWindow.display()
                            self._confirmationProceedure = (0, pile,item) #Redirect neccessary information
                            # Stop the player's movement
                            self._player.stop()
                            
                # Sets the current weapon            
                if item != None and item.getAttribute("type") == "weapon":
                    previous = self._weapon.getItem()
                    if previous != None:
                        self._player.getInventory().addItem(previous)
                    self._player.equipItem(item)
                    self._weapon.setItem(item)
                    self._player.getInventory().removeItem(item)

                # Sets the current armor
                if item != None and item.getAttribute("type") == "armor":
                    previous = self._armor.getItem()
                    if previous != None:
                        self._player.getInventory().addItem(previous)
                    self._player.equipArmor(item)
                    self._armor.setItem(item)
                    self._player.getInventory().removeItem(item)

                # Applies a potion
                if item != None and item.getAttribute("type") == "potion":
                    self._player.getInventory().removeItem(item)
                    self._player.heal(item.getAttribute("healthBoost"))

        # If a variety of windows and interfaces are not displayed
        if not self._popupWindow.getDisplay() and \
           (self._bribeWindow==None or not self._bribeWindow.getDisplay()) and \
           not self._confirmationWindow.getDisplay() and \
           (self._stealWindow==None or not self._stealWindow.getDisplay()):
            if self._atm != None and self._atm.getDisplay():
                self._atm.handleEvent(event)

            # Handle events on the pack manager
            if self._packManager.getDisplay():
                c = self._packManager.handleEvent(event)
                if c != None and c[0] == 9:
                    self._playerPack.removeMember(c[1])
                    clone = c[1].clone()
                    clone.changeFriendScore(random.randint(-25,-5))
                    p = Pack(clone)
                    self._packs.append(p)
                    clone.setPack(p)
                    
                    

            # Handle events on the interaction interface
            if self._interaction != None and self._interaction.getDisplay() and self._interactionTimer < 0:
                self._popup = None
                code = self._interaction.handleEvent(event)
                if (code == 1):
                    enemyPack = self._interaction.getEntity().getPack()
                    for e in enemyPack:
                        if e != None:
                            e.changeFriendScore(random.randint(-30,-10))
                    self._interaction = None
                    return (2,self._playerPack,enemyPack)
                elif (code == 2):
                    e = self._interaction.getEntity()
                    if self._playerPack.trueLen() < 3:
                        if e.getPack().trueLen() == 1:
                            if e.getFriendScore() + (self._player.getCharisma() * .5) > 60:
                                self._playerPack.addMember(e)
                                self._packs.remove(e.getPack())
                                e.setPack(self._playerPack)
                                self._popupWindow.setText(e.getName() + " has joined your pack")
                                self._popupWindow.display()
                                self._interaction = None # Close the interaction window
                            else:
                                self._popupWindow.setText(e.getName() + " doesn't want\nto join your pack")
                                self._popupWindow.display()
                        else:
                            self._popupWindow.setText(e.getName() + " is already part of a pack")
                            self._popupWindow.display()
                    else:
                        self._popupWindow.setText("Your pack is already full")
                        self._popupWindow.display()
                elif (code == 3):
                    e = self._interaction.getEntity()
                    self._stealWindow = Steal(self._player, e, self._screen_size)
                    self._stealWindow.display()
                elif (code == 4):
                    e = self._interaction.getEntity()
                    self._bribeWindow = Bribe(self._player, e, self._screen_size)
                    self._bribeWindow.display()
                

        # Determine the relative position of the mouse
        mouse = pygame.mouse.get_pos()
        m_pos_offset = self._player.adjustMousePos(mouse)
        m_pos_offset = (m_pos_offset[0], m_pos_offset[1])   
        popup_pos = (mouse[0] + 5, mouse[1] + 5)

        # Create a list of current creatures in the game
        # for use with popup creation
        creatures = []
        for pack in self._packs:
            for creature in pack:
                if creature != None:
                    creatures.append(creature)
        for creature in self._playerPack:
            if creature != None:
                creatures.append(creature)

        # Create the hover popups if the mouse is over an entity
        self._popup = self.setPopup(creatures, m_pos_offset, popup_pos, self._popupFont)
        if self._popup==None:
            self._popup = self.setPopup(self._dirtPiles, m_pos_offset, popup_pos, self._popupFont)
        if self._popup==None:
            self._popup = self.setPopup(self._spawnedPiles, m_pos_offset, popup_pos, self._popupFont)
        if self._popup == None:
            self._popup = self.setPopup(self._merchants, m_pos_offset, popup_pos, self._popupFont)

        # Check if the pack manager should be opened or closed
        if (self._atm == None or not self._atm.getDisplay()) and \
           (self._interaction == None or not self._interaction.getDisplay()) and \
           (not self._popupWindow.getDisplay()) and \
           not self._xpManager.getDisplay() and \
           not self._confirmationWindow.getDisplay() and \
           not self._cheatBox.isDisplayed():
            if CONTROLS.get("open_pack_manager").check(event):
                if self._packManager._timeSinceClosed > self._packManager._delay:
                    self._packManager.display()
                    self._player.stop()


        # Check if the XP Manager should be opened or closed
        if (self._atm == None or not self._atm.getDisplay()) and \
           (self._interaction == None or not self._interaction.getDisplay()) and \
           (not self._popupWindow.getDisplay()) and \
           not self._packManager.getDisplay() and \
           not self._confirmationWindow.getDisplay() and \
           not self._cheatBox.isDisplayed():
            if CONTROLS.get("open_xp_manager").check(event):
                if self._xpManager.getDisplay():
                    self._xpManager.close()
                else:
                    self._xpManager.display()
                    self._player.stop()

        # Once the user confirms, dig up a pile or not
        if self._confirmationWindow.getDisplay():
            c = self._confirmationWindow.handleEvent(event)
            if c == 1 and self._confirmationProceedure!=None:
                # Dig up a players acorn pile
                if self._confirmationProceedure[0] == 0:
                    pile = self._confirmationProceedure[1]
                    item = self._confirmationProceedure[2]
                    self._dirtPiles.remove(pile)
                    acorns = round(pile.getAcorns() + (pile.getAcorns()*item.getAcornBoost()))
                    self._player.setAcorns(min(self._player.getCheekCapacity(), self._player.getAcorns() + acorns))
                # Create a new acorn pile and forget an old one
                if self._confirmationProceedure[0] == 1:
                    self._player._fsm.changeState("bury")
                    if self._player.isFlipped():
                        dp = DirtPile((self._player.getX() - (3//4)*(self._player.getWidth() // 2),
                                self._player.getY() + (self._player.getHeight() // 3)),
                                      capacity=8+(self._player.getDiggingSkill()*2))
                    else:
                        dp = DirtPile((self._player.getX() + (self._player.getWidth() // 2),
                                self._player.getY() + (self._player.getHeight() // 3)),
                                      capacity=8+(self._player.getDiggingSkill()*2))
                    lostPile = random.choice(self._dirtPiles)
                    self._dirtPiles.remove(lostPile)
                    lostPile.setName("Abandoned Pile")
                    self._spawnedPiles.append(lostPile)
                    self._dirtPiles.append(dp)
                if self._confirmationProceedure[0] == 2:
                    pile = self._confirmationProceedure[1]
                    item = self._confirmationProceedure[2]
                    self._spawnedPiles.remove(pile)
                    acorns = round(pile.getAcorns() + (pile.getAcorns()*item.getAcornBoost()))
                    self._player.setAcorns(min(self._player.getCheekCapacity(), self._player.getAcorns() + acorns))

        # Handle events on the bribe interface
        if self._bribeWindow != None and self._bribeWindow.getDisplay():
            self._bribeWindow.handleEvent(event)
            self._interaction.updateInteraction()

        # Handle events on the steal interface
        if self._stealWindow != None and self._stealWindow.getDisplay():
            bustedRobbery = self._stealWindow.handleEvent(event)
            self._interaction.updateInteraction()
            if bustedRobbery:
                self._popupWindow.setText("You have been caught!\nPrepare for a fight")
                self._popupWindow.display()
                self._fightFlag = (True, self._interaction.getEntity().getPack()) #Start Combat on okay

        # Handle events on the XP Manager
        if self._xpManager.getDisplay() and not self._popupWindow.getDisplay() and \
           not self._confirmationWindow.getDisplay():
            c = self._xpManager.handleEvent(event)
            if c != None:
                if c[0] == 0:
                    self._popupWindow.setText("You do not have any XP")
                    self._popupWindow.display()

        # Check to see if NPC creatures want to attack the player
        if self._graceTimer <= 0:
            for pack in self._packs:
                leader = pack.getLeader()
                rect = leader.getWanderRect()
                for creature in pack:
                    if creature != None:
                        if creature.getFriendScore() < self._attackThreshold:
                            if creature.getAggression() > self._aggressionThreshold:
                                if self._player.getCollideRect().colliderect(rect):
                                    self._popupWindow.setText("You entered enemy territory!\nPrepare for a fight")
                                    self._popupWindow.display()
                                    for k in self._player._movement.keys(): self._player._movement[k] = False
                                    self._fightFlag = (True, leader.getPack()) #Start Combat on okay
                                    self._graceTimer = self._gracePeriod

        # Display the combat window once the player confirms the popup window
        if self._popupWindow.getDisplay():
            self._popupWindow.handleEvent(event)
            if self._popupWindow.getConfirmed() and self._fightFlag[0]:
                enemyPack = self._fightFlag[1]
                self._fightFlag = (False,)
                self._interaction = None
                self._stealWindow = None
                for e in enemyPack:
                    if e != None:
                        e.changeFriendScore(random.randint(-30,-10))
                return (2,self._playerPack,enemyPack)
                    
    def setPopup(self, lyst, mouse_pos, popup_pos, font):
       """Creates and manages hover popups"""
       for entity in lyst:
          x,y = entity.getPosition()
          for rect in entity.getCollideRects():
             r = rect.move(x,y)
             if r.collidepoint(mouse_pos):
                 name = entity.getName()
                 if type(entity) == Merchant:
                     name += "'s Shop"
                 return Popup(name, popup_pos, font)

    def update(self, ticks):
        """Updates the main level based on ticks from the game clock"""
        
        # Check if acorns have been collected or if they have despawned
        for acorn in self._acorns:
            if acorn.getCollideRect().colliderect(self._player.getCollideRect()) and \
                self._player.getCheekCapacity() - self._player.getAcorns() > 0:
                self._player.setAcorns(self._player.getAcorns()+1)
                acorn.collected()
            acorn.update(ticks)

        # Update piles so that they can despawn
        for pile in self._spawnedPiles:
            pile.update(ticks)

        # Spawn acorns around the map
        self._acornSpawnTimer -= ticks
        if self._acornSpawnTimer <= 0:
            self._acorns.append(Acorn((random.randint(0,self._world_size[0]),
                                       random.randint(0,self._world_size[1]))))
            self._acornSpawnTimer = random.randint(2,5)

        # Spawn Abandoned Piles around the map
        self._pileSpawnTimer -= ticks
        if self._pileSpawnTimer <=0:
            d = DirtPile((random.randint(0,self._world_size[0]),
                          random.randint(0,self._world_size[1])),
                         "Abandoned Pile")
            d.setAcorns(random.randint(1,20))
            self._spawnedPiles.append(d)
            self._pileSpawnTimer = random.randint(20,40)

        # Decrement the hunger time and update hunger
        self._hungerTimer -= ticks
        if self._hungerTimer <= 0:
            self._player.decrementHunger()
            self._hungerTimer = 2 * self._worldClock.getHourLength()

        # Update the night filter's alpha values
        self._nightFilter.setAlpha(round((-100*math.sin((math.pi /60)*(self._worldClock.getTime()-5)))+100))

        # Control if a player is starving
        if self._player.isStarving():
            self._starveTimer -= ticks
            if self._starveTimer <= 0:
                self._player.loseHealth(5)
                self._player.loseStamina(5)
                self._starveTimer = 2 * self._worldClock.getHourLength()
        else:
            self._starveTimer = 2 * self._worldClock.getHourLength()

        # Control acorn leakage if the player is carrying too many acorns
        if self._player.getAcorns() > self._player.getCheekCapacity():
            if self._leak == False:
                self._leak = True
                self._popupWindow.setText("You are carrying too many acorns!\nStash them or you'll drop them")
                self._popupWindow.display()
                for k in self._player._movement.keys(): self._player._movement[k] = False
            self._acornLeakTimer -= ticks
            if self._acornLeakTimer <= 0:
                percentLoss = random.randint(3,4)
                overflowAcorns = self._player.getAcorns() - self._player.getCheekCapacity()
                loss = (overflowAcorns // percentLoss) + random.randint(0,5)
                self._player.setAcorns(self._player.getAcorns() - loss)
                self._acornLeakTimer = self._worldClock.getHourLength()
        else:
            self._acornLeakTimer = self._worldClock.getHourLength()
            self._leak = False

        # Control merchant restocking
        for merchant in self._merchants:
            merchant.update(ticks)

        # Update the grace period between attacks
        self._graceTimer -= ticks

        # Update the interaction timer (used to prevent instantaneous button clicks)
        if  self._interaction != None and self._interaction.getDisplay() and self._interactionTimer >= 0:
            self._interactionTimer -= ticks

        # Update the bribe window, if one exists
        if self._bribeWindow != None and self._bribeWindow.getDisplay():
            self._bribeWindow.update()

        # Update the steal window, if one exists
        if self._stealWindow != None and self._stealWindow.getDisplay():
            self._stealWindow.update()

        #Update the player's position
        self._player.update(self._world_size, ticks)

        # Update the players stats
        self._stats.update()

        #Update the offset based on the player's location
        self._player.updateOffset(self._player, self._screen_size, self._world_size)

        # Remove acorns from the world that have been collected
        self._acorns = [acorn for acorn in self._acorns if not acorn.isCollected()]

        #Update InGame Clock
        self._worldClock.update(ticks)

        # Update the players inventory hud
        self._hud.update(ticks)

        # Update the current weapon and armor displays     
        self._weapon.updateBlock()
        self._armor.updateBlock()

        # Update the player's pack
        self._playerPack.update(self._world_size, ticks)

        # Update the pack manager
        self._packManager.update(ticks)

        # Remove dead packs from the game
        self._packs = [pack for pack in self._packs if not pack.isDead()]

        # Spawn a new pack if the pack population has fallen below its default
        if len(self._packs) < self._packPopulation:
            pack = spawnPacks((self._world_size[0]-128, self._world_size[1]+128), 1,
                              self._merchants + self._trees + [p.getLeader() for p in self._packs])
            self._packs += pack

        # Update packs
        for pack in self._packs: 
            pack.getLeader().wander(ticks)
            if pack.trueLen() > 1:
                pack.update(self._world_size, ticks)

        # Check if a day has passed in game time
        if self._worldClock.dayPassed():
            self._player.setXP(self._player.getXP() + self._xpPerDay)

        # Load and play a new song if the current song has ended
        SOUNDS.manageSongs("main")
        


