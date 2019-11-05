import pygame, random, math
from graphics.banner import Banner
from graphics.textbox import TextBox
from graphics.textinput import TextInput
from graphics.popup import Popup
from graphics.progressbar import ProgressBar
from graphics.statdisplay import StatDisplay
from graphics.mask import Mask
from modules.vector2D import Vector2
from modules.drawable import Drawable
from player import Player
from economy.acorn import Acorn
from economy.dirtpile import DirtPile
from minigame.atm import ATM
from animals.chipmunk import Chipmunk
from animals.turtle import Turtle
from minigame.interaction import Interaction
from level import Level
from economy.merchant import Merchant

class MainLevel(Level):

    def __init__(self, player, SCREEN_SIZE):

        super().__init__()

        self._SCREEN_SIZE = (1200,500)
        self._WORLD_SIZE = (2000,1000)

        self._font = pygame.font.SysFont("Times New Roman", 32)
        self._popupFont = pygame.font.SysFont("Times New Roman", 16)

        self._seasons = ["Spring", "Summer", "Fall", "Winter"]

        self._hour_length = 1 # ticks / seconds
        self._day_length = 24 * self._hour_length
        self._minute_length = self._hour_length / 60
        self._season_length = 2 #days
        self._year_length = self._season_length * 4

        self._current_season = 0

        self._player = player

        self._ground = Banner((0,0),(100,255,100),(self._WORLD_SIZE[1],self._WORLD_SIZE[0]))

        self._acorns = []
        self._dirtPiles = []

        # Create timers
        self._acornSpawnTimer = random.randint(5,10)
        self._hungerTimer = 2 * self._hour_length
        self._starveTimer = 2 * self._hour_length

        self._time = 0

        self._popup = None

        self._stats = StatDisplay((5,5),self._player)

        self._nightFilter = Mask((0,0),(1200,500),(20,20,50),150)

        self._txtDay = TextBox("Day: 1", (500,5), self._font, (255,255,255))
        self._txtHour = TextBox("12:00pm", (600,5), self._font, (255,255,255))
        self._txtSeason = TextBox(self._seasons[0], (575, 40), self._font, (255,255,255))

        self._creatures = []
        self._chip = Chipmunk(pos=(1600,300))
        self._chip.flip()
        self._creatures.append(self._chip)
        self._creatures.append(self._player)

        self._atm = None

        self._interaction = None

        self._merchants = [Merchant(pos=(random.randint(0,self._WORLD_SIZE[0]),
                                     random.randint(0,self._WORLD_SIZE[1])))
                           for x in range(random.randint(1,5))]

    def draw(self, screen):
        
        #Draw the background to the screen
        self._ground.draw(screen)

        for acorn in self._acorns:
            acorn.draw(screen)

        for pile in self._dirtPiles:
            pile.draw(screen)

        for creature in self._creatures:
            creature.draw(screen)

        for merchant in self._merchants:
            merchant.draw(screen)

        self._nightFilter.draw(screen)

        if self._popup != None:
            self._popup.draw(screen)

        self._stats.draw(screen)

        if self._atm != None and self._atm.getDisplay():
            self._atm.draw(screen)

        if self._interaction != None and self._interaction.getDisplay():
            self._interaction.draw(screen)

        self._txtDay.draw(screen)
        self._txtHour.draw(screen)
        self._txtSeason.draw(screen)

    def handleEvent(self, event):

        self._player.move(event, self._atm)

        # Allow the player to create dirt piles
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_b and \
            (self._atm == None or not self._atm.getDisplay())):
            dp = DirtPile((self._player.getX() + (self._player.getWidth() // 2),
                            self._player.getY() + (self._player.getHeight() // 2)))
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

        if self._atm != None and self._atm.getDisplay():
            self._atm.handleEvent(event)

        if self._interaction != None and self._interaction.getDisplay():
            self._interaction.handleEvent(event)

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
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
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
            self._hungerTimer = 2 * self._hour_length

        self._time += ticks

        self._nightFilter.setAlpha(math.sin(self._time/(self._day_length/4))*200)

        if self._player.isStarving():
            self._starveTimer -= ticks
            if self._starveTimer <= 0:
                self._player.loseHealth(5)
                self._player.loseStamina(5)
                self._starveTimer = 2 * self._hour_length
        else:
            self._starveTimer = 2 * self._hour_length

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
        self._txtDay.setText("Day: " + str(int(self._time // self._day_length)+1))
        self._txtHour.setText(str(int((self._time // self._hour_length) % 12)+1) + ":" +
                      str(int(self._time // self._minute_length)%60).zfill(2) + " " +
                      ("pm" if (int((self._time // self._hour_length) % 24)+1 >= 12) else "am"))

        self._current_season = int((((self._time // self._day_length) + 1) // self._season_length) % 4)
        self._txtSeason.setText(self._seasons[self._current_season])
        


