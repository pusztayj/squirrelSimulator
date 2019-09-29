
import pygame, random, item, pack
from vector2D import Vector2
from drawable import Drawable
from squirrel import Squirrel
from chipmunk import Chipmunk
from combatGame import CombatGame
from fox import Fox
from bear import Bear
from snake import Snake
from textbox import TextBox

SCREEN_SIZE = (1200,500)
WORLD_SIZE  = (2400,500)

animals = [Chipmunk, Fox, Bear, Snake]

def main():

    #Initialize the module
    pygame.init()
    pygame.font.init()

    #Load in the desired font
    font = pygame.font.SysFont("Times New Roman", 32)

    #Update the title for the window
    pygame.display.set_caption('Combat GUI')
   
    #Get the screen
    screen = pygame.display.set_mode(SCREEN_SIZE)

    # Create the allies
    a1 = random.choice(animals)()
    a2 = random.choice(animals)()
    a3 = random.choice(animals)()
    stick1 = item.Stick(20)
    stick1.rename("Breath Taker")
    stick2 = item.Stick(10)
    stick2.rename("Call of the Wild")
    stick3 = item.Stick(15)
    stick3.rename("Bane of Bears")
    a1.equipTool(stick1)
    a2.equipTool(stick2)
    a3.equipTool(stick3)
    allies = pack.Pack(a1)
    allies.addMember(a2)
    allies.addMember(a3)

    # Create the enemies
    b1 = random.choice(animals)()
    b2 = random.choice(animals)()
    b3 = random.choice(animals)()
    enemies = pack.Pack(b1)
    enemies.addMember(b2)
    enemies.addMember(b3)

    #Begin the game
    game = CombatGame(allies, enemies)

    #Load the background image
    background = Drawable("combatBackground.png", Vector2(0,0))

    #Create a textbox for character names
    textBoxes = []
    y = 10
    for animal in allies:
        box = TextBox(animal.getName(), (10,y), font, (255,255,255))
        textBoxes.append(box)
        y += 160
    y = 10
    for animal in enemies:
        box = TextBox(animal.getName(), (1050,y), font, (255,255,255))
        animal.flip()
        textBoxes.append(box)
        y += 160

    instructions = TextBox("Combat Mode", (500,450), font, (0,0,0))
    title = TextBox("Combat Mode", (500,10), font, (0,0,0))

    #Create an instance of the game clock
    gameClock = pygame.time.Clock()

    allies = game.getAllies()
    enemies = game.getEnemies()
    player = allies.getLeader()

    RUNNING = True

    while RUNNING:
        #Increment the clock
        gameClock.tick()

        #Draw the background to the screen
        background.draw(screen)

        #Draw textboxes to the screen
        for box in textBoxes:
            box.draw(screen)
        title.draw(screen)
        instructions.draw(screen)

        #Draw the animals to the screen
        y = 20
        for animal in allies:
            animal.setPosition((100,y))
            animal.draw(screen)
            y+=150
        y = 20
        for animal in enemies:
            animal.setPosition((950,y))
            animal.draw(screen)
            y+=150


        pygame.display.flip()

        # event handling, gets all event from the eventqueue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT or K_ESCAPE
            if (event.type == pygame.QUIT) or \
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                # change the value to False, to exit the main loop
                RUNNING = False
                
        #Calculate ticks
        ticks = gameClock.get_time() / 1000

    #Close the pygame window and quit pygame
    pygame.quit()


    

def main1():
   """
   Main loop for the program
   """
   #Initialize the module
   pygame.init()

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

   player = Squirrel()

   chip = Chipmunk(pos=(100,100))

   RUNNING = True

   while RUNNING:

      #Increment the clock
      gameClock.tick()

      #Draw the background to the screen
      background.draw(screen)

      #Draw the player to the screen
      player.draw(screen)

      chip.draw(screen)

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
            
      #Calculate ticks
      ticks = gameClock.get_time() / 1000

      #Update the player's position
      player.update(WORLD_SIZE, ticks)
      
      #Update the offset based on the player's location
      player.updateOffset(player, SCREEN_SIZE, WORLD_SIZE)


   #Close the pygame window and quit pygame
   pygame.quit()

if __name__ == "__main__":

    main()

