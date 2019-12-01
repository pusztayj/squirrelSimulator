import pygame
from modules import Drawable,Vector2
from animals import *
from graphics import *
from .combatUtils import *
from stateMachines import combatStartState,combatPlayerStates,\
     playerTransitions, combatFSM
import time
from .itemselect import ItemSelect
from graphics.guiUtils import ItemCard
from .endscreen import EndScreen

# add ranges to damage that can be done
# show modifers
# show feedback based on player choice
# add some animation


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
        self._popupFont = pygame.font.SysFont("Times New Roman", 14) 

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

        self._attackTextBox = TextBox("Click on enemy animal to proceed with attack",(0,0),self._textFont,(255,255,255))
        self._healTextBox = TextBox("Click on a potion to heal",(0,0),self._textFont,(255,255,255))
        x = self._healTextBox.getWidth()
        self._healTextBox.setPosition((600-(x//2),225))

        self._noHealTextBox = TextBox("You have no potions!",(0,0),self._textFont,(255,255,255))
        x = self._noHealTextBox.getWidth()
        self._noHealTextBox.setPosition((600-(x//2),170))

        self._turnText = TextBox("Your turn",(565,470),self._font,(255,255,255))
        x = self._turnText.getWidth()
        self._turnText.setPosition((600-(x//2),470))

        self._combatText = TextBox("",(600,100),self._textFont,(255,255,255))

        self._potionSelect = None

        self._turn = True # true means enemies pack turn

        self._orbColor = (255,255,255)
        self._playerPos = self._combatSprites[0].getPosition()
        y = self._combatSprites[0].getTextHeight()
        self._currentTurnHighlight = Box(self._playerPos,(100,107+y),
                                                    (255,255,0),3)
        self._animalStats = None
        self._popup = None

        self._allyText = TextBox("You and your allies",(239,150),self._font,(255,255,255))
        x = self._allyText.getWidth()
        self._allyText.setPosition((239-(x//2),150))
        self._allyStrength = TextBox("Total Strength: "+ \
                                     str(sum([x.getStrength() for x in self._allies if x!= None])),
                                     (239,150),self._font,(255,255,255))
        x = self._allyStrength.getWidth()
        self._allyStrength.setPosition((239-(x//2),175))

        self._enemyText = TextBox("Your enemies",(239,150),self._font,(255,255,255))
        x = self._enemyText.getWidth()
        self._enemyText.setPosition((975-(x//2),150))
        self._enemyStrength = TextBox("Total Strength: "+\
                                      str(sum([x.getStrength() for x in self._enemies if x!= None])),
                                      (239,150),self._font,(255,255,255))
        x = self._enemyStrength.getWidth()
        self._enemyStrength.setPosition((975-(x//2),175))

        self._damageText = None
        self._potions = [x for x in self._allies[0].getInventory() \
                   if type(x) == type(Potions())]

        # victory GUI items
        self._victoryScreen = None

        # retreat GUI Items
        self._retreatScreen = None

        # death GUI
        self._endScreen = EndScreen((1200,500),self._allies[0])

                                 
    def getCombatSprite(self,animal):
        """
        Given an input animal it returns the combatsprite that is for the
        appropriate animal. 
        """
        for an in self._combatSprites:
            if an.getAnimal() == animal:
                return an

    def updateDisplay(self):
        if self._tabs.getActive() == 0:
            return True
        else:
            return False        

    def alwaysDraw(self):
        for x in self._combatSprites:
            x.draw(self._screen)
        pygame.draw.circle(self._screen,self._orbColor,(600,435),25)
        self._turnText.draw(self._screen)
        self._allyText.draw(self._screen)
        self._allyStrength.draw(self._screen)
        self._enemyStrength.draw(self._screen)
        self._enemyText.draw(self._screen)
        if self._animalStats != None:
            self._animalStats.draw(self._screen)
        if self._popup != None:
            self._popup.draw(self._screen)

    def drawPlayerTurn(self):
        self.alwaysDraw()
        self._attackButton.draw(self._screen)
        self._fortifyButton.draw(self._screen)
        self._healButton.draw(self._screen)
        self._retreatButton.draw(self._screen)
        self._currentTurnHighlight.draw(self._screen)

    def drawHeal(self):
        self.alwaysDraw()
        if self._potionSelect == None:
            self._potionSelect = ItemSelect((0,0),self._potions)
            x = self._potionSelect.getWidth()
            self._potionSelect.setPosition((600-(x//2),165))
        if len(self._potions) > 0:
            self._potionSelect.draw(self._screen)
            self._healTextBox.draw(self._screen)
        else:
            self._noHealTextBox.draw(self._screen)
        self._currentTurnHighlight.draw(self._screen)
        self._attackUndoButton.draw(self._screen)
        
        
    def drawAttack(self):
        self.alwaysDraw()
        self._attackUndoButton.draw(self._screen)
        self._attackTextBox.draw(self._screen)
        self._currentTurnHighlight.draw(self._screen)

    def drawWait(self):
        self.alwaysDraw()
        self._combatText.draw(self._screen)
        self._currentTurnHighlight.draw(self._screen)

    def drawFortify(self):
        self.alwaysDraw()
        
    def drawVictory(self):
        if self._victoryScreen == None:
            self._victoryScreen = VictoryScreen(self._enemies,self._allies[0])
        self._victoryScreen.draw(self._screen)

    def drawRetreat(self):
        if self._retreatScreen == None:
            self._retreatScreen = RetreatScreen(self._allies[0])
        self._retreatScreen.draw(self._screen)

    def drawDead(self):
        self._endScreen.draw(self._screen)
        
    def handleEvent(self,event):
        self._popup = None
        for sprite in self._combatSprites: # no need to check nones as they are no longer in list
            x,y = sprite.getAnimalPosition()
            for rect in sprite.getCollideRects():
                r = rect.move(x,y)
                if (event.type == pygame.MOUSEBUTTONDOWN and event.button==3):
                    if r.collidepoint(event.pos):
                        self._animalStats = AnimalStats(sprite.getAnimal(),(400,220))
                elif r.collidepoint(pygame.mouse.get_pos()):
                    text = "Holding: " + sprite.getAnimal().getEquipItemName() + \
                           "\nArmor: " + sprite.getAnimal().getArmorsName() + \
                           "\nStrength: " + str(sprite.getAnimal().getStrength())
                    self._popup = Popup(text,(pygame.mouse.get_pos()[0]+5,pygame.mouse.get_pos()[1]+5),
                                        self._popupFont,multiLine = True)
        if self._animalStats != None:
            self._animalStats.handleEvent(event)
            if self._animalStats.getDisplay() == False:
                self._animalStats = None

    def handlePlayerTurn(self,event):
        self._attackButton.handleEvent(event,combatFSM.changeState,"attack button")
        self._fortifyButton.handleEvent(event,combatFSM.changeState,"fortify button")
        self._healButton.handleEvent(event,combatFSM.changeState,"heal button")
        self._retreatButton.handleEvent(event,combatFSM.changeState,"retreat button")

    def handleAttack(self,event):
        self._popup = None
        self._attackUndoButton.handleEvent(event,combatFSM.changeState,"go back")
        for creature in self._enemies:
            if creature != None:
                a = self.getCombatSprite(creature)
                x,y = a.getAnimalPosition()
                for rect in a.getCollideRects():
                    r = rect.move(x,y)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
                        if r.collidepoint(event.pos):
                            self._animalStats = None
                            attack(self._allies[0],creature) # the model is changed here as told by the controller
                            self._combatText.setText(self._allies.getNextToAttack().getCombatStatus())
                            x = self._combatText.getWidth()
                            self._combatText.setPosition((600-(x//2),100))
                            self._enemies.updatePack()
                            combatFSM.changeState("animal click")
                            self._allies.hasAttacked() # here we udpate the model again
                    elif r.collidepoint(pygame.mouse.get_pos()):
                        text = "Potential Damage: " + str(attackComputation(self._allies[0],creature))
                        self._popup = Popup(text,(pygame.mouse.get_pos()[0]+5,pygame.mouse.get_pos()[1]+5),
                                    self._popupFont,multiLine = True)
        if self._enemies.isDead():
            combatFSM.changeState("all dead")

    def handleFortify(self,event):
        self._animalStats = None
        fortify(self._allies[0]) # the model is changed here as told by the controller
        combatFSM.changeState("action complete")
        self._allies.hasAttacked() # here we udpate the model again

    def handleHeal(self,event):
        self._animalStats = None
        self._attackUndoButton.handleEvent(event,combatFSM.changeState,"go back")
        self._potionSelect.handleEvent(event)
        try:
            potionPick = self._potionSelect.getItemSelected()
            if potionPick != None:
                heal(self._allies[0],potionPick) # the model is changed here as told by the controller
                combatFSM.changeState("action complete")
            self._allies.hasAttacked() # here we udpate the model again
        except AttributeError:
            pass

    def handleVictory(self,event):
        if self._victoryScreen != None:
            self._victoryScreen.handleEvent(event)

    def update(self):
        self._combatSprites = [x for x in self._combatSprites if not x.getHealthBar().getEntity().isDead()] # the model is updated here as told by the controller
        for x in self._combatSprites:
            x.getHealthBar().update()
            x.getHealthText().setText(str(x.getAnimal().getHealth()) + "/100")
        self._enemyStrength.setText("Total Strength: "+str(sum([x.getStrength() for x in self._enemies if x!= None])))
        self._allyStrength.setText("Total Strength: "+str(sum([x.getStrength() for x in self._allies if x!= None])))
        if self._animalStats != None:
            self._animalStats.update()
        if self._allies[0] != None and self._potionSelect != None:
            self._potions = [x for x in self._allies[0].getInventory() \
                       if type(x) == type(Potions())]
            self._potionSelect.resetItems(self._potions)
            self._potionSelect.update()
            x = self._potionSelect.getWidth()
            self._potionSelect.setPosition((600-(x//2),165))
        self._allies.updatePack() # the model is updated here
        self._enemies.updatePack() # the model is updated here
        if self._victoryScreen != None:
            self._victoryScreen.update()
        if self._allies[0] == None:
            combatFSM.changeState("killed")

    def updateHeal(self):
        self._combatSprites[0].getHealthBar().update()

    def updateWait(self):
        # for the enemies
        self._damageText = None
        if self._turn == True:
            if self._enemies.getNextToAttack() == None:
                self._enemies.hasAttacked()
                self._turn = not self._turn
            else:
                move(self._enemies.getNextToAttack(),self._allies) # the model is changed here as told by the controller
                self._combatText.setText(self._enemies.getNextToAttack().getCombatStatus())
                x = self._combatText.getWidth()
                self._combatText.setPosition((600-(x//2),300))
                self._orbColor = (222,44,44)
                self._turnText.setText(self._enemies.getNextToAttack().getName()+"'s turn")
                x = self._turnText.getWidth()
                self._turnText.setPosition((600-(x//2),470))
                a = len([x for x in self._allies if x!=None])
                self._currentTurnHighlight.setPosition(self.getCombatSprite(self._enemies.getNextToAttack()).getPosition())
                self._allies.updatePack() # the model is updated here
                self._enemies.updatePack() # the model is updated here
                self._enemies.hasAttacked() # here we update the model
                self._turn = not self._turn
                if self._enemies.isDead():
                    combatFSM.changeState("all dead")
##                if self._allies[0].isDead():
##                    combatFSM.changeState("killed")
        # for the allies     
        elif self._turn == False and self._allies.getNextToAttack() != self._allies[0]:
            if self._allies.getNextToAttack() == None:
                self._allies.hasAttacked()
                self._turn = not self._turn
            else:
                move(self._allies.getNextToAttack(),self._enemies)
                self._combatText.setText(self._allies.getNextToAttack().getCombatStatus())
                x = self._combatText.getWidth()
                self._combatText.setPosition((600-(x//2),300))
                self._orbColor = (15,245,107)
                self._turnText.setText(self._allies.getNextToAttack().getName()+"'s turn")
                x = self._turnText.getWidth()
                self._turnText.setPosition((600-(x//2),470))
                self._currentTurnHighlight.setPosition(self.getCombatSprite(self._allies.getNextToAttack()).getPosition())
                self._allies.updatePack() # the model is updated here
                self._enemies.updatePack() # the model is updated here
                self._allies.hasAttacked() # here we update the model
                self._turn = not self._turn
                if self._enemies.isDead():
                    combatFSM.changeState("all dead")
                           
        else:
            self._turn = not self._turn
            combatFSM.changeState("done")
            self._turnText.setText("Your turn")
            x = self._turnText.getWidth()
            self._turnText.setPosition((600-(x//2),470))
            self._orbColor = (255,255,255)
            y = self._combatSprites[0].getTextHeight()
            self._currentTurnHighlight = Box(self._playerPos,(100,107+y),
                                                    (255,255,0),3)
            
