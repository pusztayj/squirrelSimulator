import pygame, random, math
from graphics import Banner, Popup, StatDisplay, Mask, TextBox
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

creatures = [Bear, Fox, Rabbit, Deer]

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

    def __init__(self, player_pack, SCREEN_SIZE):

        super().__init__()

        self._SCREEN_SIZE = SCREEN_SIZE
        self._WORLD_SIZE = (4000,2000)

        self._font = pygame.font.SysFont("Times New Roman", 32)
        self._popupFont = pygame.font.SysFont("Times New Roman", 16)

        self._songs = ["main1.mp3","main2.mp3","main3.mp3","main4.mp3"]
        self._currentSong = random.choice(self._songs)

        self._worldClock = WorldClock(self._SCREEN_SIZE[0])

        self._playerPack = player_pack
        self._packManager = PackManager(self._playerPack, self._SCREEN_SIZE)
        self._player = self._playerPack.getLeader()

        self._ground = Banner((0,0),(100,255,100),(self._WORLD_SIZE[1],self._WORLD_SIZE[0]))

        self._acorns = []
        self._dirtPiles = []

        # Create timers
        self._acornSpawnTimer = random.randint(5,10)
        self._hungerTimer = 2 * self._worldClock.getHourLength()
        self._starveTimer = 2 * self._worldClock.getHourLength()

        self._popup = None

        self._stats = StatDisplay((5,5),self._player)

        self._nightFilter = Mask((0,0),(1200,500),(20,20,50),150)

        self._creatures = []
        self._chip = Chipmunk(pos=(1600,300))
        self._chip.flip()
        self._creatures.append(self._chip)

        self._atm = None

        self._interaction = None

        # Add merchants to the world
        self._merchants = spawn(Merchant, (self._WORLD_SIZE[0]-128, self._WORLD_SIZE[1]+128),
                                random.randint(2,5), [])

        # Add trees to the world
        self._trees = spawn(Drawable, (self._WORLD_SIZE[0]-128, self._WORLD_SIZE[1]+128),
                            30, self._merchants, name="tree.png")

        self._packs = spawnPacks((self._WORLD_SIZE[0]-128, self._WORLD_SIZE[1]+128),
                                 30,
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
                    creature.loseHealth(random.randint(20,80))
                    creature.setAcorns(random.randint(0,100))

        self._hud = InventoryHUD(((self._SCREEN_SIZE[0]//2)-350,
                                  self._SCREEN_SIZE[1]-52), (700,50), self._player)

        self._weapon = ItemBlock((SCREEN_SIZE[0]-164,5))
        self._armor = ItemBlock((SCREEN_SIZE[0]-82,5))

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

        for creature in self._creatures:
            creature.draw(screen)

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

    def handleEvent(self, event):

        if (self._atm == None or not self._atm.getDisplay()) and \
           (self._interaction == None or not self._interaction.getDisplay()):
            self._hud.handleEvent(event)
            self._player.move(event, self._atm)
            
            # Allow the player to create dirt piles
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                if self._player.isFlipped():
                    dp = DirtPile((self._player.getX() - (3//4)*(self._player.getWidth() // 2),
                            self._player.getY() + (self._player.getHeight() // 3)))
                else:
                    dp = DirtPile((self._player.getX() + (self._player.getWidth() // 2),
                            self._player.getY() + (self._player.getHeight() // 3)))
                self._dirtPiles.append(dp)
            

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
                

        if self._atm != None and self._atm.getDisplay():
            self._atm.handleEvent(event)

        if self._packManager.getDisplay():
            self._packManager.handleEvent(event)

        if self._interaction != None and self._interaction.getDisplay():
            self._popup = None
            self._interaction.handleEvent(event)
            code = self._interaction.getSelection()
            if (code == 2):
                return (code,)
            elif (code == 3):
                e = self._interaction.getEntity()
                if self._playerPack.trueLen() < 3:
                    if e.getPack().trueLen() == 1:
                        self._playerPack.addMember(e)
                        self._packs.remove(e.getPack())
                        e.getPack().removeMember(e)
                        e.setPack(self._playerPack)
                        print("Let's Be Friends..." + e.getName())
                    else:
                        print(e.getName(), "is already part of a pack")
                else:
                    print("Your pack is already full")

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
        if self._popup == None:
            self._popup = self.setPopup(self._merchants, m_pos_offset, popup_pos, self._popupFont)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            if self._packManager._timeSinceClosed > self._packManager._delay:
                self._packManager.display()

        # Code for testing
        if event.type == pygame.KEYDOWN and event.key == pygame.K_o:
            self._player.setAcorns(self._player.getAcorns()+1)



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
            self._acornSpawnTimer = random.randint(5,10)

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

        if self._player.isDead():
            print("The Player is Dead")

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

        for pack in self._packs:
            pack.getLeader().wander(ticks)
            pack.update(self._WORLD_SIZE, ticks)

        if not pygame.mixer.music.get_busy():
            temp = self._currentSong
            while temp == self._currentSong:
                self._currentSong = random.choice(self._songs)
            SoundManager.getInstance().playMusic(self._currentSong)
        


