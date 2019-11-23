import pygame
from modules import Drawable,Vector2
from animals import *
from graphics import *
from combatUtils import *
from stateMachines import combatStartState,combatPlayerStates,\
     playerTransitions, combatFSM
import time
from .itemselect import ItemSelect


# Add when player wants to attack when you hover over damage shown
# highlight who's turn it is
# figu


class SubCombatLevel(object):

    def __init__(self,screen,allies,enemies,combatSprites):
        """
        The input of allies will be the data model. The input of the health
        bar object will be the view. The view will be updated by the change
        in the model. The model changes are handled in combat GUI and through
        the pack. Here we simply update the view. 
        """
        self._screen = screen
        self._allies = allies
        self._enemies = enemies
        self._combatSprites = combatSprites
        self._font = pygame.font.SysFont("Times New Roman", 20)
        self._textFont = pygame.font.SysFont("Times New Roman", 28)

        self._attackButton = Button("Attack", (385,100),self._font,(255,255,255),
                                    (222,44,44),50,100,borderWidth = 2)
        self._fortifyButton = Button("Fortify",(495,100),self._font,(255,255,255),
                                     (46,46,218), 50,100,borderWidth = 2)

        self._healButton = Button("Heal",(605,100),self._font,(255,255,255),
                                    (10,200,40),50,100,borderWidth = 2)

        self._retreatButton = Button("Retreat",(715,100),self._font,(255,255,255),
                                     (206,218,46),50,100,borderWidth = 2)

        self._attackUndoButton = Button("Go Back",(550,100),self._font,
                                        (255,255,255),(0,0,0),50,100)

        self._attackTextBox = TextBox("Click on enemy animal to proceed with attack",(350,190),self._textFont,(255,255,255))

        self._turnText = TextBox("Your turn",(565,470),self._font,(255,255,255))
        x = self._turnText.getWidth()
        self._turnText.setPosition((600-(x//2),470))

        self._combatText = TextBox("",(600,100),self._textFont,(255,255,255))

        self._potionSelect = None
        potions = [x for x in self._allies[0].getInventory() \
                   if type(x) == type(Potions())]
        self._potionSelect = ItemSelect((255,100),potions)

        self._turn = True # true means enemies pack turn

        self._orbColor = (255,255,255)

    def alwaysDraw(self):
        for x in self._combatSprites:
            x.draw(self._screen)
        pygame.draw.circle(self._screen,self._orbColor,(600,435),25)
        self._turnText.draw(self._screen)

    def drawPlayerTurn(self):
        self.alwaysDraw()
        self._attackButton.draw(self._screen)
        self._fortifyButton.draw(self._screen)
        self._healButton.draw(self._screen)
        self._retreatButton.draw(self._screen)


    def drawHeal(self):
        self.alwaysDraw()
        x = self._potionSelect.getWidth()
        self._potionSelect.setPosition((600-(x//2),100))
        self._potionSelect.draw(self._screen)
        
    def drawAttack(self):
        self.alwaysDraw()
        self._attackUndoButton.draw(self._screen)
        self._attackTextBox.draw(self._screen)

    def drawWait(self):
        self.alwaysDraw()
        self._combatText.draw(self._screen)

    def drawFortify(self):
        self.alwaysDraw()

    def handleEvent(self,event):
        if (event.type == pygame.MOUSEBUTTONDOWN and event.button==3):
            for animal in enemies:
                if animal.getCollideRect().collidepoint(event.pos):
                        scroll = guiUtils.getInfoCard(animal, (450,100))
                        instructions.setText(animal.getName() + " selected...")
                        target = animal
    
    def handlePlayerTurn(self,event):
        self._attackButton.handleEvent(event,combatFSM.changeState,"attack button")
        self._fortifyButton.handleEvent(event,combatFSM.changeState,"fortify button")
        self._healButton.handleEvent(event,combatFSM.changeState,"heal button")
        self._retreatButton.handleEvent(event,combatFSM.changeState,"retreat button")

    def handleAttack(self,event):
        self._attackUndoButton.handleEvent(event,combatFSM.changeState,"go back")
        if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
            enemies = [x for x in self._combatSprites if x.isEnemy()]
            for creature in self._enemies:
                if creature != None:
                    a = [z for z in enemies if z.getAnimal() == creature][0]
                    x,y = a.getPosition()
                    for rect in a.getCollideRects():
                        r = rect.move(x,y)
                        if r.collidepoint(event.pos):
                            attack(self._allies[0],creature) # the model is changed here as told by the controller
                            self._enemies.updatePack()
                            combatFSM.changeState("animal click")
                            self._allies.hasAttacked() # here we udpate the model again

    def handleFortify(self,event):
        fortify(self._allies[0]) # the model is changed here as told by the controller
        combatFSM.changeState("action complete")
        self._allies.hasAttacked() # here we udpate the model again

    def handleHeal(self,event):
        self._potionSelect.handleEvent(event)
        potionPick = self._potionSelect.getItemSelected()
        if potionPick != None:
            heal(self._allies[0],potionPick) # the model is changed here as told by the controller
            potions = [x for x in self._allies[0].getInventory() \
                   if type(x) == type(Potions())]
            self._potionSelect.resetItems(potions)
            combatFSM.changeState("action complete")
        self._allies.hasAttacked() # here we udpate the model again

    def update(self):
        self._combatSprites = [x for x in self._combatSprites if not x.getHealthBar().getEntity().isDead()] # the model is updated here as told by the controller
        for x in self._combatSprites:
            x.getHealthBar().update()
        self._potionSelect.update()
        self._allies.updatePack() # the model is updated here
        self._enemies.updatePack() # the model is updated here


    def updateWait(self):
        if self._turn == True:
            move(self._enemies.getNextToAttack(),self._allies) # the model is changed here as told by the controller
            self._combatText.setText(self._enemies.getNextToAttack().getCombatStatus())
            x = self._combatText.getWidth()
            self._combatText.setPosition((600-(x//2),100))
            self._orbColor = (222,44,44)
            self._turnText.setText(self._enemies.getNextToAttack().getName()+"'s turn")
            x = self._turnText.getWidth()
            self._turnText.setPosition((600-(x//2),470))
            self._allies.updatePack() # the model is updated here
            self._enemies.updatePack() # the model is updated here
            self._enemies.hasAttacked() # here we update the model
            self._turn = not self._turn
        elif self._turn == False and self._allies.getNextToAttack() != self._allies[0]:
            move(self._allies.getNextToAttack(),self._enemies)
            self._combatText.setText(self._allies.getNextToAttack().getCombatStatus())
            x = self._combatText.getWidth()
            self._combatText.setPosition((600-(x//2),100))
            self._orbColor = (15,245,107)
            self._turnText.setText(self._allies.getNextToAttack().getName()+"'s turn")
            x = self._turnText.getWidth()
            self._turnText.setPosition((600-(x//2),470))
            self._allies.updatePack() # the model is updated here
            self._enemies.updatePack() # the model is updated here
            self._allies.hasAttacked() # here we update the model
            self._turn = not self._turn
        else:
            combatFSM.changeState("done")
            self._turnText.setText("Your turn")
            x = self._turnText.getWidth()
            self._turnText.setPosition((600-(x//2),470))
            self._orbColor = (255,255,255)
            
