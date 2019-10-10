
import pygame, random
##from items.item import Item
from animals.pack import Pack
from modules.vector2D import Vector2
from modules.drawable import Drawable
from animals.squirrel import Squirrel
from animals.chipmunk import Chipmunk
from animals.cow import Cow
from animals.deer import Deer
from combatGame import CombatGame
from animals.fox import Fox
from animals.bear import Bear
from animals.snake import Snake
from animals.rabbit import Rabbit
from graphics.textbox import TextBox
from graphics.button import Button
from graphics.banner import Banner
from graphics.scrollbox import ScrollBox
from animals.shmoo import Shmoo
from animals.hedgehog import HedgeHog
from graphics.mysurface import MySurface
from graphics import guiUtils
from items.items import *

SCREEN_SIZE = (1200,500)
WORLD_SIZE  = (2400,500)

animals = [Chipmunk, Fox, Bear, Snake, Deer, Rabbit, Shmoo, HedgeHog, Cow]

def attackButtonFunc():
    print("Set Attack")

def blockButtonFunc():
    print("Set Block")

def useItemButtonFunc():
    print("Set Use Item")

def retreatButtonFunc():
    print("Set Retreat")

def backButtonFunc():
    print("Set Back")

def main():

    #Initialize the module
    pygame.init()
    pygame.font.init()

    #Load in the desired font
    font = pygame.font.SysFont("Times New Roman", 32)
    font2 = pygame.font.SysFont("Times New Roman", 16)

    #Update the title for the window
    pygame.display.set_caption('Combat GUI')
   
    #Get the screen
    screen = pygame.display.set_mode(SCREEN_SIZE)

    # Create the allies
    a1 = random.choice(animals)()
    a2 = random.choice(animals)()
    a3 = random.choice(animals)()
    stick1 = Stick(level=20)
    stick1.rename("Breath Taker")
    stick2 = Stick(level=10)
    stick2.rename("Call of the Wild")
    stick3 = Stick(level=15)
    stick3.rename("Bane of Bears")
    a1.getInventory().addItem(Berries())
    a1.equipTool(stick1)
    a2.equipTool(stick2)
    a3.equipTool(stick3)
    allies = Pack(a1)
    allies.addMember(a2)
    allies.addMember(a3)

    # Create the enemies
    b1 = random.choice(animals)()
    b2 = random.choice(animals)()
    b3 = random.choice(animals)()
    enemies =Pack(b1)
    enemies.addMember(b2)
    enemies.addMember(b3)

    #Begin the game
    game = CombatGame(allies, enemies)

    player = allies.getLeader()

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

    instructions = TextBox("Select a Target", (500,450), font, (0,0,0))
    
    title = TextBox("Combat Mode", (500,10), font, (0,0,0))

    # Create Buttons
    confirmButton = Button("Confirm", (750,440), font, (0,0,0), (200,200,200), 40, 125,
                           (0,0,0), 5)

    attackButton = Button("Attack", (320,440), font, (0,100,0), (0,210,0), 40, 125,
                          (0,128,0), 2)

    useItemButton = Button("Use Item", (470,440), font, (0,0,100), (40,200,195), 40, 125,
                          (0,0,128), 2)

    blockButton = Button("Block", (620,440), font, (94,81,39), (213,175,53), 40, 125,
                          (94,81,39), 2)

    retreatButton = Button("Retreat", (770,440), font, (88,39,94), (192,106,202), 40, 125,
                          (88,39,94), 2)

    backButton = Button("Back", (320,340), font, (118,32,2), (215,63,11), 40, 125,
                          (118,32,2), 2)

    # Create Decorative Banners
    banner = Banner((300,430), (120,120,120), (150, 615), (0,0,0), 2)

##    s = pygame.Surface((400,400))
##    s.fill((255,0,0))
##    Chipmunk((0,0)).draw(s)
##    TextBox("This is Chip", (0,150), font, (255,255,255)).draw(s)
##    guiUtils.makeMultiLineTextBox("Chip is a friendly chipmunk, who loves to steal acorns.\n" +
##            "Watch your acorns carefully when Chip is around...", (0,200),
##            font2, (255,255,255), (255,0,0)).draw(s)
##    s = MySurface(s)
##    scroll = ScrollBox((400,100),(200,400), s, (0,0,0), 2)

    scroll = None #guiUtils.getInfoCard(allies[0], (400,100))

    #Create an instance of the game clock
    gameClock = pygame.time.Clock()

    allies = game.getAllies()
    enemies = game.getEnemies()
    player = allies.getLeader()

    RUNNING = True

    target = None

    while RUNNING:
        #Increment the clock
        gameClock.tick()

        #Draw the background to the screen
        background.draw(screen)

        #confirmButton.draw(screen)
        banner.draw(screen)

        #Draw textboxes to the screen
        for box in textBoxes:
            box.draw(screen)
        title.draw(screen)
        #instructions.draw(screen)

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

        attackButton.draw(screen)
        blockButton.draw(screen)
        useItemButton.draw(screen)
        retreatButton.draw(screen)
        backButton.draw(screen)
        
        if scroll != None:
            scroll.draw(screen)

        pygame.display.flip()

        # event handling, gets all event from the eventqueue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT or K_ESCAPE
            if (event.type == pygame.QUIT) or \
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                # change the value to False, to exit the main loop
                RUNNING = False
            if (event.type == pygame.MOUSEBUTTONDOWN and event.button==3):
                for animal in enemies:
                    if animal.getCollideRect().collidepoint(event.pos):
                        scroll = guiUtils.getInfoCard(animal, (450,100))
                        instructions.setText(animal.getName() + " selected...")
                        target = animal
                for animal in allies:
                    if animal.getCollideRect().collidepoint(event.pos):
                        scroll = guiUtils.getInfoCard(animal, (450,100))
                if confirmButton.getCollideRect().collidepoint(event.pos) and \
                   target != None:
                    instructions.setText("Begin the Fight!")
            #confirmButton.move(event)
            attackButton.handleEvent(event, attackButtonFunc)
            blockButton.handleEvent(event, blockButtonFunc)
            useItemButton.handleEvent(event, useItemButtonFunc)
            retreatButton.handleEvent(event, retreatButtonFunc)
            backButton.handleEvent(event, backButtonFunc)
            if scroll != None:
                scroll.move(event)
                
        #Calculate ticks
        ticks = gameClock.get_time() / 1000

        if player.isDead():
            RUNNING =False

    #Close the pygame window and quit pygame
    pygame.quit()



if __name__ == "__main__":

    main()

