"""
Author: Trevor Stalnaker
File: mainlevel.py
"""
from .timer import Timer
from .pileManager import PileManager
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

def spawn(spawnType, spawnRange, spawnCount, collidables=[], name=None, wanderer=False):
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

        self._playerPack = player_pack

        self.setConstants()
        self.setFonts()
        self.setupGameElements()

        self._cheatBox = cheatBox

        # Set the fight flag to false initially
        self._fightFlag = (False,)

        # Initialize leak to False
        self._leak = False # A boolean flag for leaking acorns

        # Start playing music
        SOUNDS.manageSongs("main")

    def setConstants(self):
        self._screen_size = CONSTANTS.get("screen_size")
        self._world_size = CONSTANTS.get("world_size")
        self._xpPerDay = CONSTANTS.get("xpPerDay")
        
        # Friendscore at which animals begin to attack
        self._attackThreshold = CONSTANTS.get("attackThreshold")
        
        # Agression level at which attacks will happen
        self._aggressionThreshold = CONSTANTS.get("aggressionThreshold") 

        # The number of packs in the game
        self._packPopulation = CONSTANTS.get("packPopulation")

    def setFonts(self):
        self._font = pygame.font.SysFont("Times New Roman", 32)
        self._popupFont = pygame.font.SysFont("Times New Roman", 16)
        self._messageFont = pygame.font.SysFont("Times New Roman", 20)

    def setupGameElements(self):
        self._worldClock = WorldClock(self._screen_size[0])
        self.setupTimers()
        self.setupEnvironment()
        self.setupEntities()
        self.setupUI()

    def setupTimers(self):
        self._acornSpawnTimer = Timer(lambda: random.randint(*CONSTANTS.get("acornSpawnTime")))
        self._pileSpawnTimer = Timer(lambda: random.randint(*CONSTANTS.get("pileSpawnTime")))
        self._acornLeakTimer = Timer(self._worldClock.getHourLength())
        self._hungerTimer = Timer(2 * self._worldClock.getHourLength())
        self._starveTimer = Timer(2 * self._worldClock.getHourLength())

        #Prevent buttons from being clicked when interaction opens
        self._interactionDelay = 0.1 
        self._interactionTimer = self._interactionDelay

        # Grace period (time between NPC attacks)
        self._gracePeriod = CONSTANTS.get("gracePeriod")
        self._graceTimer = self._gracePeriod

    def setupEnvironment(self):
        # Create the ground
        dimensions = (self._world_size[1],self._world_size[0])
        self._ground = Banner((0,0),CONSTANTS.get("groundColor"), dimensions)

        # Create the night filter
        self._nightFilter = Mask((0,0),self._screen_size,(20,20,50),150, False)
        
        # Spawn some acorns at start of the game
        initialAcornRange = CONSTANTS.get("initialAcornRange")
        initialAcornCount = random.randint(*initialAcornRange)
        self._acorns = list()
        for x in range(initialAcornCount): self.spawnAcorn()

        self._pileManager = PileManager()

        self.setupMerchants()
        self.spawnTrees()
        
    def spawnTrees(self):
        spawnRange = (self._world_size[0]-128, self._world_size[1]+128)
        numberOfTreesToSpawn = 30
        entitiesToAvoidOverlapping = self._merchants
        self._trees = spawn(Drawable, spawnRange, numberOfTreesToSpawn,
                            entitiesToAvoidOverlapping, name="tree.png")

    def setupEntities(self):
        self.setupPlayerPack()
        self.setupPacks()

    def setupPacks(self):
        spawnRange = (self._world_size[0]-128, self._world_size[1]+128)
        numberOfPacksToSpawn = self._packPopulation
        entitiesToAvoidOverlapping = self._merchants + self._trees
        self._packs = spawnPacks(spawnRange, numberOfPacksToSpawn,
                                 entitiesToAvoidOverlapping)

    def setupMerchants(self):
        # Add merchants to the world
        spawnRange = (self._world_size[0]-128, self._world_size[1]+128)
        numberOfMerchantsToSpawn = random.randint(2,5)
        self._merchants = spawn(Merchant, spawnRange, numberOfMerchantsToSpawn)

        # Set the restocking rates for the merchants
        dayLen = self._worldClock.getDayLength()
        baseRestockTime = CONSTANTS.get("restockTime")
        restockTime = random.randint(baseRestockTime[0]*dayLen,
                                     baseRestockTime[1]*dayLen)
        for merchant in self._merchants:
            merchant.setRestockTimer(restockTime)

    def setupPlayerPack(self):
        self._player = self._playerPack.getLeader()
        self._packManager = PackManager(self._playerPack, self._screen_size)

    def createConfirmationAndPopupWindows(self):

        # Set the fonts
        font = self._messageFont
        buttonFont = self._popupFont

        # Set the dimensions
        width, height = 288, 150
        dimensions = (width, height)
        buttonWidth, buttonHeight = 40, 20
        buttonDimensions = (buttonWidth, buttonHeight)

        # Set the color scheme
        fontColor = (255,255,255)
        backgroundColor = (0,0,0)
        buttonFontColor = (255,255,255)
        buttonColor = (120,120,120)

        self._popupWindow = PopupWindow("", (0,0), dimensions, font, fontColor,
                                        backgroundColor, buttonColor, buttonDimensions,
                                        buttonFont,buttonFontColor, borderWidth=1)
        
        self._confirmationWindow = ConfirmationWindow("", (0,0), dimensions, font, fontColor,
                                            backgroundColor, buttonColor, buttonDimensions,
                                            buttonFont, buttonFontColor, borderWidth=1)
        
        # Position the window on the screen
        verticalCenter = 1/3 #from top of screen
        horizontalCenter = 1/2 #from left of screen
        self._popupWindow.center(cen_point=(horizontalCenter, verticalCenter))
        self._confirmationWindow.center(cen_point=(horizontalCenter, verticalCenter))

        self._popupWindow.close()
        self._confirmationWindow.close()
        self._confirmationProcedure = None

    def setupUI(self):
        # Set the hover popup to None
        self._popup = None

        self.createConfirmationAndPopupWindows()

        # Create the player's stats display
        self._stats = StatDisplay((5,5),self._player)

        # Set ATM and Interaction windows to None
        self._atm = None
        self._interaction = None

        # Create the player's inventory hud
        self._hud = InventoryHUD(((self._screen_size[0]//2)-350,
                                  self._screen_size[1]-52), (700,50), self._player)

        # Create the player's armor and weapon display blocks
        self._weapon = ItemBlock((self._screen_size[0]-164,5))
        self._armor = ItemBlock((self._screen_size[0]-82,5))

        # Set the bribe and steal windows to None
        self._bribeWindow = None
        self._stealWindow = None

        # Create the XP Manager
        self._xpManager = XPManager((self._screen_size[0]//2 - 250//2, 80), self._player)
        self._xpManager.close()
        
 
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

        for pile in self._pileManager.getAllPiles():
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

    def handleCreateDirtPileEvent(self, event):
        # Allow the player to create dirt piles
        if CONTROLS.get("bury").check(event):
            # Check if the player can remember this new pile
            currentPlayerPiles = self._pileManager.getNumberOfPlayerPiles()
            playerMemory = self._player.getMemory()
            playerCanRememberAnotherPile = currentPlayerPiles < playerMemory
            if playerCanRememberAnotherPile:
                self.digNewPile()
            else:
                self._confirmationWindow.setText("Are you sure you want to create\na new acorn pile?\nYou will forget an old one")
                self._confirmationWindow.setConfirmFunction(self.digNewPileAndForgetOldOne)
                self._confirmationWindow.display()
                self._player.stop()

    def digNewPileAndForgetOldOne(self):
        self.forgetOldPile()
        self.digNewPile()
        
    def handleSelectDirtPileEvent(self, event):
        coords = self.getWorldCoordinatesFromRelativeEvent(event)
        for pile in self._pileManager.getPlayerPiles():
            pileSelected = pile.getCollideRect().collidepoint(coords)
            if pileSelected:
                self._atm = ATM(self._player, pile, self._screen_size)

    def handleSelectCreatureEvent(self, event):
        coords = self.getWorldCoordinatesFromRelativeEvent(event)
        for pack in self._packs:
            for creature in pack:
                if creature != None:
                    x,y = creature.getPosition()
                    for rect in creature.getCollideRects():
                        r = rect.move(x,y)
                        creatureSelected = r.collidepoint(coords)
                        if creatureSelected:
                            self._interaction = Interaction(creature)
                            self._interactionTimer = self._interactionDelay
                            self._player.stop()

    def handleSelectMerchantEvent(self, event):
        coords = self.getWorldCoordinatesFromRelativeEvent(event)
        for merchant in self._merchants:
            if merchant.getCollideRect().collidepoint(coords):
                return (1, merchant) # Set Game Mode to Merchant and provide merchant

    def handleSelectionEvents(self, event):
        if CONTROLS.get("select").check(event):
            self.handleSelectDirtPileEvent(event)
            self.handleSelectCreatureEvent(event)
            code = self.handleSelectMerchantEvent(event)
            if code != None: return code #Temporary refactoring code

    def handleEatEvent(self, item):
        self._player.getInventory().removeItem(item)
        self._player.eat(item.getAttribute("hungerBoost"), item.getAttribute("healthBoost"))

    def getWorldCoordinatesFromRelativeEvent(self, event):
        relative_x = event.pos[0] + Drawable.WINDOW_OFFSET[0]
        relative_y = event.pos[1] + Drawable.WINDOW_OFFSET[1]
        worldCoordinateClicked = (relative_x, relative_y)
        return worldCoordinateClicked

    def tryToDigUpPile(self, event, item):
        coordinates = self.getWorldCoordinatesFromRelativeEvent(event)
        for pile in self._pileManager.getAllPiles():
            pileClicked = pile.getCollideRect().collidepoint(coordinates)
            if pileClicked:
                isPlayerPile = pile.getOwner() == self._player
                notEnoughSpace = pile.getAcorns() > self._player.getAvailableCheekSpace()
                if isPlayerPile and notEnoughSpace:
                    self.confirmDiggingUpPlayerPileWithoutMaxAcornCollection(pile, item)
                elif isPlayerPile:
                    self.confirmDiggingUpPlayerPile(pile, item)
                elif notEnoughSpace:
                    self.confirmDiggingUpPileWithoutMaxAcornCollection(pile, item)
                else:
                    self.digUpPile(pile, item)
                self._player.stop()

    def confirmDiggingUpPlayerPileWithoutMaxAcornCollection(self, pile, item):
        self._confirmationWindow.setText("Are you sure you want to\n dig up your acorn pile?")
        self._confirmationWindow.setConfirmFunction(self.confirmDiggingUpPileWithoutMaxAcornCollection,
                                                    (pile, item))
        self._confirmationWindow.display()

    def confirmDiggingUpPileWithoutMaxAcornCollection(self, pile, item):
        self._confirmationWindow.setText("Are you sure you want to\n dig up this acorn pile?\nYou" + \
                                         " won't collect all the acorns")
        self._confirmationWindow.setConfirmFunction(self.digUpPile, (pile, item))
        self._confirmationWindow.display()
        
    def confirmDiggingUpPlayerPile(self, pile, item):
        self._confirmationWindow.setText("Are you sure you want to\n dig up your acorn pile?")
        self._confirmationWindow.setConfirmFunction(self.digUpPile, (pile, item))
        self._confirmationWindow.display()
        
    def digUpPile(self, pile, item):
        self._pileManager.removePile(pile)
        acornsInPile = pile.getAcorns()
        potentialHarvest = round(acornsInPile*(1+item.acornModifier()))
        playerMaxAcorns = self._player.getCheekCapacity()
        playerPotentialAcorns = self._player.getAcorns() + acornsInPile
        trueTotal = min(playerMaxAcorns, playerPotentialAcorns)
        self._player.setAcorns(trueTotal)
         
    def handleUseToolEvent(self, event, item):
        self.tryToDigUpPile(event, item)
                
    def handleWeaponEquipEvent(self, item):
        previous = self._weapon.getItem()
        if previous != None:
            self._player.getInventory().addItem(previous)
        self._player.equipItem(item)
        self._weapon.setItem(item)
        self._player.getInventory().removeItem(item)

    def handleArmorEquipEvent(self, item):
        previous = self._armor.getItem()
        if previous != None:
            self._player.getInventory().addItem(previous)
        self._player.equipArmor(item)
        self._armor.setItem(item)
        self._player.getInventory().removeItem(item)

    def handleUsePotionEvent(self, item):
        self._player.getInventory().removeItem(item)
        self._player.heal(item.getAttribute("healthBoost"))

    def handleUseItemEvent(self, event):
        if CONTROLS.get("use_item").check(event):
            # Get the current active item in the hud
            item = self._hud.getActiveItem()
            if item != None:
                itemType = item.getAttribute("type")
                if itemType == "food":
                    self.handleEatEvent(item)
                elif itemType == "tool":
                    self.handleUseToolEvent(event, item)
                elif itemType == "weapon":
                    self.handleWeaponEquipEvent(item)
                elif itemType == "armor":
                    self.handleArmorEquipEvent(item)
                elif itemType == "potion":
                    self.handleUsePotionEvent(item)

    def handlePackManagerEvent(self, event):
        if self.isOnlyActiveWindow(self._packManager):
            if CONTROLS.get("open_pack_manager").check(event) and \
                self._packManager._display == True:
                    self._packManager.close()
            else:
                c = self._packManager.handleEvent(event)
                if c != None and c[0] == 9:
                    self._playerPack.removeMember(c[1])
                    clone = c[1].clone()
                    clone.changeFriendScore(random.randint(-25,-5))
                    p = Pack(clone)
                    self._packs.append(p)
                    clone.setPack(p)

    def areActiveWindows(self):
        windowStates = self.getWindowStates()
        return any(windowStates.values())

    def getWindowStates(self):
        windowsToCheck = [self._atm, self._interaction, self._bribeWindow,
                          self._stealWindow, self._packManager, self._popupWindow,
                          self._confirmationWindow, self._cheatBox, self._xpManager]
        windowStates = {window:self.isActiveWindow(window) for window in windowsToCheck}
        return windowStates

    def isOnlyActiveWindow(self, window):
        windowStates = self.getWindowStates()
        if not self.isActiveWindow(window): return False
        for w, s in windowStates.items():
            if s and w != window:
                return False
        return True
        
    def handleInteractionWindowEvent(self, event):
        if self.isOnlyActiveWindow(self._interaction) and self._interactionTimer < 0:
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

    def createPopUpsOnHover(self):
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
            piles = self._pileManager.getAllPiles()
            self._popup = self.setPopup(piles, m_pos_offset, popup_pos, self._popupFont)
        if self._popup == None:
            self._popup = self.setPopup(self._merchants, m_pos_offset, popup_pos, self._popupFont)

    def isActiveWindow(self, window):
        return not(window == None) and window.getDisplay()

    def handleOpenWindowEvent(self, event, window, e):
        if e.check(event) and not window.getDisplay():
            window.display()
            self._player.stop()

    def handleOpenPackManagerEvent(self, event):
        eventReference = CONTROLS.get("open_pack_manager")
        window = self._packManager
        self.handleOpenWindowEvent(event, window, eventReference)

    def handleOpenXPManagerEvent(self, event):
        eventReference = CONTROLS.get("open_xp_manager")
        window = self._xpManager
        self.handleOpenWindowEvent(event, window, eventReference)

    def handleCloseXPManagerEvent(self, event):
        if self.isOnlyActiveWindow(self._xpManager):
            if CONTROLS.get("open_xp_manager").check(event):
                if self._xpManager.getDisplay():
                    self._xpManager.close()

    def handleEventsOnXPManager(self, event):
        if self.isOnlyActiveWindow(self._xpManager):
            c = self._xpManager.handleEvent(event)
            if c != None:
                if c[0] == 0:
                    self._popupWindow.setText("You do not have any XP")
                    self._popupWindow.display()

    def handleEventsOnBribeWindow(self, event):
        if self.isActiveWindow(self._bribeWindow):
            self._bribeWindow.handleEvent(event)
            self._interaction.updateInteraction()

    def handleEventsOnStealWindow(self, event):
        if self.isActiveWindow(self._stealWindow):
            bustedRobbery = self._stealWindow.handleEvent(event)
            self._interaction.updateInteraction()
            if bustedRobbery:
                self._popupWindow.setText("You have been caught!\nPrepare for a fight")
                self._popupWindow.display()
                self._fightFlag = (True, self._interaction.getEntity().getPack()) #Start Combat on okay

    def handleEventsOnConfirmationWindow(self, event):
        if self.isActiveWindow(self._confirmationWindow):
            self._confirmationWindow.handleEvent(event)

    def handleEventsOnPopUpWindow(self, event):
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

    def handleNPCAttacks(self):
        if self._graceTimer <= 0:
            for pack in self._packs:
                leader = pack.getLeader()
                rect = leader.getWanderRect()
                for c in pack.getTrueMembers():
                    attackThresholdMet = c.getFriendScore() < self._attackThreshold
                    aggressionThresholdMet = c.getAggression() > self._aggressionThreshold
                    playerInEnemyTerritory = self._player.getCollideRect().colliderect(rect)
                    if attackThresholdMet and aggressionThresholdMet and playerInEnemyTerritory:    
                        self._popupWindow.setText("You entered enemy territory!\nPrepare for a fight")
                        self._popupWindow.display()
                        self._player.stop()
                        self._fightFlag = (True, leader.getPack()) #Start Combat on okay
                        self._graceTimer = self._gracePeriod

    def manageEventsHandledAlways(self, event):
        self.createPopUpsOnHover()
        self.handleEventsOnConfirmationWindow(event)
        self.handleEventsOnBribeWindow(event)
        self.handleEventsOnStealWindow(event)
        self.handleEventsOnXPManager(event)
        self.handleNPCAttacks()
        self.handleEventsOnPopUpWindow(event)

    def manageEventsHandledWhenNoActiveWindows(self, event):
        self._hud.handleEvent(event)
        self._player.move(event)
        self.handleCreateDirtPileEvent(event)
        code = self.handleSelectionEvents(event)
        if code != None: return code #Temporary refactoring code
        self.handleUseItemEvent(event)
        self.handleOpenPackManagerEvent(event)
        self.handleOpenXPManagerEvent(event)

    def manageEventsHandledWhenActiveWindows(self, event):
        if self.isOnlyActiveWindow(self._atm):
            self._atm.handleEvent(event)
        self.handlePackManagerEvent(event)
        code = self.handleInteractionWindowEvent(event)
        if code != None: return code #Temporary refactoring code
        self.handleCloseXPManagerEvent(event)
        
    def handleEvent(self, event):
        """Handles events for the main level"""
        if not self.areActiveWindows():
            c = self.manageEventsHandledWhenNoActiveWindows(event)
        else:
            c = self.manageEventsHandledWhenActiveWindows(event)
        if c != None: return c # Temporary refactoring code
        self.manageEventsHandledAlways(event)



    def digNewPile(self):
        # Create a new acorn pile and forget an old one
        self._player._fsm.changeState("bury")
        if self._player.isFlipped():
            dp = DirtPile((self._player.getX() - (3//4)*(self._player.getWidth() // 2),
                    self._player.getY() + (self._player.getHeight() // 3)),
                          capacity=8+(self._player.getDiggingSkill()*2))
        else:
            dp = DirtPile((self._player.getX() + (self._player.getWidth() // 2),
                    self._player.getY() + (self._player.getHeight() // 3)),
                          capacity=8+(self._player.getDiggingSkill()*2)) 
        
        dp.setOwner(self._player)
        self._pileManager.addPlayerPile(dp)
        
    def forgetOldPile(self):
        lostPile = random.choice(self._pileManager.getPlayerPiles())
        self._pileManager.abandonPile(lostPile)
                  
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

    def spawnAcorn(self):
        """Spawn a new acorn on the map"""
        x_coordinate = random.randint(0,self._world_size[0])
        y_coordinate = random.randint(0,self._world_size[1])
        position = (x_coordinate, y_coordinate)
        self._acorns.append(Acorn(position))

    def spawnAbandonedPile(self):
        """Spawn a new abandoned pile on the map"""
        x_coordinate = random.randint(0,self._world_size[0])
        y_coordinate = random.randint(0,self._world_size[1])
        position = (x_coordinate, y_coordinate)
        name = "Abandoned Pile"
        acornsInPile = random.randint(1,20)
        d = DirtPile(position, name)
        d.setAcorns(acornsInPile)
        self._pileManager.addSpawnedPile(d)

    def takeStarveDamage(self):
        """Apply negative effects to starving player"""
        self._player.loseHealth(5)
        self._player.loseStamina(5)

    def leakAcorns(self):
        """Calculate and execute acorn leakage"""
        percentLoss = random.randint(25,33) / 100 # Between 25 and 33 percent
        overflowAcorns = self._player.getAcorns() - self._player.getCheekCapacity()
        loss = round(overflowAcorns * percentLoss)
        self._player.setAcorns(self._player.getAcorns() - loss)

    def updateTimers(self, ticks):
        """Update and maintain the in-game timers"""
        self._acornSpawnTimer.update(ticks, self.spawnAcorn)
        self._pileSpawnTimer.update(ticks, self.spawnAbandonedPile)
        self._hungerTimer.update(ticks, self._player.decrementHunger)

        if self._player.isStarving():
            self._starveTimer.update(ticks, self.takeStarveDamage)
        else:
            self._starveTimer.resetTimer()

        # Control acorn leakage if the player is carrying too many acorns
        if self._player.getAcorns() > self._player.getCheekCapacity():
            if self._leak == False:
                self._leak = True
                self._popupWindow.setText("You are carrying too many acorns!\nStash them or you'll drop them")
                self._popupWindow.display()
                self._player.stop()
            self._acornLeakTimer.update(ticks, self.leakAcorns)         
        else:
            self._acornLeakTimer.resetTimer()
            self._leak = False

        # Update the grace period between attacks
        self._graceTimer -= ticks

        # Update the interaction timer (used to prevent instantaneous button clicks)
        if  self._interaction != None and self._interaction.getDisplay() and self._interactionTimer >= 0:
            self._interactionTimer -= ticks

    def updateAcorns(self, ticks):
        for acorn in self._acorns:
            playerTouchingAcorn = acorn.getCollideRect().colliderect(self._player.getCollideRect())
            playerHasRoomToCollect = self._player.getAvailableCheekSpace() > 0
            if  playerTouchingAcorn and playerHasRoomToCollect:
                self._player.addAcorns(1)
                acorn.collected()
            acorn.update(ticks)

        # Remove acorns that have been collected
        self._acorns = [acorn for acorn in self._acorns if not acorn.isCollected()]

    def updateNightFilter(self):
        currentTime = self._worldClock.getTime()
        newAlpha = round((-100*math.sin((math.pi /60)*(currentTime-5)))+100)
        self._nightFilter.setAlpha(newAlpha)

    def updateEnvironment(self, ticks):
        self.updateAcorns(ticks)
        for pile in self._pileManager.getSpawnedPiles():
            pile.update(ticks)
        self.updateNightFilter()

    def checkAndMaintainPackPopulation(self):
        """Spawn new packs if the pack population has fallen below the default"""
        tooFewPacks = len(self._packs) < self._packPopulation
        if tooFewPacks:
            packsNeeded = self._packPopulation - len(self._packs)
            x_coordinate = self._world_size[0]-128
            y_coordinate = self._world_size[1]+128
            position = (x_coordinate, y_coordinate)
            entitiesToAvoidOverlapping = self._merchants + self._trees + [p.getLeader() for p in self._packs]
            pack = spawnPacks(position, packsNeeded, entitiesToAvoidOverlapping)
            self._packs += pack

    def removeDeadPacksFromGame(self):
        self._packs = [pack for pack in self._packs if not pack.isDead()]

    def updatePacks(self, ticks):
        self.removeDeadPacksFromGame()
        self.checkAndMaintainPackPopulation()
        for pack in self._packs: 
            pack.getLeader().wander(ticks)
            if pack.trueLen() > 1:
                pack.update(self._world_size, ticks)

    def updateEntities(self, ticks):
        for merchant in self._merchants:
            merchant.update(ticks)
        self._player.update(self._world_size, ticks)
        self.updatePacks(ticks)
        self._playerPack.update(self._world_size, ticks)
        
    def updateUI(self, ticks):
        if self._bribeWindow != None and self._bribeWindow.getDisplay():
            self._bribeWindow.update()
        if self._stealWindow != None and self._stealWindow.getDisplay():
            self._stealWindow.update()
        self._stats.update()
        self._hud.update(ticks)
        self._weapon.updateBlock()
        self._armor.updateBlock()
        self._packManager.update(ticks)

    def updateViewOffset(self):
        self._player.updateOffset(self._player, self._screen_size, self._world_size)

    def onDayChange(self):
        self._player.addXP(self._xpPerDay)

    def update(self, ticks):
        """Update the main level based on ticks from the game clock"""
        self.updateEnvironment(ticks)
        self.updateTimers(ticks)
        self.updateEntities(ticks)
        self.updateUI(ticks)
        self._worldClock.update(ticks)
        self.updateViewOffset()
        # Check if a day has passed in game time
        if self._worldClock.dayPassed():
            self.onDayChange()
        # Load and play a new song if the current song has ended
        SOUNDS.manageSongs("main")
        


