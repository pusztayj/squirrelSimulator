
import pygame
from .utils import *
from minigame.level import Level
from polybius.graphics import Drawable
from polybius.managers import CONSTANTS, SOUNDS, CONTROLS
from managers import USER_INTERFACE
from polybius.graphics.ui.menu import Menu
from polybius.graphics import *
from polybius.utils import Timer

from minigame.itemselect import ItemSelect

class CombatLevel(Level):

    def __init__(self,allies,enemies):
        super().__init__()

        self._screen_size = CONSTANTS.get("screen_size")

        self._player = allies.getLeader()
        self._allies = allies
        self._enemies = enemies
        
        self._combatOrder = TurnOrder(self._allies, self._enemies)
        self._current = self._combatOrder.getCurrent()
        
        self._npcTurnLength = 3
        self._npcTurnTimer = Timer(self._npcTurnLength)

        self._font = pygame.font.SysFont("Times New Roman", 20)
        self._textFont = pygame.font.SysFont("Times New Roman", 28)
        self._popupFont = pygame.font.SysFont("Times New Roman", 14) 

        # make the background
        self._background = Drawable("merchantForest2.png",
                                    (0,0), worldBound=False)

        self.initializeWidgets()

        SOUNDS.manageSongs("combat")
        self.initializeCombatSprites()
        self._orbColor = (255,255,255)
        self.initializeTextElements() 
        self.initializeVictoryItems()
        self.initializeRetreatItems()
        self.initializeFlags()
        self._menuSelection = None

        self._exitCode = None

    def initializeFlags(self):
        self._npcDone = False
        self._playerDone = False
        self._playerAttacked = False

    def initializeCombatSprites(self):
        allies = self._allies.getTrueMembers()
        enemies = self._enemies.getTrueMembers()
        allEntities = allies + enemies
        
        self._combatSprites = createCombatSprites(self._allies, self._enemies, self._font)

        self._creatureSpriteMap = dict(zip(allEntities, self._combatSprites))

        self._spriteToCreatureMap = dict(zip(self._combatSprites, allEntities))
        
        self._creatureSpriteMap[self._current].select()

    def initializeWidgets(self):     
        self.initializeMovesMenu()
        self._backToMenuButton = Button("Go Back",(550,100),self._font,
                                        (255,255,255),(0,0,0),50,100)
        self.initializePotionSelect()
        self.initializeConfirmationWindow()
        self._animalStats = None
        self._popup = None
        self._particleText = None

    def initializeMovesMenu(self):
        combat_commands = USER_INTERFACE.getControlsForMenu("combat")
        self._movesMenu = Menu((385,100),(430, 50), combat_commands, padding=(0,0), spacing=10,
                     color=None, borderWidth=0, orientation="horizontal")

    def initializePotionSelect(self):
        self._potions = [x for x in self._allies[0].getInventory() \
                   if x.getAttribute("type") == "potion"]
        self._potionSelect = ItemSelect((0,165),self._potions)
        self._potionSelect.keepCentered(cen_point=(1/2,None))

    def initializeConfirmationWindow(self):

        # Set the fonts
        font = pygame.font.SysFont("Times New Roman", 20)
        buttonFont = pygame.font.SysFont("Times New Roman", 16)

        # Set the dimensions
        width, height = 288, 150
        dimensions = (width, height)
        buttonWidth, buttonHeight = 40, 20
        buttonDimensions = (buttonWidth, buttonHeight)

        # Set the color scheme
        fontColor = (255,255,255)
        backgroundColor = (0,0,0)
        buttonFontColor = (255,255,255)
        buttonColor = (120,120,120)

        self._confirmationWindow = ConfirmationWindow("", (0,0), dimensions,
                                            font, fontColor, backgroundColor,
                                            buttonColor, buttonDimensions,
                                            buttonFont, buttonFontColor,
                                            borderWidth=1)

        verticalCenter = 1/3 #from top of screen
        horizontalCenter = 1/2 #from left of screen
        self._confirmationWindow.center(cen_point=(horizontalCenter, verticalCenter))
        self._confirmationWindow.close()
        

    def initializeVictoryItems(self):
        self._victoryScreen = None
        self._victoryScreenProper = VictoryScreen(self._enemies,self._player)

    def initializeRetreatItems(self):
        self._retreatScreen = None
        # should probably refactor to be inside victory and retreat screens
        self._backWorld = Button("Back to World",(875,210),self._font,(0,0,0),
                            (124,252,0),80,150,borderWidth = 2)

    def initializeTextElements(self):

        self._moveText = TextBox("",(0,0),self._textFont,(255,255,255))

        self._turnText = TextBox("Your turn",(0,470),self._font,(255,255,255))
        self._turnText.keepCentered(cen_point=(1/2,None))

        self._combatText = TextBox("",(600,100),self._textFont,(255,255,255))
        self._combatText.keepCentered(cen_point=(1/2,None))
        
        ### RIPE FOR REFACTOR ###
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

    def drawCombatSprites(self, screen):
        for x in self._combatSprites:
            x.draw(screen)

    def drawTurnOrb(self, screen):
        position = (600,435)
        radius = 25
        pygame.draw.circle(screen,self._orbColor,position,radius)

    def drawInfoElements(self, screen):
        self._turnText.draw(screen)
        self._allyText.draw(screen)
        self._allyStrength.draw(screen)
        self._enemyStrength.draw(screen)
        self._enemyText.draw(screen)
        if self._popup != None:
            self._popup.draw(screen)

    def drawAnimalStats(self, screen):
        if self._animalStats != None:
            self._animalStats.draw(screen)

    def drawPlayerAttackState(self, screen):
        self._backToMenuButton.draw(screen)
        self._moveText.setText("Click on enemy animal to proceed with attack")
        self._moveText.setPosition((0,200))
        self._moveText.center(cen_point=(1/2,None))
        self._moveText.draw(screen)

    def drawPlayerHealState(self, screen):
        if len(self._potions) > 0:
            self._potionSelect.draw(screen)
            self._moveText.setText("Click on a potion to heal")
            self._moveText.setPosition((0,225))
            self._moveText.center(cen_point=(1/2,None))
            self._moveText.draw(screen)
        else:
            self._moveText.setText("You have no potions!")
            self._moveText.setPosition((0,225))
            self._moveText.center(cen_point=(1/2,None))
            self._moveText.draw(screen)
        self._backToMenuButton.draw(screen)

    def drawPlayerTurnState(self, screen):
        self.drawAnimalStats(screen)
        if not self._movesMenu.getDisplay():
            if self._playerDone:
                self._combatText.draw(screen)
            elif self._menuSelection == 1:
                self.drawPlayerAttackState(screen)
            elif self._menuSelection == 3:
                self.drawPlayerHealState(screen)
        else:
            self._movesMenu.draw(screen)

    def drawRetreatScreen(self, screen):
        if self._retreatScreen != None:
            self._retreatScreen.draw(screen)
            self._backWorld.draw(screen)

    def drawVictoryScreen(self, screen):
        if self._victoryScreen != None:
            self._victoryScreen.draw(screen)
            self._backWorld.draw(screen)

    def drawParticleText(self, screen):
        if self._particleText != None:
            self._particleText.draw(screen)

    def drawConfirmationWindow(self, screen):
        if self._confirmationWindow.getDisplay():
            self._confirmationWindow.draw(screen)
        
    def draw(self, screen):
        self._background.draw(screen)
        if self._retreatScreen == None and self._victoryScreen == None:
            self.drawCombatSprites(screen)
            self.drawTurnOrb(screen)
            self.drawInfoElements(screen)
            self.drawParticleText(screen)
            if self._current == self._player:
                self.drawPlayerTurnState(screen)
            else:
                self._combatText.draw(screen)
            self.drawConfirmationWindow(screen)
        self.drawRetreatScreen(screen)
        self.drawVictoryScreen(screen)

    def executePlayerAttack(self, creature):
        self._player.attackLogic([creature])
        attack(self._player,creature) # the model is changed here as told by the controller
        self._playerDone = True

        # Show the player's attack on the screen
        text = self._player.getCombatStatus().replace(self._player.getName(),"You",1)
        text = text.replace("You has", "You have")
        self._combatText.setText(text)
        self.createTextParticle()

        # Set the player attacked flag to true
        self._playerAttacked = True

    def getHoverStats(self, animal):
        if animal.isEquipped():
            item = animal.getEquipItem().getAttribute("name")
        else:
            item = ""
        if animal.hasArmor():
            armor = animal.getArmor().getAttribute("name")
        else:
            armor = ""
        return "Holding: " + item + \
               "\nArmor: " + armor + \
               "\nStrength: " + str(animal.getStrength())

    def handleEventOnCombatSprite(self, event):
        for sprite in self._combatSprites:
            x,y = sprite.getAnimalPosition()
            creature = self._spriteToCreatureMap[sprite]
            for rect in sprite.getCollideRects():
                r = rect.move(x,y)
                if (CONTROLS.get("display_animal_stats").check(event) and self._current == self._player):
                    if r.collidepoint(event.pos):
                        self._animalStats = AnimalStats(sprite.getAnimal(),(400,220))
                elif r.collidepoint(pygame.mouse.get_pos()):
                    movesMenuHidden = not self._movesMenu.getDisplay()
                    inAttackState = self._menuSelection == 1
                    hoveringOnEnemy = creature in self._enemies.getTrueMembers()
                    if movesMenuHidden and inAttackState and hoveringOnEnemy:
                        text = "Potential Damage: " + str(attackComputation(self._allies[0],creature))
                        if CONTROLS.get("select").check(event):
                            playerHasntAttacked = not self._playerAttacked
                            if r.collidepoint(event.pos) and playerHasntAttacked:
                                self.executePlayerAttack(creature)            
                    else:
                        animal = sprite.getAnimal()
                        text = self.getHoverStats(animal)
                        
                    self._popup = Popup(text,(pygame.mouse.get_pos()[0]+5,pygame.mouse.get_pos()[1]+5),
                                        self._popupFont,multiLine = True)

    def handleEventOnAnimalStats(self, event):
        if self._animalStats != None:
            self._animalStats.handleEvent(event)
            if self._animalStats.getDisplay() == False:
                self._animalStats = None

    def handleFortifyEvent(self):
        fortify(self._player) # the model is changed here as told by the controller
        self._playerDone = True
        self._combatText.setText("You have fortified!")

    def handleHealEvent(self, event):
        self._backToMenuButton.handleEvent(event,self._movesMenu.display)
        self._potionSelect.handleEvent(event)
        potionPick = self._potionSelect.getItemSelected()
        if potionPick != None:
            heal(self._player,potionPick) # the model is changed here as told by the controller
            self._playerDone = True
            
            # Show the player's move on the screen
            self._combatText.setText("You healed with a potion!")
            self._player._target = self._player
            self.createTextParticle()

    def handleRetreatEvent(self, event):
        self._confirmationWindow.setText("Are you sure you want to retreat?")
        self._confirmationWindow.setConfirmFunction(self.executeRetreat)
        self._confirmationWindow.display()
        self._menuSelection = None

    def executeRetreat(self):
        retreat(self._player)
        self._movesMenu.close()
        if self._retreatScreen == None:
            self._retreatScreen = RetreatScreen(self._player) 
               
    def handleEventOnPlayerTurn(self, event):
        self.handleEventOnConfirmationWindow(event)
        self.handleEventOnAnimalStats(event)
        if self._movesMenu.getDisplay() and not self._menuSelection == 4:
            self._menuSelection = self._movesMenu.handleEvent(event)
        else:
            if self._menuSelection == 1: # handles attack 
                self._backToMenuButton.handleEvent(event,self._movesMenu.display)
            if self._menuSelection == 2: # handles fortify
                self.handleFortifyEvent()
            if self._menuSelection == 3: # handles heal
                self.handleHealEvent(event)  
            if self._menuSelection == 4: # handles retreat
                self.handleRetreatEvent(event)

    def isActiveWindow(self, window):
        return not(window == None) and window.getDisplay()

    def handleEventOnConfirmationWindow(self, event):
        if self.isActiveWindow(self._confirmationWindow):
            self._confirmationWindow.handleEvent(event)

    def checkForExitCondition(self):
        if self._exitCode != None:
            return self._exitCode
        
    def handleEvent(self, event):
        self._popup = None
        self.handleEventOnCombatSprite(event)
        if self._current == self._player:
            self.handleEventOnPlayerTurn(event)
        else:
            self._animalStats = None # could be in update

        if self._victoryScreen != None:
            self._victoryScreen.handleEvent(event)
            self._backWorld.handleEvent(event, self.setActive, False)
            if not self.isActive():
                self._exitCode = (0,)
        if self._retreatScreen != None:
            self._backWorld.handleEvent(event, self.setActive, (False,))
            if not self.isActive():
                self._exitCode = (0,)
            
        return self.checkForExitCondition()

    def removeDeadCombatSprites(self):
        self._combatSprites = [sprite for sprite in self._combatSprites
                                if not sprite.getAnimal().isDead()]

    def updateCombatSprites(self, ticks):
        self.removeDeadCombatSprites()
        for sprite in self._combatSprites:
            sprite.update(ticks)

    def getTotalStrength(self, pack):
        pack = pack.getTrueMembers()
        totalPackStrength = sum([c.getStrength() for c in pack])
        return totalPackStrength

    def updateDisplayedStrengths(self):
        enemyStrength = self.getTotalStrength(self._enemies)
        self._enemyStrength.setText("Total Strength: " + str(enemyStrength))
        allyStrength = self.getTotalStrength(self._allies)
        self._allyStrength.setText("Total Strength: "+str(allyStrength))

    def updatePacks(self):
        self._allies.updatePack()
        self._enemies.updatePack()

    def goToNextTurnFromPlayer(self):
        self._combatOrder.getNext()
        self._playerDone = False
        self._menuSelection = None

    def goToNextTurnFromNPC(self):
        self._combatOrder.getNext()
        self._npcDone = False

    def updateCurrent(self):
        self._creatureSpriteMap[self._current].deselect()
        self._current = self._combatOrder.getCurrent()
        self._creatureSpriteMap[self._current].select()

    def setToPlayerTurn(self):
        self._movesMenu.display()
        self._playerAttacked = False

    def updateOrbOnNPCTurn(self):
        if self._current in self._allies.getTrueMembers():
            self._current.move(self._enemies.getTrueMembers())
            self._orbColor = (15,245,107)
        else:
            self._current.move(self._allies.getTrueMembers())
            self._orbColor = (222,44,44)

    def replaceLastInstance(self, string, target, replacement):
        s = string[::-1].replace(target[::-1], replacement[::-1], 1)[::-1]
        return s

    def updateCombatText(self):
        text = self._current.getCombatStatus()
        playerName = self._player.getName()
        text = self.replaceLastInstance(text, playerName, "you")
        self._combatText.setText(text)

    def updateTurnText(self):
        self._turnText.setText(self._current.getName()+"'s turn")

    def manageTimeFollowingPlayersTurn(self, ticks):
        self._npcTurnTimer.update(ticks, self.goToNextTurnFromPlayer)

    def updateUI(self):
        if self._enemies.isDead() and self._victoryScreen == None:
            self._victoryScreen = self._victoryScreenProper
        if self._victoryScreen != None:
            self._victoryScreen.update()
        if self._animalStats != None:
            self._animalStats.update()

    def updateNPCTurn(self, ticks):
        if not self._npcDone:
            self.updateOrbOnNPCTurn()
            self.updateCombatText()
            self.updateTurnText()
            self.createTextParticle()
            self._npcDone = True   
        self._npcTurnTimer.update(ticks, self.goToNextTurnFromNPC)

    def createTextParticle(self):

        ## The combat logic needs to be refactored for this to
        ## work at its best!!!
        
        target = self._current.getCombatTarget()
        if target != None:
            combatSprite = self._creatureSpriteMap[target]
            box = combatSprite._box

            # Calculate the position of the particle
            x, y = box._position
            w, h = box._demensions
            
            if target in self._allies:
                startPos = (x, y)
                endPos = (x, y+(h//2))
            else:
                startPos = (x+w, y)
                endPos = (x+w, y+(h//2))

            # Set the font color
            if target != self._current:
                color = (255, 0, 0)
                text = "--" # I want to replace this with the damage done
            else:
                color = (0, 255, 0)
                text = "++" # I want to replace this with the health gained
                #flip the direction of the animation
                startPos, endPos = endPos, startPos

            font = pygame.font.SysFont("Impact", 26)
            
            self._particleText = ParticleText(text, startPos, endPos, self._npcTurnLength,
                                              font, color)

            
    def updateDisplayForPlayerTurn(self):
        if self._potionSelect != None:
            self._potions = [x for x in self._player.getInventory() \
                       if x.getAttribute("type") == "potion"]
            self._potionSelect.resetItems(self._potions)
            self._potionSelect.update()
        self._turnText.setText("Your turn")
        self._orbColor = (255,255,255)

    def manageParticleText(self, ticks):
        if self._particleText != None:
            self._particleText.update(ticks)
            if self._particleText.finished():
                self._particleText = None

    def update(self, ticks):

        self.updateUI()
        self.updateCombatSprites(ticks)
        self.updateDisplayedStrengths()
        self.updatePacks()
        self.manageParticleText(ticks)
        
        allEnemiesDead = self._enemies.isDead()
        if not allEnemiesDead:
            if self._playerDone:
                self.manageTimeFollowingPlayersTurn(ticks)

            currentChanged = self._current != self._combatOrder.getCurrent()
            if currentChanged:
                self.updateCurrent()
                if self._current == self._player:
                    self.setToPlayerTurn()
                
            playersTurn = self._current == self._player
            if playersTurn:
                self.updateDisplayForPlayerTurn()
            else:
                self.updateNPCTurn(ticks)
               
        SOUNDS.manageSongs("combat")
            
        


        


