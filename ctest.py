import pygame
from modules import Drawable,Vector2
from animals import *
from graphics import *
from combatUtils import *
from stateMachines import combatStartState,combatPlayerStates,\
     playerTransitions, combatFSM
import time
from items.items import *
from minigame.itemselect import ItemSelect
from minigame.subcombatlevel import SubCombatLevel



SCREEN_SIZE = (1200,500)
WORLD_SIZE  = (2400,500)


def main():

    pygame.init()
    pygame.display.set_caption("Combat MiniGame")
    font = pygame.font.SysFont("Times New Roman", 20)
    textFont = pygame.font.SysFont("Times New Roman", 28)

    screen = pygame.display.set_mode(SCREEN_SIZE)
    background = Drawable("merchantForest2.png", Vector2(0,0))

    ### Make the ally pack ###
    ally1 = Fox()
    ally1.getInventory().addItem(Potions())
    ally1.getInventory().addItem(Potions())
    ally1.getInventory().addItem(Potions())
    ally1.getInventory().addItem(Spear())
##    ally2 = Rabbit()
    ally3 = Bear()

    allies = Pack(ally1)
##    allies.addMember(ally2)
    allies.addMember(ally3)
    
    combatSprites = list()

    y = 200
    for a in allies:
        if allies.isLeader(a):
            c = CombatSprite(a,(228,275),font)
            combatSprites.append(c)
        else:
            if a != None:
                c = CombatSprite(a,(100,y),font)
                combatSprites.append(c)
                y+=150
                
    ### Make the enemy pack ###
    enemy1 = Fox()
##    enemy2 = Bear()
##    enemy3 = Snake()
    enemy1.getInventory().addItem(Spear())

    enemies = Pack(enemy1)
##    enemies.addMember(enemy2)
##    enemies.addMember(enemy3)

    y = 200
    for e in enemies:
        if enemies.isLeader(e):
            c = CombatSprite(e,(847,275),font,enemies = True)
            combatSprites.append(c)
        else:
            if e != None:
                c = CombatSprite(e,(972,y),font,enemies = True)
                combatSprites.append(c)
                y+=150
        
    potionSelect = None
    
    RUNNING = True

    lev = SubCombatLevel(screen,allies,enemies,combatSprites)

    while RUNNING:
        background.draw(screen)

        if combatFSM.getCurrentState() == "player turn":
            lev.drawPlayerTurn()

        elif combatFSM.getCurrentState() == "fortify": 
            lev.drawFortify()
 
        elif combatFSM.getCurrentState() == "attack":
            lev.drawAttack()

        elif combatFSM.getCurrentState() == "heal":
            lev.drawHeal()
            lev.updateHeal()

        elif combatFSM.getCurrentState() == "waiting":
            lev.updateWait()
            lev.update()
            lev.drawWait()
            time.sleep(1.2)

        elif combatFSM.getCurrentState() == "victory":
            lev.drawVictory()

        elif combatFSM.getCurrentState() == "retreat":
            lev.drawRetreat()

        elif combatFSM.getCurrentState() == "dead":
            print("yes")
            lev.drawDead()

        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    RUNNING = False

            lev.handleEvent(event) # for the item popups

            if combatFSM.getCurrentState() == "heal":
                lev.handleHeal(event)

            elif combatFSM.getCurrentState() == "player turn":
                lev.handlePlayerTurn(event)

            elif combatFSM.getCurrentState() == "attack":
                lev.handleAttack(event)
                                
            elif combatFSM.getCurrentState() == "fortify":
                lev.handleFortify(event)
                                
            elif combatFSM.getCurrentState() == "retreat":
                retreat(allies[0])
                
            elif combatFSM.getCurrentState() == "victory":
                lev.handleVictory(event)
        
        if combatFSM.getCurrentState() != "waiting":
            lev.update()
        
    pygame.quit()

if "__main__" == __name__:
    main()  
