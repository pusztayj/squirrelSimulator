"""
@authors: Justin Pusztay, Trevor Stalnaker

In this file we have a level that manages combat. It creates an instance
of the sublevel manager and draws the approrpriate screen that needs to
be drawn for each specfic state in the finite state machine.

In this file we also create the specific combat sprites that uses the
CombatSprite class from combatUtils. We also have methods that draw,
updates, and handleEvents for the interface.
"""


import pygame,random
from modules import Drawable,Vector2
from animals import *
from graphics import *
from .combatUtils import *
from stateMachines import combatStartState,combatPlayerStates,\
     playerTransitions, combatFSM
import time
from minigame.itemselect import ItemSelect
from minigame.subcombatlevel import SubCombatLevel
from level import Level
from modules.drawable import Drawable
from modules.soundManager import SoundManager

class CombatLevel(Level):

    def __init__(self, player, SCREEN_SIZE,allies,enemies,screen):
        """
        Here we initialize our combat level manager, where we pass in
        the player, the allies pack, enemies pack and the screen/screen size.
        """
        super().__init__()

        self._SCREEN_SIZE = (1200,500)

        self._player = player
        self._allies = allies
        self._enemies = enemies
        self._screen = screen

        self._font = pygame.font.SysFont("Times New Roman", 20)
        self._textFont = pygame.font.SysFont("Times New Roman", 28)

        # make the background
        self._background = Drawable("merchantForest2.png",
                                    (0,0), worldBound=False)

        SoundManager.getInstance().manageSongs("combat")
            
        # create the combat sprites
        self._combatSprites = list()
        self.createCombatSprites()

        # create the sub level manager
        self._lev = SubCombatLevel(self._screen,self._allies,self._enemies,self._combatSprites)
        # create the back to world function
        self._backWorld = Button("Back to World",(875,210),self._font,(0,0,0),
                                 (124,252,0),80,150,borderWidth = 2)



    def createCombatSprites(self):
        """
        Here we create the combat sprite for each animal of each pack. 
        """
        y = 200
        for a in self._allies:
            if self._allies.isLeader(a):
                c = CombatSprite(a,(228,275),self._font)
                self._combatSprites.append(c)
            else:
                if a != None:
                    c = CombatSprite(a,(100,y),self._font)
                    self._combatSprites.append(c)
                    y+=150
        y = 200
        for e in self._enemies:
            if self._enemies.isLeader(e):
                c = CombatSprite(e,(847,275),self._font,enemies = True)
                self._combatSprites.append(c)
            else:
                if e != None:
                    c = CombatSprite(e,(972,y),self._font,enemies = True)
                    self._combatSprites.append(c)
                    y+=150

    def draw(self, screen):
        """
        Here we draw the combat interface based on the state.
        """
        # we always draw the background
        self._background.draw(screen)
        
        # here we draw the player turn state
        if combatFSM.getCurrentState() == "player turn":
            self._lev.drawPlayerTurn()
            
        # here we draw the fortify state
        elif combatFSM.getCurrentState() == "fortify": 
            self._lev.drawFortify()
            
        # here we draw the attack state
        elif combatFSM.getCurrentState() == "attack":
            self._lev.drawAttack()
            
        # here we draw the heal state
        elif combatFSM.getCurrentState() == "heal":
            self._lev.drawHeal()
            self._lev.updateHeal()
            
        # here we draw the wait state
        elif combatFSM.getCurrentState() == "waiting":
            """
            The wait state and combat interface need to be updated here
            since the positions of certain surfaces are set based on
            which NPC's turn it is. So they must be updated here before the
            wait state is drawn.
            """
            self._lev.updateWait()
            self._lev.update()
            self._lev.drawWait()
            time.sleep(1.2) # this time.sleep allows the player to see NPC turn
                            # along with changes in what's drawn in the GUI

        # here we draw the victory state
        elif combatFSM.getCurrentState() == "victory":
            self._lev.drawVictory()
            self._backWorld.draw(self._screen)
            
        # here we draw the retreat state
        elif combatFSM.getCurrentState() == "retreat":
            self._lev.drawRetreat()
            self._backWorld.draw(self._screen)

    def handleEvent(self, event):
        """
        In this method we handle all events for the combat interface.
        We handle each event for each state individually except for
        events that happen with every state. 
        """
        self._lev.handleEvent(event) # for the item popups

        # handles the event for the heal state
        if combatFSM.getCurrentState() == "heal":
            self._lev.handleHeal(event)
        # handles the event for the player turn state
        elif combatFSM.getCurrentState() == "player turn":
            self._lev.handlePlayerTurn(event)

        # handles the event for the attack state
        elif combatFSM.getCurrentState() == "attack":
            self._lev.handleAttack(event)

        # handles the event for the fortify state
        elif combatFSM.getCurrentState() == "fortify":
            self._lev.handleFortify(event)

        # handles the event for the retreat state 
        elif combatFSM.getCurrentState() == "retreat":
            retreat(self._allies[0])
            self._backWorld.handleEvent(event, self.setActive, False)
            if not self.isActive():
                combatFSM.changeState("exit")
                return (0,)

        # handles the event for the victory state
        elif combatFSM.getCurrentState() == "victory":
            self._lev.handleVictory(event)
            self._backWorld.handleEvent(event, self.setActive, False)
            if not self.isActive():
                combatFSM.changeState("exit")
                return (0,)

    def update(self, ticks):
        """
        In this method we update the combat interface based on state.
        """
        # here we update the wait state
        if combatFSM.getCurrentState() != "waiting":
            self._lev.update()
        SoundManager.getInstance().manageSongs("combat")
            
