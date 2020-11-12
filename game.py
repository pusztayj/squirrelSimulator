import pygame, random, math, os, pickle
from minigame import *
from polybius.graphics.ui.menu import Menu
from graphics import FileMenu
from player import Player
from animals import *
from polybius.managers import CONSTANTS, SOUNDS, FRAMES, CONTROLS
from managers import USER_INTERFACE, NAMES, ANIMALS, ITEMS

class Game():

    def __init__(self):

        # Initialize the module
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        
        self.initializeManagers()

        self._SCREEN_SIZE = CONSTANTS.get("screen_size")
        
        # Update the title for the window
        pygame.display.set_caption('Squirrel Simulator')

        # Get the screen
        self._screen = pygame.display.set_mode(self._SCREEN_SIZE)#, pygame.FULLSCREEN)

        # Create an instance of the game clock
        self._gameClock = pygame.time.Clock()

        self.createPlayer()
        self.initializeCheatBox()
        self.initializeFileMenus()
        self.initializeLevels()
        self.initializePauseMenu()
        
        # Create the loading screen
        loadingTime = 1
        self._loading = LoadingScreen(loadingTime)

        # Create the controls scroll display
        self.initializeControlsDisplay()

        # Create the title display
        self._titleScreen = TitleScreen()

        # Create the name input interface
        self._nameInput = NameInput()

        # Create the tutorial window
        self.createTutorialWindow()

        self._flicker  = False # Used to blit the game background over the controls / tutorials
        self._lag = True #Used to ever so slightly updated paused game at start

        self._RUNNING = True

        # Set the initial game code to None
        self._code = None

        self._currentLevel = self._code

        self._windows = [self._cheatBox, self._loading, self._pauseMenu,
                       self._controls, self._tutorial, self._nameInput,
                       self._titleScreen, self._loadMenu, self._saveMenu]
        
    def initializeFileMenus(self):
        self._loadMenu = FileMenu((self._SCREEN_SIZE[0]//2 - 250,self._SCREEN_SIZE[1]//2-150),
                       (500,300), "Load")
        self._loadMenu.close()

        self._saveMenu = FileMenu((self._SCREEN_SIZE[0]//2 - 250,self._SCREEN_SIZE[1]//2-150),
                       (500,300), "Save")
        self._saveMenu.close()

        CONSTANTS.addConstant("loadMenu", self._loadMenu)
        CONSTANTS.addConstant("saveMenu", self._saveMenu)

    def createPlayer(self):
        self._player = Player(pos=CONSTANTS.get("player_start_pos"))
        self._playerPack = Pack(self._player)
        self._player.setPack(self._playerPack)
        self._player.scale(1.5)
        CONSTANTS.addConstant("player", self._player)

    def initializeLevels(self):
        self._level = MainLevel()
        self._merchantLevel = None
        self._combatLevel = None
        self._endScreen = None

    def initializeCheatBox(self):
        self._cheatBox = CheatBox(self._SCREEN_SIZE)
        CONSTANTS.addConstant("cheatbox", self._cheatBox)

    def initializePauseMenu(self):
        pWidth = self._SCREEN_SIZE[0] // 4
        pHeight = 2 * (self._SCREEN_SIZE[1] // 3)
        pause_commands = USER_INTERFACE.getControlsForMenu("pause")
        self._pauseMenu = Menu(((self._SCREEN_SIZE[0]//2 - pWidth//2), self._SCREEN_SIZE[1]//2 - pHeight//2),
                 (pWidth, pHeight), pause_commands, (37,16), -1)
        self._pauseMenu.close()

    def initializeControlsDisplay(self):
        pos = (self._SCREEN_SIZE[0]//2 - 209, self._SCREEN_SIZE[1]//2 - 100)
        self._controls = Controls(pos, 200)
        self._controls.close()

    def runGameLoop(self):
        while self.isRunning():
            self._gameClock.tick()
            self.draw()
            self.handleEvents()
            self.update()
        pygame.quit()

    def drawActiveWindows(self):
        for w in self._windows:
            if w.getDisplay():
                w.draw(self._screen)

    def isActiveLevel(self, level):
         return level != None and level.isActive()

    def drawActiveLevel(self):
        if self._level.isActive() or self._flicker:
            self._level.draw(self._screen)
            self._flicker = False

        if self.isActiveLevel(self._merchantLevel):
            self._merchantLevel.draw(self._screen)

        if self.isActiveLevel(self._combatLevel):
            self._combatLevel.draw(self._screen)

    def draw(self):
        gameOver = self._endScreen != None
        if gameOver:
            self._endScreen.draw(self._screen)
        else:
            self.drawActiveLevel()
            self.drawActiveWindows()
        pygame.display.flip()

    def handleEventsOnGameOver(self, event):
        c = self._endScreen.handleEvent(event)
        if c == 0:
            self.endGame()
        elif c == 1:
            self.restartGame()

    def endGame(self):
        self._RUNNING = False

    def restartGame(self):
        self.createPlayer()
        self.initializeLevels()
        self._lag = True
        self._nameInput = NameInput()
        if self._cheatBox.getDisplay():
            self._cheatBox.toggleDisplay()
        self._titleScreen._displayed = True

    def handleTogglingOfPauseMenu(self, event):
        pauseEvent = CONTROLS.get("pause").check(event)
        atmNotOpen = self._level._atm == None or not self._level.atm.getDisplay()
        notLoading = not self._loading.getDisplay()
        controlsDisplayClosed = not self._controls.getDisplay()  
        if pauseEvent and atmNotOpen and notLoading and controlsDisplayClosed:
            if not self.isActiveLevel(self._merchantLevel) and \
                not self.isActiveLevel(self._combatLevel):
                self._level.setActive(not self._level.isActive())
            if self._pauseMenu.getDisplay():
                self._pauseMenu.close()
            else:
                self._pauseMenu.display()
                self._player.stop()

    def handleAbstractLevelEvents(self, level, event):
        levelIsActive = self.isActiveLevel(level)
        notLoading = not self._loading.getDisplay()
        notPaused = not self._pauseMenu.getDisplay()
        if levelIsActive and notLoading and notPaused:
            self._code = level.handleEvent(event)

    def handleMainLevelEvents(self, event):
        self.handleAbstractLevelEvents(self._level, event)

    def handleMerchantLevelEvents(self, event):
        self.handleAbstractLevelEvents(self._merchantLevel, event)

    def handleCombatLevelEvents(self, event):
        self.handleAbstractLevelEvents(self._combatLevel, event)

    def handleCheatBoxEvents(self, event):
        if CONTROLS.get("display_cheat_box").check(event):
            self._cheatBox.toggleDisplay()
        cheatBoxOpen = self._cheatBox.getDisplay()
        notLoading = not self._loading.getDisplay()
        if cheatBoxOpen and notLoading:
            cheatCode = self._cheatBox.handleEvent(event)
            if cheatCode != None:
                codeCommand = cheatCode[0]
                isType1Code = codeCommand in self._cheatBox.getCodesByType(1)
                isType2Code = codeCommand in self._cheatBox.getCodesByType(2)
                isType3Code = codeCommand in self._cheatBox.getCodesByType(3)
                isType4Code = codeCommand in self._cheatBox.getCodesByType(4)
                if isType1Code and len(cheatCode)==2:
                    instructions = (codeCommand, self._player, cheatCode[1])
                    self._cheatBox.execute(instructions) 
                if isType2Code:
                    instructions = (codeCommand, self._level, cheatCode[1])
                    self._cheatBox.execute(instructions)
                if isType3Code:
                    instructions = (codeCommand, self._level, cheatCode[1],
                                 cheatCode[2], cheatCode[3])
                    self._cheatBox.execute(instructions)
                if isType4Code and len(cheatCode)==3:
                    instructions = (codeCommand, player, cheatCode[1],
                                 cheatCode[2])
                    self._cheatBox.execute(instructions)

    def handlePauseMenuEvents(self, event):
        if self._pauseMenu.getDisplay() and not self._controls.getDisplay():
            sel = self._pauseMenu.handleEvent(event)
            if sel == 1:
                if self._merchantLevel == None or not self._merchantLevel.isActive():
                   self._level.setActive(True)
            if sel == 2:
                SOUNDS.toggleMute()
            if sel == 3:
                self._tutorial.display()
            if sel == 4:
                self._controls.display()
            if sel == 5:
                self._RUNNING = False

    def handleControlsMenuEvents(self, event):
        if self._controls.getDisplay():
            self._controls.handleEvent(event)
            if not self._controls.getDisplay():
                # Allow the controls menu to be taken off the screen
                self._flicker = True

    def handleTutorialDisplayEvents(self, event):
        if self._tutorial.getDisplay():
            self._tutorial.handleEvent(event)
            if not self._tutorial.getDisplay():
                self._flicker = True

    def handleNameInputEvents(self, event):
        if self._nameInput.getDisplay():
            self._nameInput.handleEvent(event)
            if not self._nameInput.getDisplay():
                self._flicker = True
                # Update the stats display with the new name
                self._level._stats.update() 
                self._tutorial.display()

    def handleSaveGameEvent(self, event):
        if CONTROLS.get("save").check(event):
            self._saveMenu.display()
            self._level.setActive(False)
            self._player.stop()

    def handleLoadGameEvent(self, event):
        if CONTROLS.get("load").check(event):
            self._loadMenu.display()
            self._level.setActive(False)
            self._player.stop()

    def handleFileManagerEvents(self, event):
        if self._loadMenu.getDisplay():
            sel = self._loadMenu.handleEvent(event, self.unpauseGame)
            if sel != None: self.loadGame(sel)
        if self._saveMenu.getDisplay():
            sel = self._saveMenu.handleEvent(event, self.unpauseGame)
            if sel != None: self.saveGame(sel)

    def unpauseGame(self):
        if not self.isActiveLevel(self._merchantLevel) and \
            not self.isActiveLevel(self._combatLevel):
                self._level.setActive(True)

    def handleEvents(self): 
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                self._RUNNING = False   
            if self._titleScreen.getDisplay():
                self._titleScreen.handleEvent(event)
            else:    
                if not self._tutorial.getDisplay() and not self._nameInput.getDisplay():
                    if self._endScreen != None:
                        self.handleEventsOnGameOver(event)    
                    else:
                        self.handleTogglingOfPauseMenu(event)
                        self.handleMainLevelEvents(event)
                        self.handleMerchantLevelEvents(event)
                        self.handleCombatLevelEvents(event)
                        self.handleCheatBoxEvents(event)
                        self.handlePauseMenuEvents(event)
                        self.handleControlsMenuEvents(event)

                        if not self.isActiveLevel(self._combatLevel):
                            self.handleSaveGameEvent(event)
                            self.handleLoadGameEvent(event)
                            self.handleFileManagerEvents(event)
                else:
                     self.handleTutorialDisplayEvents(event)
                     self.handleNameInputEvents(event)

    def setGameModeToMerchant(self):
        self._level.setActive(False)
        SOUNDS.fadeOut(1000)
        merch = self._code[1]
        self._merchantLevel = MerchantLevel(self._player, merch)
        self._code = None
        self._player.stop()
        self._loading.setDisplay(True)
        

    def setGameModeToMain(self):
        SOUNDS.fadeOut(1000)
        self._level.setActive(True)
        self._code = None
        self._loading.setDisplay(True)

    def setGameModeToCombat(self):
        self._level.setActive(False)
        SOUNDS.fadeOut(1000)
        self._combatLevel = CombatLevel(self._code[1], self._code[2])
        self._code = None
        self._player.stop()
        self._loading.setDisplay(True)

    def manageLevelTransitions(self):
        self._currentLevel = self._code
        if self._code != None:
            if self._code[0] == 0:
                self.setGameModeToMain()
            elif self._code[0] == 1:
                self.setGameModeToMerchant()
            elif self._code[0] == 2:
                self.setGameModeToCombat()

    def createAndTransitionToEndScreen(self):
        SOUNDS.fadeOut(1000)
        self._endScreen = EndScreen(self._player)

    def blitLevelForDisplay(self, ticks):
        if self._lag:
            self._lag = False
            self._level.update(ticks)

    def updateAbstractLevel(self, level, ticks):
        levelIsActive = self.isActiveLevel(level)
        notLoading = not self._loading.getDisplay()
        if levelIsActive and notLoading:
            level.update(ticks)

    def updateMainLevel(self, ticks):
        self.updateAbstractLevel(self._level, ticks)
        
    def updateMerchantLevel(self, ticks):
        self.updateAbstractLevel(self._merchantLevel, ticks)

    def updateCombatLevel(self, ticks):
        self.updateAbstractLevel(self._combatLevel, ticks)
            
    def update(self):
        
        ticks = self._gameClock.get_time() / 1000
        self.manageLevelTransitions()
        
        # Update the title screen
        if self._titleScreen.getDisplay():
             self._titleScreen.update(ticks)
             
        # Create the end screen
        elif self._player.isDead() and self._endScreen == None:
            self.createAndTransitionToEndScreen()
            
        # Update the end screen
        elif self._endScreen != None:
            self._endScreen.update()
            
        # Load the level briefly to create a display behind the tutorial
        elif self._tutorial.getDisplay() or self._nameInput.getDisplay():
            self.blitLevelForDisplay(ticks)
            
        else:
            self.updateMainLevel(ticks)
            self.updateMerchantLevel(ticks)
            self.updateCombatLevel(ticks)
            
            # Update the cheat box
            if self._cheatBox.getDisplay():
                self._cheatBox.update(ticks)

            # Update the loading screen
            if self._loading.getDisplay():
                self._loading.update(ticks)

    def isRunning(self):
        return self._RUNNING

    def createTutorialWindow(self):
        instruct = ["Welcome to Squirrel Simulator",
             "Hit ESC to pause the game",
             "Use WASD to move",    
             "You must eat acorns to survive.\nCollect them and hit space\nto eat them",
             "Click on animals and merchant huts\nto interact with them",
             "Animals can belong to packs.\nHit E to view your pack",
             "You gain XP points over time.\nHit R to view XP chart",
             "You can only carry so many acorns.\nHit B to bury acorns.\nYou can dig up piles by right\nclicking with selected tool",
             "Right click to use and equip items"]

        self._tutorial = Instructions((self._SCREEN_SIZE[0]//2-150,
                                self._SCREEN_SIZE[1]//2-100),
                               instruct)
        self._tutorial.close()

    def saveGame(self, fileName):
        data = self._level.exportData()
        data.makePickleSafe()
        path = os.path.join("saves", fileName+".sqs")
        with open(path, "wb") as file:
            pickle.dump(data, file)
        data.undoPickleSafe()
        self.unpauseGame()

    def loadGame(self, fileName):
        path = os.path.join("saves",fileName+".sqs")
        with open(path, "rb") as file:
            data = pickle.load(file)
            data.undoPickleSafe()
            self._level.importData(data)
        self._player = CONSTANTS.get("player")
        self._code = (0,)
        self.manageLevelTransitions()

    def initializeManagers(self):
        """A function that sets the resource paths for the various managers"""

        SOUNDS.setResourcePath(os.path.join("resources","data","music.csv"))
        SOUNDS.setMusicFolderPath(os.path.join("resources","sounds","music"))
        SOUNDS.setSFXFolderPath(os.path.join("resources","sounds","sfx"))

        FRAMES.prepareImagesFromCSV(os.path.join("resources","data","images.csv"),
                                   os.path.join("resources","images"))

        CONTROLS.setResourcePath(os.path.join("resources","data","default_controls.csv"))

        CONSTANTS.setResourcePath(os.path.join("resources","data","constants.csv"))

        NAMES.setResourcePath(os.path.join("resources","data","names.csv"))
        ITEMS.setResourcePath(os.path.join("resources","data","items.csv"))
        ANIMALS.setResourcePath(os.path.join("resources","data","animals.csv"))
        USER_INTERFACE.setResourcePath(os.path.join("resources","data","menuButtons.csv"))
