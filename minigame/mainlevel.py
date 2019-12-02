import pygame, random, math
from graphics import *
from modules.vector2D import Vector2
from modules.drawable import Drawable
from player import Player
from economy.acorn import Acorn
from economy.dirtpile import DirtPile
from minigame.atm import ATM
from animals import *
from minigame.interaction import Interaction
from level import Level
from economy.merchant import Merchant
from minigame.worldclock import WorldClock
from modules.soundManager import SoundManager
from minigame.inventoryhud import InventoryHUD
from items.items import *
from items import items
from minigame.itemblock import ItemBlock
from minigame.packmanager import PackManager
from minigame.bribe import Bribe
from minigame.steal import Steal
from minigame.xpmanager import XPManager

creatures = [Bear, Fox, Rabbit, Deer, Chipmunk, Hedgehog]

def createPack(pos):
    leader = random.choice(creatures)(pos=pos)
    p = Pack(leader)
    leader.setPack(p)
    for x in range(2):
        if random.random() < .25:
            c = random.choice(creatures)(pos=(pos[0]+(((-1)**x)*30),
                                                      pos[1]+(((-1)**x)*30)))
            c.setPack(p)
            p.addMember(c)
    return p

def spawnPacks(spawnRange, spawnCount, collidables):
    spawns = []
    packs = []
    while len(packs) < spawnCount:
        e = createPack((random.randint(0,spawnRange[0]), random.randint(0,spawnRange[1])))
        if e.getLeader().getWanderRect().collidelist([x.getCollideRect() for x in spawns + collidables]) == -1:
            spawns.append(e.getLeader())
            packs.append(e)
    return packs

def spawn(spawnType, spawnRange, spawnCount, collidables, name=None, wanderer=False):
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

    def __init__(self, player_pack, SCREEN_SIZE, cheatBox):

        super().__init__()

        self._xpPerDay = 1

        self._attackThreshold = 20

        self._cheatBox = cheatBox

        self._SCREEN_SIZE = SCREEN_SIZE
        self._WORLD_SIZE = (4000,2000)

        self._font = pygame.font.SysFont("Times New Roman", 32)
        self._popupFont = pygame.font.SysFont("Times New Roman", 16)
        self._messageFont = pygame.font.SysFont("Times New Roman", 20)

        self._songs = ["main1.mp3","main2.mp3","main3.mp3","main4.mp3"]
        self._currentSong = random.choice(self._songs)

        self._worldClock = WorldClock(self._SCREEN_SIZE[0])

        self._playerPack = player_pack
        self._packManager = PackManager(self._playerPack, self._SCREEN_SIZE)
        self._player = self._playerPack.getLeader()

        self._ground = Banner((0,0),(100,255,100),(self._WORLD_SIZE[1],self._WORLD_SIZE[0]))

        self._acorns = [Acorn((random.randint(0,self._WORLD_SIZE[0]),
                                       random.randint(0,self._WORLD_SIZE[1]))) for x in range(random.randint(20,30))]
        self._dirtPiles = []

        self._spawnedPiles = []

        # Create timers
        self._acornSpawnTimer = random.randint(2,5)
        self._pileSpawnTimer = random.randint(20,40)
        self._hungerTimer = 2 * self._worldClock.getHourLength()
        self._starveTimer = 2 * self._worldClock.getHourLength()

        self._interactionDelay = 0.1 #Prevent buttons from being clicked when interaction opens
        self._interactionTimer = self._interactionDelay

        self._popup = None

        # Create the popup window
        self._popupWindow = PopupWindow("", (0,0), (288,100), self._messageFont,
                                        (255,255,255),(0,0,0), (120,120,120), (40,20),
                                        self._popupFont,(255,255,255), borderWidth=1)
        self._popupWindow.setPosition((SCREEN_SIZE[0]//2 - self._popupWindow.getWidth()//2,
                                       SCREEN_SIZE[1]//3 - self._popupWindow.getHeight()//2))
        self._popupWindow.close()

        # Create the confirmation window
        self._confirmationWindow = ConfirmationWindow("", (0,0), (288,150), self._messageFont,
                                        (255,255,255),(0,0,0), (120,120,120), (40,20),
                                        self._popupFont,(255,255,255), borderWidth=1)
        self._confirmationWindow.setPosition((SCREEN_SIZE[0]//2 - self._confirmationWindow.getWidth()//2,
                                       SCREEN_SIZE[1]//3 - self._confirmationWindow.getHeight()//2))
        self._confirmationWindow.close()
        self._confirmationProceedure = None

        self._stats = StatDisplay((5,5),self._player)

        self._nightFilter = Mask((0,0),(1200,500),(20,20,50),150, False)

        self._atm = None

        self._interaction = None

        # Add merchants to the world
        self._merchants = spawn(Merchant, (self._WORLD_SIZE[0]-128, self._WORLD_SIZE[1]+128),
                                random.randint(2,5), [])

        # Add trees to the world
        self._trees = spawn(Drawable, (self._WORLD_SIZE[0]-128, self._WORLD_SIZE[1]+128),
                            30, self._merchants, name="tree.png")

        self._packs = spawnPacks((self._WORLD_SIZE[0]-128, self._WORLD_SIZE[1]+128),
                                 20,
                                 self._merchants + self._trees)
        
        for pack in self._packs:
            for creature in pack:
                if creature != None:
                    for _ in range(2):
                        i = items.__all__
                        random.shuffle(i)
                        for x in i:
                            if .08 >= random.random():
                                creature.getInventory().addItem(globals()[x]())
                    if random.random() < .33:
                        creature.equipArmor(random.choice(items.armors)())
                    if random.random() < .33:
                        creature.equipItem(random.choice(items.weapons)())
                    creature.loseHealth(random.randint(0,20))
                    creature.setAcorns(random.randint(0,100))

        self._hud = InventoryHUD(((self._SCREEN_SIZE[0]//2)-350,
                                  self._SCREEN_SIZE[1]-52), (700,50), self._player)

        self._weapon = ItemBlock((SCREEN_SIZE[0]-164,5))
        self._armor = ItemBlock((SCREEN_SIZE[0]-82,5))

        self._bribeWindow = None
        self._stealWindow = None

        self._fightFlag = (False,)

        self._xpManager = XPManager((SCREEN_SIZE[0]//2 - 250//2, 80), self._player)
        self._xpManager.close()

        SoundManager.getInstance().playMusic(self._currentSong)

    def setActive(self, boolean):
        self._active = boolean
        self._currentSong = random.choice(self._songs)
        SoundManager.getInstance().playMusic(self._currentSong)

    def draw(self, screen):
        
        #Draw the background to the screen
        self._ground.draw(screen)

        for acorn in self._acorns:
            acorn.draw(screen)

        for pile in self._dirtPiles:
            pile.draw(screen)

        for pile in self._spawnedPiles:
            pile.draw(screen)

        notDrawnTrees = []
        playerY = self._player.getY()
        for tree in self._trees:
            treeY = tree.getY()
            treeHeight = tree.getHeight()
            if playerY > (treeY + treeHeight) - (self._player.getHeight()-4):
                tree.draw(screen)
            else:
                notDrawnTrees.append(tree)

        notDrawnMerchants = []
        for merch in self._merchants:
            merchY = merch.getY()
            merchHeight = merch.getHeight()
            if playerY > (merchY + merchHeight) - self._player.getHeight():
                merch.draw(screen)
            else:
                notDrawnTrees.append(merch)

        self._playerPack.draw(screen)

        for pack in self._packs:
            pack.draw(screen)

        for merchant in notDrawnMerchants:
            merchant.draw(screen)

        self._player.draw(screen)

        for tree in notDrawnTrees:
            tree.draw(screen)

        self._nightFilter.draw(screen)

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

        if (self._atm == None or not self._atm.getDisplay()) and \
           (self._interaction == None or not self._interaction.getDisplay()) and \
           (not self._packManager.getDisplay()) and \
           (not self._popupWindow.getDisplay()) and \
           (not self._confirmationWindow.getDisplay()) and \
           (not self._cheatBox.isDisplayed()):
            self._hud.handleEvent(event)
            self._player.move(event, self._atm)
            
            # Allow the player to create dirt piles
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
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

            if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
                for pile in self._dirtPiles:
                    if pile.getCollideRect().collidepoint((event.pos[0] + Drawable.WINDOW_OFFSET[0],
                              event.pos[1] + Drawable.WINDOW_OFFSET[1])):
                        self._atm = ATM(self._player, pile)
                        
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
                                    for k in self._player._movement.keys(): self._player._movement[k] = False
                            
                for merchant in self._merchants:
                    if merchant.getCollideRect().collidepoint((event.pos[0] + Drawable.WINDOW_OFFSET[0],
                                             event.pos[1] + Drawable.WINDOW_OFFSET[1])):
                        return (1, merchant) # Set Game Mode to Merchant and provide merchant

            if event.type == pygame.MOUSEBUTTONDOWN and event.button==3:
                
                item = self._hud.getActiveItem()
                
                if item != None and issubclass(type(item), items.Food):
                    self._player.getInventory().removeItem(item)
                    self._player.eat(item._hungerBoost, item._healthBoost)
                    
                if item != None and type(item) == items.Shovel:
                    for pile in self._spawnedPiles:
                        if pile.getCollideRect().collidepoint((event.pos[0] + Drawable.WINDOW_OFFSET[0],
                              event.pos[1] + Drawable.WINDOW_OFFSET[1])):
                            if self._player.getAcorns() + pile.getAcorns() > self._player.getCheekCapacity():
                                self._confirmationWindow.setText("Are you sure you want to\n dig up this acorn pile?\nYou" + \
                                                                 " won't collect all the acorns")
                                self._confirmationWindow.display()
                                self._confirmationProceedure = (2, pile) #Redirect neccessary information
                            else:
                                self._spawnedPiles.remove(pile)
                                acorns = pile.getAcorns()
                                self._player.setAcorns(min(self._player.getCheekCapacity(), self._player.getAcorns() + acorns))
                            

                    for pile in self._dirtPiles:
                        if pile.getCollideRect().collidepoint((event.pos[0] + Drawable.WINDOW_OFFSET[0],
                              event.pos[1] + Drawable.WINDOW_OFFSET[1])):
                            self._confirmationWindow.setText("Are you sure you want to\n dig up your acorn pile?")
                            self._confirmationWindow.display()
                            self._confirmationProceedure = (0, pile) #Redirect neccessary information
                            
                            
                if item != None and issubclass(type(item), items.Weapon):
                    previous = self._weapon.getItem()
                    if previous != None:
                        self._player.getInventory().addItem(previous)
                    self._player.equipItem(item)
                    self._weapon.setItem(item)
                    self._player.getInventory().removeItem(item)
                if item != None and issubclass(type(item), items.Armor):
                    previous = self._armor.getItem()
                    if previous != None:
                        self._player.getInventory().addItem(previous)
                    self._player.equipArmor(item)
                    self._armor.setItem(item)
                    self._player.getInventory().removeItem(item)

                if item != None and issubclass(type(item), items.Potions):
                    self._player.getInventory().removeItem(item)
                    self._player.heal(item.getHealthBoost())

        if not self._popupWindow.getDisplay() and \
           (self._bribeWindow==None or not self._bribeWindow.getDisplay()) and \
           not self._confirmationWindow.getDisplay() and \
           (self._stealWindow==None or not self._stealWindow.getDisplay()):
            if self._atm != None and self._atm.getDisplay():
                self._atm.handleEvent(event)

            if self._packManager.getDisplay():
                c = self._packManager.handleEvent(event)
                if c != None and c[0] == 9:
                    self._playerPack.removeMember(c[1])
                    clone = c[1].clone()
                    clone.changeFriendScore(random.randint(-25,-5))
                    p = Pack(clone)
                    self._packs.append(p)
                    clone.setPack(p)

            if self._interaction != None and self._interaction.getDisplay() and self._interactionTimer < 0:
                self._popup = None
                self._interaction.handleEvent(event)
                code = self._interaction.getSelection()
                if (code == 2):
                    enemyPack = self._interaction.getEntity().getPack()
                    for e in enemyPack:
                        if e != None:
                            e.changeFriendScore(random.randint(-30,-10))
                    self._interaction = None
                    return (code,self._playerPack,enemyPack)
                elif (code == 3):
                    e = self._interaction.getEntity()
                    if self._playerPack.trueLen() < 3:
                        if e.getPack().trueLen() == 1:
                            if e.getFriendScore() + (self._player.getCharisma() * .5) > 60:
                                self._playerPack.addMember(e)
                                self._packs.remove(e.getPack())
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
                elif (code == 4):
                    e = self._interaction.getEntity()
                    self._bribeWindow = Bribe(self._player, e, self._SCREEN_SIZE)
                    self._bribeWindow.display()
                elif (code == 5):
                    e = self._interaction.getEntity()
                    self._stealWindow = Steal(self._player, e, self._SCREEN_SIZE)
                    self._stealWindow.display()

        mouse = pygame.mouse.get_pos()
        m_pos_offset = self._player.adjustMousePos(mouse)
        m_pos_offset = (m_pos_offset[0], m_pos_offset[1])   
        popup_pos = (mouse[0] + 5, mouse[1] + 5)

        creatures = []
        for pack in self._packs:
            for creature in pack:
                if creature != None:
                    creatures.append(creature)
        for creature in self._playerPack:
            if creature != None:
                creatures.append(creature)
        
        self._popup = self.setPopup(creatures, m_pos_offset, popup_pos, self._popupFont)
        if self._popup==None:
            self._popup = self.setPopup(self._dirtPiles, m_pos_offset, popup_pos, self._popupFont)
        if self._popup==None:
            self._popup = self.setPopup(self._spawnedPiles, m_pos_offset, popup_pos, self._popupFont)
        if self._popup == None:
            self._popup = self.setPopup(self._merchants, m_pos_offset, popup_pos, self._popupFont)

        if (self._atm == None or not self._atm.getDisplay()) and \
           (self._interaction == None or not self._interaction.getDisplay()) and \
           (not self._popupWindow.getDisplay()) and \
           not self._xpManager.getDisplay() and \
           not self._confirmationWindow.getDisplay() and \
           not self._cheatBox.isDisplayed():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                if self._packManager._timeSinceClosed > self._packManager._delay:
                    self._packManager.display()
                    for k in self._player._movement.keys(): self._player._movement[k] = False

        if (self._atm == None or not self._atm.getDisplay()) and \
           (self._interaction == None or not self._interaction.getDisplay()) and \
           (not self._popupWindow.getDisplay()) and \
           not self._packManager.getDisplay() and \
           not self._confirmationWindow.getDisplay() and \
           not self._cheatBox.isDisplayed():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                if self._xpManager.getDisplay():
                    self._xpManager.close()
                else:
                    self._xpManager.display()
                    for k in self._player._movement.keys(): self._player._movement[k] = False

        if self._confirmationWindow.getDisplay():
            c = self._confirmationWindow.handleEvent(event)
            if c == 1 and self._confirmationProceedure!=None:
                # Dig up a players acorn pile
                if self._confirmationProceedure[0] == 0:
                    pile = self._confirmationProceedure[1]
                    self._dirtPiles.remove(pile)
                    acorns = pile.getAcorns()
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
                    self._spawnedPiles.remove(pile)
                    acorns = pile.getAcorns()
                    self._player.setAcorns(min(self._player.getCheekCapacity(), self._player.getAcorns() + acorns))

        if self._bribeWindow != None and self._bribeWindow.getDisplay():
            self._bribeWindow.handleEvent(event)
            self._interaction.updateInteraction()

        if self._stealWindow != None and self._stealWindow.getDisplay():
            bustedRobbery = self._stealWindow.handleEvent(event)
            self._interaction.updateInteraction()
            if bustedRobbery:
                self._popupWindow.setText("You have been caught!\nPrepare for a fight")
                self._popupWindow.display()
                self._fightFlag = (True, self._interaction.getEntity().getPack()) #Start Combat on okay

        if self._xpManager.getDisplay() and not self._popupWindow.getDisplay() and \
           not self._confirmationWindow.getDisplay():
            c = self._xpManager.handleEvent(event)
            if c != None:
                if c[0] == 0:
                    self._popupWindow.setText("You do not have any XP")
                    self._popupWindow.display()
                ##if c[0] == 1:
                ##    self._popupWindow.setText(c[1] + " upgraded")
                ##    self._popupWindow.display()

##        for pack in self._packs:
##            leader = pack.getLeader()
##            rect = leader.getWanderRect()
##            if leader.getFriendScore() < self._attackThreshold:
##                if self._player.getCollideRect().colliderect(rect):
##                    self._popupWindow.setText("You entered enemy territory!\nPrepare for a fight")
##                    self._popupWindow.display()
##                    for k in self._player._movement.keys(): self._player._movement[k] = False
##                    self._fightFlag = (True, leader.getPack()) #Start Combat on okay

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

        for acorn in self._acorns:
            if acorn.getCollideRect().colliderect(self._player.getCollideRect()) and \
                self._player.getCheekCapacity() - self._player.getAcorns() > 0:
                self._player.setAcorns(self._player.getAcorns()+1)
                acorn.collected()
            acorn.update(ticks)

        self._acornSpawnTimer -= ticks
        if self._acornSpawnTimer <= 0:
            self._acorns.append(Acorn((random.randint(0,self._WORLD_SIZE[0]),
                                       random.randint(0,self._WORLD_SIZE[1]))))
            self._acornSpawnTimer = random.randint(2,5)

        # Spawn Abandoned Piles around the map
        self._pileSpawnTimer -= ticks
        if self._pileSpawnTimer <=0:
            d = DirtPile((random.randint(0,self._WORLD_SIZE[0]),
                          random.randint(0,self._WORLD_SIZE[1])),
                         "Abandoned Pile")
            d.setAcorns(random.randint(1,20))
            self._spawnedPiles.append(d)
            self._pileSpawnTimer = random.randint(20,40)

        self._hungerTimer -= ticks
        if self._hungerTimer <= 0:
            self._player.decrementHunger()
            self._hungerTimer = 2 * self._worldClock.getHourLength()

        self._nightFilter.setAlpha(math.sin(self._worldClock.getTime()/
                                            (self._worldClock.getDayLength()
                                             /4))*200)

        if self._player.isStarving():
            self._starveTimer -= ticks
            if self._starveTimer <= 0:
                self._player.loseHealth(5)
                self._player.loseStamina(5)
                self._starveTimer = 2 * self._worldClock.getHourLength()
        else:
            self._starveTimer = 2 * self._worldClock.getHourLength()

        if  self._interaction != None and self._interaction.getDisplay() and self._interactionTimer >= 0:
            self._interactionTimer -= ticks

        if self._bribeWindow != None and self._bribeWindow.getDisplay():
            self._bribeWindow.update()

        if self._stealWindow != None and self._stealWindow.getDisplay():
            self._stealWindow.update()

        #Update the player's position
        self._player.update(self._WORLD_SIZE, ticks)

        # Update the players stats
        self._stats.update()

        #Update the offset based on the player's location
        self._player.updateOffset(self._player, self._SCREEN_SIZE, self._WORLD_SIZE)

        # Remove acorns from the world that have been collected
        self._acorns = [acorn for acorn in self._acorns if not acorn.isCollected()]

        #Update InGame Clock
        self._worldClock.update(ticks)

        self._hud.update(ticks)

        self._weapon.updateBlock()
        self._armor.updateBlock()

        self._playerPack.update(self._WORLD_SIZE, ticks)
        
        self._packManager.update(ticks)

        self.packs = [pack for pack in self._packs if not pack.isDead()]

        for pack in self._packs: 
            pack.getLeader().wander(ticks)
            if pack.trueLen() > 1:
                pack.update(self._WORLD_SIZE, ticks)

        if self._worldClock.dayPassed():
            self._player.setXP(self._player.getXP() + self._xpPerDay)

        if not pygame.mixer.music.get_busy():
            temp = self._currentSong
            while temp == self._currentSong:
                self._currentSong = random.choice(self._songs)
            SoundManager.getInstance().playMusic(self._currentSong)
        


