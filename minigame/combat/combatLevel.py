
import pygame
from .utils import *
from level import Level
from modules import Drawable
from managers import CONSTANTS, USER_INTERFACE, SOUNDS

from minigame.turnOrder import TurnOrder
from minigame.victoryscreen import VictoryScreen

from graphics.ui.menu import Menu
from graphics import *

from minigame.itemselect import ItemSelect


SCREEN_SIZE = CONSTANTS.get("screen_size")

class CombatLevel(Level):

    def __init__(self,allies,enemies):
        super().__init__()

        self._player = allies.getLeader()
        self._allies = allies
        self._enemies = enemies
        
        self._combatOrder = TurnOrder(self._allies, self._enemies)
        self._current = self._combatOrder.getCurrent()
        
        self._npcTurnLength = 3
        self._npcTurnTimer = self._npcTurnLength


        self._font = pygame.font.SysFont("Times New Roman", 20)
        self._textFont = pygame.font.SysFont("Times New Roman", 28)
        self._popupFont = pygame.font.SysFont("Times New Roman", 14) 

        # make the background
        self._background = Drawable("merchantForest2.png",
                                    (0,0), worldBound=False)

        SOUNDS.manageSongs("combat")

        # create the combat sprites
        self._combatSprites = createCombatSprites(self._allies, self._enemies, self._font)

        self._creatureSpriteMap = dict(zip(self._allies.getTrueMembers()+self._enemies.getTrueMembers(),
                                self._combatSprites))

        self._spriteToCreatureMap = dict(zip(self._combatSprites, self._allies.getTrueMembers()+self._enemies.getTrueMembers()))
        
        self._creatureSpriteMap[self._current].select()

        combat_commands = USER_INTERFACE.getControlsForMenu("combat")
        self._movesMenu = Menu((385,100),(430, 50), combat_commands, padding=(0,0), spacing=10,
                     color=None, borderWidth=0, orientation="horizontal")   

        # attack state and heal state go back button
        self._backToMenuButton = Button("Go Back",(550,100),self._font,
                                        (255,255,255),(0,0,0),50,100)

        # puts the text indicating the next step in the appropriate place after clicking attack or heal
        self._moveText = TextBox("",(0,0),self._textFont,(255,255,255))

        # text box that displays your turn
        self._turnText = TextBox("Your turn",(0,470),self._font,(255,255,255))
        self._turnText.keepCentered(cen_point=(1/2,None))

        # combat text displaying what each NPC did
        self._combatText = TextBox("",(600,100),self._textFont,(255,255,255))
        self._combatText.keepCentered(cen_point=(1/2,None))

        self._potions = [x for x in self._allies[0].getInventory() \
                   if x.getAttribute("type") == "potion"]
        self._potionSelect = ItemSelect((0,165),self._potions)
        centerGraphicsElement(self._potionSelect,axes=(True, False))

        self._orbColor = (255,255,255)

        self._animalStats = None # animal stats menu
        self._popup = None # collision pop up menu

        # the textbox with the strength of the enemies and the allies
        
        ################################ ripe for refactoring ##############################################
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
        ################################ ripe for refactoring ##############################################

        # victory GUI items
        self._victoryScreen = None

        # retreat GUI Items
        self._retreatScreen = None

        self._backWorld = Button("Back to World",(875,210),self._font,(0,0,0),
                            (124,252,0),80,150,borderWidth = 2) # should be inside victory and retreat screens

        self._npcDone = False
        self._playerDone = False
        self._menuSelection = None

    def draw(self, screen):
        # what we always draw
        self._background.draw(screen)

        if self._retreatScreen == None and self._victoryScreen == None:

            for x in self._combatSprites:
                x.draw(screen)
            pygame.draw.circle(screen,self._orbColor,(600,435),25)
            self._turnText.draw(screen)
            self._allyText.draw(screen)
            self._allyStrength.draw(screen)
            self._enemyStrength.draw(screen)
            self._enemyText.draw(screen)
            if self._popup != None:
                self._popup.draw(screen)
    
            # here we draw the player turn state
            if self._current == self._player:
                if self._animalStats != None:
                    self._animalStats.draw(screen)
                if not self._movesMenu.getDisplay():
                    if self._playerDone:
                        self._combatText.draw(screen)
                    elif self._menuSelection == 1: # draws what is seen after clicking attack button
                        self._backToMenuButton.draw(screen)
                        self._moveText.setText("Click on enemy animal to proceed with attack")
                        self._moveText.setPosition((0,200))
                        centerGraphicsElement(self._moveText,axes=(True, False))
                        self._moveText.draw(screen) # NEEDS REFACTOR SINCE WE ARE INTEGRATING MULTIPLE TEXT BOXES
                    elif self._menuSelection == 3: # draws what is seen after clicking heal button
                        if len(self._potions) > 0:
                            self._potionSelect.draw(screen)
                            self._moveText.setText("Click on a potion to heal")
                            self._moveText.setPosition((0,225))
                            centerGraphicsElement(self._moveText,axes=(True, False))
                            self._moveText.draw(screen)# NEEDS REFACTOR SINCE WE ARE INTEGRATING MULTIPLE TEXT BOXES
                        else:
                            self._moveText.setText("You have no potions!")
                            self._moveText.setPosition((0,225))
                            centerGraphicsElement(self._moveText,axes=(True, False))
                            self._moveText.draw(screen) # NEEDS REFACTOR SINCE WE ARE INTEGRATING MULTIPLE TEXT BOXES
                        self._backToMenuButton.draw(screen)
                else:
                    self._movesMenu.draw(screen)
            else:
                self._combatText.draw(screen)
                
        if self._retreatScreen != None:
            self._retreatScreen.draw(screen)
            self._backWorld.draw(screen)

        if self._victoryScreen != None:
            self._victoryScreen.draw(screen)
            self._backWorld.draw(screen)


    def handleEvent(self, event):
        self._popup = None
        for sprite in self._combatSprites: # no need to check nones as they are no longer in list
            x,y = sprite.getAnimalPosition()
            creature = self._spriteToCreatureMap[sprite]
            for rect in sprite.getCollideRects():
                r = rect.move(x,y)
                if (event.type == pygame.MOUSEBUTTONDOWN and event.button==3 and self._current == self._player):
                    if r.collidepoint(event.pos):
                        self._animalStats = AnimalStats(sprite.getAnimal(),(400,220))
                elif r.collidepoint(pygame.mouse.get_pos()):
                    if (not self._movesMenu.getDisplay()) and self._menuSelection == 1 and \
                       creature in self._enemies.getTrueMembers():
                        text = "Potential Damage: " + str(attackComputation(self._allies[0],creature))
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            if r.collidepoint(event.pos):
                                attack(self._player,creature) # the model is changed here as told by the controller
                                self._playerDone = True

                                # Show the player's attack on the screen
                                self._player.attackLogic([creature])
                                text = self._player.getCombatStatus().replace(self._player.getName(),"You",1)
                                self._combatText.setText(text)
                                
                    else:
                        animal = sprite.getAnimal()
                        if animal.isEquipped():
                            item = sprite.getAnimal().getEquipItem().getAttribute("name")
                        else:
                            item = ""
                        if animal.hasArmor():
                            armor = sprite.getAnimal().getArmor().getAttribute("name")
                        else:
                            armor = ""
                        text = "Holding: " + item + \
                               "\nArmor: " + armor + \
                               "\nStrength: " + str(sprite.getAnimal().getStrength())
                    self._popup = Popup(text,(pygame.mouse.get_pos()[0]+5,pygame.mouse.get_pos()[1]+5),
                                        self._popupFont,multiLine = True)

        if self._current == self._player:
            if self._animalStats != None:
                self._animalStats.handleEvent(event)
                if self._animalStats.getDisplay() == False:
                    self._animalStats = None
            if self._movesMenu.getDisplay():
                self._menuSelection = self._movesMenu.handleEvent(event)
            else:
                if self._menuSelection == 1: # handles attack 
                    self._backToMenuButton.handleEvent(event,self._movesMenu.display)
                if self._menuSelection == 2: # handles fortify
                    fortify(self._player) # the model is changed here as told by the controller
                    self._playerDone = True
                    
                    # Show the player's move on the screen
                    self._combatText.setText("You have fortified!")
                    
                if self._menuSelection == 3: # handles heal
                    self._backToMenuButton.handleEvent(event,self._movesMenu.display)
                    self._potionSelect.handleEvent(event)
                    potionPick = self._potionSelect.getItemSelected()
                    if potionPick != None:
                        heal(self._player,potionPick) # the model is changed here as told by the controller
                        self._playerDone = True
                        
                        # Show the player's move on the screen
                        self._combatText.setText("You healed with a potion!")
                    
                if self._menuSelection == 4: # handles retreat
                    retreat(self._player)
                    if self._retreatScreen == None:
                        # are you sure? popup window should be drawn here
                        self._retreatScreen = RetreatScreen(self._player) 
                    self._backWorld.handleEvent(event, self.setActive, False)
                    if not self.isActive():
                        return (0,)    
        else:
            self._animalStats = None # could be in update

        if self._victoryScreen != None:
            self._victoryScreen.handleEvent(event)
            self._backWorld.handleEvent(event, self.setActive, False)
            if not self.isActive():
                return (0,)

    def update(self, ticks):
        if self._enemies.isDead() and self._victoryScreen == None:
            self._victoryScreen = VictoryScreen(self._enemies,self._player)
  
        self._combatSprites = [x for x in self._combatSprites if not x.getHealthBar().getEntity().isDead()] # the model is updated here as told by the controller
        for x in self._combatSprites:
            x.update(ticks)
        self._enemyStrength.setText("Total Strength: "+str(sum([x.getStrength() for x in self._enemies if x!= None])))
        self._allyStrength.setText("Total Strength: "+str(sum([x.getStrength() for x in self._allies if x!= None])))
        self._allies.updatePack() # the model is updated here
        self._enemies.updatePack() # the model is updated here
        if self._victoryScreen != None:
            self._victoryScreen.update()
        if self._animalStats != None:
            self._animalStats.update()

        if not self._enemies.isDead():
            if self._playerDone:
                self._npcTurnTimer -= ticks
                if self._npcTurnTimer <= 0:
                    self._npcTurnTimer = self._npcTurnLength
                    self._combatOrder.getNext()
                    self._playerDone = False
                    self._menuSelection = None
                
            if self._current != self._combatOrder.getCurrent():
                self._creatureSpriteMap[self._current].deselect()
                self._current = self._combatOrder.getCurrent()
                if self._current == self._player:
                    self._movesMenu.display()
                self._creatureSpriteMap[self._current].select()

            if self._current != self._player:
                if not self._npcDone:
                    if self._current in self._allies.getTrueMembers():
                        self._current.move(self._enemies.getTrueMembers())
                        self._orbColor = (15,245,107)
                    else:
                        self._current.move(self._allies.getTrueMembers())
                        self._orbColor = (222,44,44)

                    # Replace the player's name with you (use reverses to find the last instance of the name)
                    text = self._current.getCombatStatus()
                    text = text[::-1].replace(self._player.getName()[::-1], "you"[::-1], 1)[::-1]
                    self._combatText.setText(text)
                    
                    self._turnText.setText(self._current.getName()+"'s turn")
                    self._npcDone = True
                self._npcTurnTimer -= ticks
                if self._npcTurnTimer <= 0:
                    self._npcTurnTimer = self._npcTurnLength
                    self._combatOrder.getNext()
                    self._npcDone = False
                
            
            else:
                if self._potionSelect != None:
                    self._potions = [x for x in self._player.getInventory() \
                               if x.getAttribute("type") == "potion"]
                    self._potionSelect.resetItems(self._potions)
                    self._potionSelect.update()
                    centerGraphicsElement(self._potionSelect,axes=(True, False))
                self._turnText.setText("Your turn")
                self._orbColor = (255,255,255)
            
                
        SOUNDS.manageSongs("combat")
            
        


        


