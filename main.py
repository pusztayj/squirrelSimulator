
import pygame, random
from graphics.banner import Banner
from graphics.textbox import TextBox
from graphics.textinput import TextInput
from graphics.popup import Popup
from modules.vector2D import Vector2
from modules.drawable import Drawable
from player import Player
from economy.acorn import Acorn
from economy.dirtpile import DirtPile
from minigame.atm import ATM
from animals.chipmunk import Chipmunk

SCREEN_SIZE = (1200,500)
WORLD_SIZE  = (2400,500)

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

   ground = Banner((0,300),(100,255,100),(500, 2400))

   acornCount = TextBox("Acorns: " + str(player.getAcorns()), (0,0), font, (255,255,255))
   
   acorns = []
   #for x in range(100):
   #   acorns.append(Acorn((random.randint(0,2400),random.randint(300,500))))

   dirtPiles = []

   acornSpawnTimer = random.randint(5,10)

   popup = None #Popup("Pop", (0,0), popupFont)

   creatures = []
   chip = Chipmunk(pos=(1600,300))
   chip.flip()
   creatures.append(chip)

   atm = None

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

      acornCount.draw(screen)

      for creature in creatures:
         creature.draw(screen)

      if popup != None:
         popup.draw(screen)

      if atm != None and atm.getDisplay():
         atm.draw(screen)

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
          
         for pile in dirtPiles:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button==3:
               if pile.getCollideRect().collidepoint((event.pos[0] + Drawable.WINDOW_OFFSET[0],
                                                  event.pos[1] + Drawable.WINDOW_OFFSET[1])):
                  atm = ATM(player, pile)
            pile.handleEvent(event, player)
            
         if atm != None and atm.getDisplay():
            atm.handleEvent(event)

         mouse = pygame.mouse.get_pos()
         m_pos_offset = player.adjustMousePos(mouse)
         m_pos_offset = (m_pos_offset[0], m_pos_offset[1])   
         popup_pos = (mouse[0] + 5, mouse[1] + 5)
         for creature in creatures:
            if creature.getCollideRect().collidepoint(m_pos_offset):
               popup = Popup(creature.getName(),popup_pos, popupFont)
            else: popup = None
               
      for acorn in acorns:
         if acorn.getCollideRect().colliderect(player.getCollideRect()) and \
            player.getCheekCapacity() - player.getAcorns() > 0:
            player.setAcorns(player.getAcorns() + 1)
            acorn.collected()
            
            
      #Calculate ticks
      ticks = gameClock.get_time() / 1000

      acornSpawnTimer -= ticks
      if acornSpawnTimer <= 0:
         acorns.append(Acorn((random.randint(0,2400),random.randint(300,500))))
         acornSpawnTimer = random.randint(5,10)

      #Update the player's position
      player.update(WORLD_SIZE, ticks)
      
      #Update the offset based on the player's location
      player.updateOffset(player, SCREEN_SIZE, WORLD_SIZE)

      dirtPiles = [pile for pile in dirtPiles if not pile.isEmpty()]

      #player.setAcorns(player.getAcorns() + len([acorn for acorn in acorns if acorn.isCollected()]))

      acorns = [acorn for acorn in acorns if not acorn.isCollected()]

      acornCount.setText("Acorns: " + str(player.getAcorns()))


   #Close the pygame window and quit pygame
   pygame.quit()

if __name__ == "__main__":
    main()

