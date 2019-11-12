import pygame
from modules.drawable import Drawable
from modules.vector2D import Vector2
from animals.pack import Pack
from animals.chipmunk import Chipmunk
from animals.deer import Deer
from animals.fox import Fox
from animals.bear import Bear
from animals.snake import Snake
from animals.rabbit import Rabbit
from graphics.textbox import TextBox
from graphics.progressbar import ProgressBar
from graphics.popup import Popup
from graphics.popupwindow import PopupWindow
from graphics.linkedprogressbar import LinkedProgressBar
from graphics.button import Button
from combatUtils import *
from stateMachines import combatStartState,combatPlayerStates,\
     playerTransitions, combatFSM
import time

SCREEN_SIZE = (1200,500)
WORLD_SIZE  = (2400,500)

"""
REMARK
------

If the screen size changes note that the positions of everything
is hard coded so those positions need to be changed.
"""

def main():

    pygame.init()
    pygame.display.set_caption("Combat MiniGame")
    font = pygame.font.SysFont("Times New Roman", 20)
    textFont = pygame.font.SysFont("Times New Roman", 28)

    screen = pygame.display.set_mode(SCREEN_SIZE)
    background = background = Drawable("merchantForest2.png", Vector2(0,0))

    ### Make the ally pack ###
    ally1 = Bear()
    ally2 = Snake()
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
    # ally pack health bars
    allyHealthBars = list()
    y = 200+133
    for x in allies:
        if allies.isLeader(x):
            a = LinkedProgressBar(x,(x.getX() + (x.getWidth()//4),250+138),64,
                                  100,x.getHealth())
##            a = ProgressBar((x.getX() + (x.getWidth()//4),250+138),64,
##                            100,x.getHealth())
            allyHealthBars.append(a)
        else:
            a = LinkedProgressBar(x,(x.getX() + (x.getWidth()//4),y),64,
                                  100,x.getHealth())
##            a = ProgressBar((x.getX() + (x.getWidth()//4),y),
##                             64,100,x.getHealth())
            allyHealthBars.append(a)
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
        
    y = 200+133
    for x in enemies:
        if enemies.isLeader(x):
            a = LinkedProgressBar(x,(x.getX() + (x.getWidth()//4),250+138),64,
                                  100,x.getHealth())
##            a = ProgressBar((x.getX() + (x.getWidth()//4),250+138),64,
##                            100,x.getHealth())
            allyHealthBars.append(a)
        else:
            a = LinkedProgressBar(x,(x.getX() + (x.getWidth()//4),y),64,
                                  100,x.getHealth())
##            a = ProgressBar((x.getX() + (x.getWidth()//4),y),64,
##                            100,x.getHealth())
            allyHealthBars.append(a)
            y+=150

    ### Make the turn counter metric ###
    turnText = TextBox("Your turn",(565,470),font,(255,255,255))

    ### Health counter Hover over Popup ###
    allyPopups = list()
    for x in allies:
        text = x.getName() + "\nHealth: " + str(x.getHealth()) + "/100"
        a = Popup(text,(0,0),font)
        allyPopups.append(a)

    ### Buttons for player to play game on ###
    attackButton = Button("Attack", (385,100),font,(255,255,255),(222,44,44),
                          50,100,borderWidth = 2)

    fortifyButton = Button("Fortify",(495,100),font,(255,255,255),(46,46,218),
                           50,100,borderWidth = 2)

    healButton = Button("Heal",(605,100),font,(255,255,255),(0,0,0),
                           50,100)

    retreatButton = Button("Retreat",(715,100),font,(255,255,255),(206,218,46),
                           50,100,borderWidth = 2)

    attackUndoButton = Button("Go Back",(550,100),font,(255,255,255),(0,0,0),
                           50,100)

    ### Necessary Text Boxes ###
    attackTextBox = TextBox("Click on enemy animal to proceed with attack",
                            (350,190),textFont,(255,255,255))
    
        
    

    RUNNING = True
    while RUNNING:
        background.draw(screen)
        
        ### Draw the allies ###
        for a in allies:
            a.draw(screen)

        ### Draw the enemeies ###
        for e in enemies:
            e.draw(screen)
            
        ### Drawing the health bars ###
        for x in allyHealthBars:
            x.draw(screen)

        ### Draw hover over pop ups ###

            
        ### Draw the turn metric ###
        pygame.draw.circle(screen,(255,255,255),(600,435),25)
        turnText.draw(screen)

        ### Draw the buttons if the players turn ###
        if combatFSM.getCurrentState() == "player turn":
            attackButton.draw(screen)
            fortifyButton.draw(screen)
            healButton.draw(screen)
            retreatButton.draw(screen)

        if combatFSM.getCurrentState() == "attack":
            attackUndoButton.draw(screen)
            attackTextBox.draw(screen)

        if combatFSM.getCurrentState() == "waiting":
                combatOrder = turnOrder(allies,enemies)
                text_y = 150
                for creature in combatOrder:
                    if creature in allies:
                        move(creature,enemies)
                        pygame.draw.circle(screen,(15,245,107),(600,435),25)
                        turnText.setText(creature.getName()+"'s turn")
                        allies.updatePack()
                        enemies.updatePack()
                    else:
                        move(creature,allies)
                        pygame.draw.circle(screen,(222,44,44),(600,435),25)
                        turnText.setText(creature.getName()+"'s turn")
                        allies.updatePack()
                        enemies.updatePack()
                    text = creature.getCombatStatus()
                    popup = TextBox(text,(375,text_y),font,(255,255,255))
                    popup.draw(screen)
                    pygame.display.flip()
                    time.sleep(1)
                    text_y += 50
                combatFSM.changeState("done")
            
            
        # needs to be after everything is drew
        pygame.display.flip()


        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                RUNNING = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    RUNNING = False
                    
            if combatFSM.getCurrentState() == "player turn":
                attackButton.handleEvent(event,combatFSM.changeState,"attack button")
                fortifyButton.handleEvent(event,combatFSM.changeState,"fortify button")
                healButton.handleEvent(event,combatFSM.changeState,"heal button")
                retreatButton.handleEvent(event,combatFSM.changeState,"retreat button")
                
            if combatFSM.getCurrentState() == "attack":
                attackUndoButton.handleEvent(event,combatFSM.changeState,"go back")
                if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
                    for creature in enemies:
                        x,y = creature.getPosition()
                        for rect in creature.getCollideRects():
                            r = rect.move(x,y)
                            if r.collidepoint(event.pos):
                                attack(allies[0],creature)
                                enemies.updatePack()
                                combatFSM.changeState("animal click")
                                
            elif combatFSM.getCurrentState() == "fortify":
                fortify(allies[0])
                combatFSM.changeState("action complete")
                
            elif combatFSM.getCurrentState() == "heal":
                combatFSM.changeState("action complete")
                
            elif combatFSM.getCurrentState() == "retreat":
                retreat(allies[0])
                RUNNING = False
        allyHealthBars = [x for x in allyHealthBars if not x.getEntity().isDead()]
        for x in allyHealthBars:
            x.update()
        
    pygame.quit()

if "__main__" == __name__:
    main()  
        
