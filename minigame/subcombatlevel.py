"""
@authors: Justin Pusztay, Trevor Stalnaker

In this file we create a sublevel mananger for the combat minigame GUI
so that the appropriate interfaces are drawn, handled, and updated for
the appropriate state that the combat game is currently in.
"""


import pygame
from modules import Drawable,Vector2
from animals import *
from graphics import *
from .combatUtils import *
from .victoryscreen import VictoryScreen
from stateMachines import combatStartState,combatPlayerStates,\
     playerTransitions, combatFSM
import time
from .itemselect import ItemSelect
from graphics.guiUtils import ItemCard
from .endscreen import EndScreen

class SubCombatLevel(object):

    def __init__(self,screen,allies,enemies,combatSprites):
        """
        Here we create a subcombat level that requires the input of
        allies and enemies packs whick is the data model. The combat
        sprites are objects created that are passed into the sublevel
        manager. 
        """
        # we must set the state back to player turn to make sure right screen
        combatFSM.backToStart()
        self._screen = screen
        self._allies = allies
        self._enemies = enemies
        
        # this list is created to ensure that the proper order is done
        self._combatOrder = [None]*6
        self._combatOrder[::2] = self._allies
        self._combatOrder[1::2] = self._enemies
        self._counter = 1
        self._combatSprites = combatSprites
        self._font = pygame.font.SysFont("Times New Roman", 20)
        self._textFont = pygame.font.SysFont("Times New Roman", 28)
        self._popupFont = pygame.font.SysFont("Times New Roman", 14) 

        # create the buttons for the player state
        self._attackButton = Button("Attack", (385,100),self._font,(255,255,255),
                                    (222,44,44),50,100,borderWidth = 2)
        self._fortifyButton = Button("Fortify",(495,100),self._font,(255,255,255),
                                     (46,46,218), 50,100,borderWidth = 2)

        self._healButton = Button("Heal",(605,100),self._font,(255,255,255),
                                    (10,200,40),50,100,borderWidth = 2)

        self._retreatButton = Button("Retreat",(715,100),self._font,(255,255,255),
                                     (206,218,46),50,100,borderWidth = 2)

        # attack state and heal state go back button
        self._attackUndoButton = Button("Go Back",(550,100),self._font,
                                        (255,255,255),(0,0,0),50,100)

        # the attack text box
        self._attackTextBox = TextBox("Click on enemy animal to proceed with attack",(0,0),self._textFont,(255,255,255))
        x = self._attackTextBox.getWidth()
        self._attackTextBox.setPosition((600-(x//2),200))

        # the heal text box
        self._healTextBox = TextBox("Click on a potion to heal",(0,0),self._textFont,(255,255,255))
        x = self._healTextBox.getWidth()
        self._healTextBox.setPosition((600-(x//2),225))

        # you have no potions text box
        self._noHealTextBox = TextBox("You have no potions!",(0,0),self._textFont,(255,255,255))
        x = self._noHealTextBox.getWidth()
        self._noHealTextBox.setPosition((600-(x//2),170))

        # text box that displays your turn
        self._turnText = TextBox("Your turn",(565,470),self._font,(255,255,255))
        x = self._turnText.getWidth()
        self._turnText.setPosition((600-(x//2),470))

        # combat text displaying what each NPC did
        self._combatText = TextBox("",(600,100),self._textFont,(255,255,255))

        self._potionSelect = None

        self._turn = True # true means enemies pack turn

        # orb color to indicate whose turn it is
        self._orbColor = (255,255,255)
        self._playerPos = self._combatSprites[0].getPosition()
        y = self._combatSprites[0].getTextHeight()
        self._currentTurnHighlight = Box(self._playerPos,(100,107+y),
                                                    (255,255,0),3)
        self._animalStats = None
        self._popup = None

        # the textbox with the strength of the enemies and the allies
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
                   if x.getAttribute("type") == "potion"]

        # victory GUI items
        self._victoryScreen = VictoryScreen(self._enemies,self._allies[0])

        # retreat GUI Items
        self._retreatScreen = None
                           
    def getCombatSprite(self,animal):
        """
        Given an input animal it returns the combatsprite that is for the
        appropriate animal. 
        """
        for an in self._combatSprites:
            if an.getAnimal() == animal:
                return an

    def updateDisplay(self):
        """
        This method is responsible for the which tab is active in the
        display.
        """
        if self._tabs.getActive() == 0:
            return True
        else:
            return False        

    def alwaysDraw(self):
        """
        These surfaces must be drawn regardless of the state. 
        """
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

    def drawPlayerTurn(self):
        """
        Draw the player turn state surfaces.
        """
        self.alwaysDraw()
        self._attackButton.draw(self._screen)
        self._fortifyButton.draw(self._screen)
        self._healButton.draw(self._screen)
        self._retreatButton.draw(self._screen)
        self._currentTurnHighlight.draw(self._screen)
        if self._popup != None:
            self._popup.draw(self._screen)

    def drawHeal(self):
        """
        Draw the heal state surfaces.
        """
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
        if self._popup != None:
            self._popup.draw(self._screen)
        self._attackUndoButton.draw(self._screen)
        
    def drawAttack(self):
        """
        Draw the attack state surfaces.
        """
        self.alwaysDraw()
        self._attackUndoButton.draw(self._screen)
        self._attackTextBox.draw(self._screen)
        self._currentTurnHighlight.draw(self._screen)
        if self._popup != None:
            self._popup.draw(self._screen)

    def drawWait(self):
        """
        Draw the wait state surfaces.
        """
        self.alwaysDraw()
        self._combatText.draw(self._screen)
        self._currentTurnHighlight.draw(self._screen)
        if self._popup != None:
            self._popup.draw(self._screen)

    def drawFortify(self):
        """
        Draw the fortify state surfaces.
        """
        self.alwaysDraw()
        
    def drawVictory(self):
        """
        Draw the victory state surfaces.
        """
        self._victoryScreen.draw(self._screen)

    def drawRetreat(self):
        """
        Draw the retreat state surfaces.
        """
        if self._retreatScreen == None:
            self._retreatScreen = RetreatScreen(self._allies[0])
        self._retreatScreen.draw(self._screen)

    def drawDead(self):
        """
        Draw the dead state surfaces.
        """
        self._endScreen.draw(self._screen)
        
    def handleEvent(self,event):
        """
        We handle the events that need to be handled regardless of which state you are
        in.
        """
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
        """
        Hanldes the events for the player turn state.
        """
        self._attackButton.handleEvent(event,combatFSM.changeState,"attack button")
        self._fortifyButton.handleEvent(event,combatFSM.changeState,"fortify button")
        self._healButton.handleEvent(event,combatFSM.changeState,"heal button")
        self._retreatButton.handleEvent(event,combatFSM.changeState,"retreat button")

    def handleAttack(self,event):
        """
        Handles the events for the attack state. 
        """
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
                            self._allies.updatePack()
                            self._enemies.updatePack()
                            combatFSM.changeState("animal click")
                            self._combatOrder[::2] = self._allies
                            self._combatOrder[1::2] = self._enemies
                    elif r.collidepoint(pygame.mouse.get_pos()):
                        text = "Potential Damage: " + str(attackComputation(self._allies[0],creature))
                        self._popup = Popup(text,(pygame.mouse.get_pos()[0]+5,pygame.mouse.get_pos()[1]+5),
                                    self._popupFont,multiLine = True)
        if self._enemies.isDead():
            combatFSM.changeState("all dead")

    def handleFortify(self,event):
        """
        Handles the events for the fortify state. 
        """
        self._animalStats = None
        fortify(self._allies[0]) # the model is changed here as told by the controller
        combatFSM.changeState("action complete")
        self._allies.hasAttacked() # here we udpate the model again

    def handleHeal(self,event):
        """
        Handles the events for the heal state. 
        """
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
        """
        Handles the events for the victory state. 
        """
        if self._victoryScreen != None:
            self._victoryScreen.handleEvent(event)

    def update(self):
        """
        Updates all the surfaces that need to be updated regardless of state
        """
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
        self._combatOrder[::2] = self._allies
        self._combatOrder[1::2] = self._enemies
        if self._victoryScreen != None:
            self._victoryScreen.update()
        if self._allies[0] == None:
            combatFSM.changeState("killed")

    def updateHeal(self):
        """Updates health bar."""
        self._combatSprites[0].getHealthBar().update()

    def updateWait(self):
        """
        Updates the wait state where the  NPC turn is. Here we simulate a for
        loop through a counter. We see whose turn it is and then the appropriate
        surfaces are updated and the combat text is written to show which NPCs turn
        it was. We also check to see if we are back when the player turn is and
        update all the right surfaes to have the necessary conditions. 
        """
        self._damageText = None
        if self._counter > 5:
            self._counter = 0
        if self._combatOrder[self._counter] == None:
            pass
        elif self._counter != 0 and self._counter % 2 == 0: # these are allies
            move(self._combatOrder[self._counter],self._combatOrder[1::2])
            self._combatText.setText(self._combatOrder[self._counter].getCombatStatus())
            x = self._combatText.getWidth()
            self._combatText.setPosition((600-(x//2),300))
            self._orbColor = (15,245,107)
            self._turnText.setText(self._combatOrder[self._counter].getName()+"'s turn")
            x = self._turnText.getWidth()
            self._turnText.setPosition((600-(x//2),470))
            self._currentTurnHighlight.setPosition(self.getCombatSprite(self._combatOrder[self._counter]).getPosition())
            self._allies.updatePack() # the model is updated here
            self._enemies.updatePack() # the model is updated here
            self._combatOrder[::2] = self._allies
            self._combatOrder[1::2] = self._enemies
            if self._enemies.isDead():
                combatFSM.changeState("all dead")
        elif self._counter % 2 == 1: # these are the enemies
            move(self._combatOrder[self._counter],self._combatOrder[::2]) # the model is changed here as told by the controller
            self._combatText.setText(self._combatOrder[self._counter].getCombatStatus())
            x = self._combatText.getWidth()
            self._combatText.setPosition((600-(x//2),300))
            self._orbColor = (222,44,44)
            self._turnText.setText(self._combatOrder[self._counter].getName()+"'s turn")
            x = self._turnText.getWidth()
            self._turnText.setPosition((600-(x//2),470))
            self._currentTurnHighlight.setPosition(self.getCombatSprite(self._combatOrder[self._counter]).getPosition())
            self._allies.updatePack() # the model is updated here
            self._enemies.updatePack() # the model is updated here
            self._combatOrder[::2] = self._allies
            self._combatOrder[1::2] = self._enemies
            if self._enemies.isDead():
                combatFSM.changeState("all dead")
        elif self._counter == 0: # this is the player
            combatFSM.changeState("done")
            self._turnText.setText("Your turn")
            x = self._turnText.getWidth()
            self._turnText.setPosition((600-(x//2),470))
            self._orbColor = (255,255,255)
            y = self._combatSprites[0].getTextHeight()
            self._currentTurnHighlight = Box(self._playerPos,(100,107+y),
                                                    (255,255,0),3)
        self._counter += 1
            




