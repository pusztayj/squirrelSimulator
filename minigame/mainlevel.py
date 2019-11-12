import pygame, random, math
from graphics import Banner, Popup, StatDisplay, Mask
from modules.vector2D import Vector2
from modules.drawable import Drawable
from player import Player
from economy.acorn import Acorn
from economy.dirtpile import DirtPile
from minigame.atm import ATM
from animals.chipmunk import Chipmunk
from animals.fox import Fox
from minigame.interaction import Interaction
from level import Level
from economy.merchant import Merchant
from minigame.worldclock import WorldClock
from modules.soundManager import SoundManager
from minigame.inventoryhud import InventoryHUD
from items.items import Food

def spawn(spawnType, spawnRange, spawnCount, collidables, name=None):
    spawns = []
    while len(spawns) < spawnCount:
        if name == None:
            e = spawnType(pos=(random.randint(0,spawnRange[0]),
                                 random.randint(0,spawnRange[1])))
        else:
            e = spawnType(name,(random.randint(0,spawnRange[0]),
                                 random.randint(0,spawnRange[1])))
        if e.getCollideRect().collidelist([x.getCollideRect() for x in spawns + collidables]) == -1:
            spawns.append(e)
    return spawns

class MainLevel(Level):

    def __init__(self, player, SCREEN_SIZE):

        super().__init__()

        self._SCREEN_SIZE = SCREEN_SIZE
        self._WORLD_SIZE = (2000,1000)

        self._font = pygame.font.SysFont("Times New Roman", 32)
        self._popupFont = pygame.font.SysFont("Times New Roman", 16)

        self._songs = ["main1.mp3","main2.mp3","main3.mp3","main4.mp3"]
        self._currentSong = random.choice(self._songs)

        self._worldClock = WorldClock(self._SCREEN_SIZE[0])

        self._player = player

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
        self._fox = Fox(pos=(800,200))
        self._fox.flip()
        self._fox.scale(1.5)
        self._creatures.append(self._fox)
        self._creatures.append(self._chip)
        self._creatures.append(self._player)

        self._atm = None

        self._interaction = None

        # Add merchants to the world
        self._merchants = spawn(Merchant, (self._WORLD_SIZE[0]-128, self._WORLD_SIZE[1]+128),
                                random.randint(2,5), [])

        # Add trees to the world
        self._trees = spawn(Drawable, (self._WORLD_SIZE[0]-128, self._WORLD_SIZE[1]+128),
                            30, self._merchants, "tree.png")

        self._hud = InventoryHUD(((self._SCREEN_SIZE[0]//2)-350,
                                  self._SCREEN_SIZE[1]-52), (700,50), player)

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

        for merchant in notDrawnMerchants:
            merchant.draw(screen)

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

        self._hud.draw(screen)

    def handleEvent(self, event):

        

        if self._atm == None or not self._atm.getDisplay():
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

            for creature in self._creatures:
                x,y = creature.getPosition()
                for rect in creature.getCollideRects():
                    r = rect.move(x,y)
                    if r.collidepoint((event.pos[0] + Drawable.WINDOW_OFFSET[0],
                                         event.pos[1] + Drawable.WINDOW_OFFSET[1])):
                        self._interaction = Interaction()
                        
            for merchant in self._merchants:
                if merchant.getCollideRect().collidepoint((event.pos[0] + Drawable.WINDOW_OFFSET[0],
                                         event.pos[1] + Drawable.WINDOW_OFFSET[1])):
                    return (1, merchant) # Set Game Mode to Merchant and provide merchant

        if event.type == pygame.MOUSEBUTTONDOWN and event.button==3:
            item = self._hud.getActiveItem()
            if item != None and issubclass(type(item), Food):
                self._player.getInventory().removeItem(item)
                self._player.eat(item._hungerBoost, item._healthBoost)
                

        if self._atm != None and self._atm.getDisplay():
            self._atm.handleEvent(event)

        if self._interaction != None and self._interaction.getDisplay():
            self._interaction.handleEvent(event)
            return (self._interaction.getSelection(),)


                

        mouse = pygame.mouse.get_pos()
        m_pos_offset = self._player.adjustMousePos(mouse)
        m_pos_offset = (m_pos_offset[0], m_pos_offset[1])   
        popup_pos = (mouse[0] + 5, mouse[1] + 5)
        self._popup = self.setPopup(self._creatures, m_pos_offset, popup_pos, self._popupFont)
        if self._popup==None:
            self._popup = self.setPopup(self._dirtPiles, m_pos_offset, popup_pos, self._popupFont)
        if self._popup == None:
            self._popup = self.setPopup(self._merchants, m_pos_offset, popup_pos, self._popupFont)


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

        self._hud.update()

        #self._fox.wander(1)

        if not pygame.mixer.music.get_busy():
            temp = self._currentSong
            while temp == self._currentSong:
                self._currentSong = random.choice(self._songs)
            SoundManager.getInstance().playMusic(self._currentSong)
        


