
import pygame, random, math
#from graphics.banner import Banner
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
from minigame.interaction import Interaction

SCREEN_SIZE = (1200,500)
WORLD_SIZE  = (2400,500)

def setPopup(lyst, mouse_pos, popup_pos, font):
   for entity in lyst:
      x,y = entity.getPosition()
      for rect in entity.getCollideRects():
         r = rect.move(x,y)
         if r.collidepoint(mouse_pos):
            return Popup(entity.getName(), popup_pos, font)
               
def main():
   """
   Main loop for the program
   """
   #Initialize the module
   pygame.init()
   pygame.font.init()

   font = pygame.font.SysFont("Times New Roman", 32)
   popupFont = pygame.font.SysFont("Times New Roman", 16)

   #Store the pygame key codes for simplicity later
   movement_keys = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]

   #Update the title for the window
   pygame.display.set_caption('Squirrel Simulator')
   
   #Get the screen
   screen = pygame.display.set_mode(SCREEN_SIZE)

   #Load the background image
   background = Drawable("background.png", Vector2(0,0))

   #Create an instance of the game clock
   gameClock = pygame.time.Clock()

   player = Player(pos=(600,300))
   player.scale(2)

   ground = Banner((0,300),(100,255,100),(500, 2400))

   acorns = []
   dirtPiles = []

   acornSpawnTimer = random.randint(5,10)

   time = 0

   popup = None #Popup("Pop", (0,0), popupFont)

   stats = StatDisplay((5,5),player)

   nightFilter = Mask((0,0),(1200,500),(20,20,50),150)
   
   creatures = []
   chip = Chipmunk(pos=(1600,300))
   chip.flip()
   creatures.append(chip)
   creatures.append(player)

   atm = None

   interaction = None

   RUNNING = True

   while RUNNING:

      #Increment the clock
      gameClock.tick()

      #Draw the background to the screen
      background.draw(screen)
      ground.draw(screen)

      for acorn in acorns:
         acorn.draw(screen)

      for pile in dirtPiles:
         pile.draw(screen)

      #Draw the player to the screen
      player.draw(screen)

      for creature in creatures:
         creature.draw(screen)

      nightFilter.draw(screen)

      if popup != None:
         popup.draw(screen)

      stats.draw(screen)

      if atm != None and atm.getDisplay():
         atm.draw(screen)

      if interaction != None and interaction.getDisplay():
         interaction.draw(screen)



      pygame.display.flip()

      # event handling, gets all event from the eventqueue
      for event in pygame.event.get():
         # only do something if the event is of type QUIT or K_ESCAPE
         if (event.type == pygame.QUIT) or \
             (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            # change the value to False, to exit the main loop
            RUNNING = False
            
         elif (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP) \
            and event.key in movement_keys:
            player.move(event)

         elif (event.type == pygame.KEYDOWN and event.key == pygame.K_b):
            if player.getAcorns() > 0:
                  dp = DirtPile((player.getX() + (player.getWidth() // 2),
                                      player.getY() + (player.getHeight() // 2)))
                  dp.addAcorn()
                  player.setAcorns(player.getAcorns() - 1)
                  dirtPiles.append(dp)
          


         if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
            for pile in dirtPiles:
               if pile.getCollideRect().collidepoint((event.pos[0] + Drawable.WINDOW_OFFSET[0],
                                                  event.pos[1] + Drawable.WINDOW_OFFSET[1])):
                  atm = ATM(player, pile)
                  pile.handleEvent(event, player)
            for creature in creatures:
               x,y = creature.getPosition()
               for rect in creature.getCollideRects():
                  r = rect.move(x,y)
                  if r.collidepoint((event.pos[0] + Drawable.WINDOW_OFFSET[0],
                                 event.pos[1] + Drawable.WINDOW_OFFSET[1])):
                     interaction = Interaction()
            
         if atm != None and atm.getDisplay():
            atm.handleEvent(event)

         if interaction != None and interaction.getDisplay():
            interaction.handleEvent(event)
            
         # Button inputs to be used for testing
         if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            player.loseHealth(10)
         if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            player.heal(10)
         if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            player.setAcorns(player.getAcorns() + 1)
         if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
            if nightFilter.getAlpha() == 0:
               nightFilter.setAlpha(150)
            else:
               nightFilter.setAlpha(0)

         mouse = pygame.mouse.get_pos()
         m_pos_offset = player.adjustMousePos(mouse)
         m_pos_offset = (m_pos_offset[0], m_pos_offset[1])   
         popup_pos = (mouse[0] + 5, mouse[1] + 5)
         popup = setPopup(creatures, m_pos_offset, popup_pos, popupFont)
         if popup==None:
            popup = setPopup(dirtPiles, m_pos_offset, popup_pos, popupFont)
            
      for acorn in acorns:
         if acorn.getCollideRect().colliderect(player.getCollideRect()) and \
            player.getCheekCapacity() - player.getAcorns() > 0:
            player.setAcorns(player.getAcorns()+1)
            acorn.collected()    
            
      #Calculate ticks
      ticks = gameClock.get_time() / 1000

      acornSpawnTimer -= ticks
      if acornSpawnTimer <= 0:
         acorns.append(Acorn((random.randint(0,2400),random.randint(300,500))))
         acornSpawnTimer = random.randint(5,10)

      time += ticks
##      print(time)

      nightFilter.setAlpha(math.sin(time/120)*200)

      #Update the player's position
      player.update(WORLD_SIZE, ticks)

      # Update the players stats
      stats.update()
      
      #Update the offset based on the player's location
      player.updateOffset(player, SCREEN_SIZE, WORLD_SIZE)

      # Remove acorns from the world that have been collected
      acorns = [acorn for acorn in acorns if not acorn.isCollected()]

   #Close the pygame window and quit pygame
   pygame.quit()

if __name__ == "__main__":
    main()

