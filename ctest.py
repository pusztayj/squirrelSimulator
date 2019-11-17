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

"""
REMARK
------

If the screen size changes note that the positions of everything
is hard coded so those positions need to be changed.
"""

def makeHealthBars(pack1):
    healthbars = list()
    y = 200+133
    for x in pack1:
        if pack1.isLeader(x):
            a = LinkedProgressBar(x,(x.getX() + (x.getWidth()//4),250+138),64,
                                  100,x.getHealth())
            healthbars.append(a)
        else:
            a = LinkedProgressBar(x,(x.getX() + (x.getWidth()//4),y),64,
                                  100,x.getHealth())
            healthbars.append(a)
            y+=150
    return healthbars

def main():

    pygame.init()
    pygame.display.set_caption("Combat MiniGame")
    font = pygame.font.SysFont("Times New Roman", 20)
    textFont = pygame.font.SysFont("Times New Roman", 28)

    screen = pygame.display.set_mode(SCREEN_SIZE)
    background = Drawable("merchantForest2.png", Vector2(0,0))

    ### Make the ally pack ###
    ally1 = Bear()
    ally1.getInventory().addItem(Potions())
    ally2 = Deer()
    ally3 = Fox()

    allies = Pack(ally1)
    allies.addMember(ally2)
    allies.addMember(ally3)

    y = 200
    for a in allies:
        if allies.isLeader(a):
            a.setPosition((225,250))
        else:
            a.setPosition((100,y))
            y+=150
                
    ### Make the enemy pack ###
    enemy1 = Deer()
    enemy1.flip()
    enemy2 = Rabbit()
    enemy2.flip()
    enemy3 = Rabbit()
    enemy3.flip()

    enemies = Pack(enemy1)
    enemies.addMember(enemy2)
    enemies.addMember(enemy3)

    y = 200
    for e in enemies:
        if enemies.isLeader(e):
            e.setPosition((847,250))
        else:
            e.setPosition((972,y))
            y+=150

    healthbars = makeHealthBars(allies) + makeHealthBars(enemies)
        
    potionSelect = None
    
    RUNNING = True

    lev = SubCombatLevel(screen,allies,enemies,healthbars)
    print([x.getName() for x in allies])
    print([x.getName() for x in enemies])
    count = 0
    
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

        elif combatFSM.getCurrentState() == "waiting":
            lev.drawWait()
            time.sleep(3)
            
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    RUNNING = False

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
                RUNNING = False
        lev.update()
        if combatFSM.getCurrentState() == "waiting":
            lev.updateWait()
        
        
    pygame.quit()

if "__main__" == __name__:
    main()  
        
