import pygame,random
from modules import Drawable,Vector2
from animals import *
from graphics import *
from .combatUtils import *
from stateMachines import combatStartState,combatPlayerStates,\
     playerTransitions, combatFSM
import time
from items.items import *
from minigame.itemselect import ItemSelect
from minigame.subcombatlevel import SubCombatLevel
from level import Level
from modules.drawable import Drawable
from modules.soundManager import SoundManager

class CombatLevel(Level):

    def __init__(self, player, SCREEN_SIZE,allies,enemies,screen):
        super().__init__()

        self._SCREEN_SIZE = (1200,500)

        self._songs = ["battle1.mp3","battle2.mp3"]
        self._currentSong = random.choice(self._songs)

        self._player = player
        self._allies = allies
        self._enemies = enemies
        self._screen = screen

        self._font = pygame.font.SysFont("Times New Roman", 20)
        self._textFont = pygame.font.SysFont("Times New Roman", 28)

        self._background = Drawable("merchantForest2.png",
                                    (0,0), worldBound=False)

        SoundManager.getInstance().playMusic(self._currentSong)

        self._combatSprites = list()
        self.createCombatSprites()

        self._lev = SubCombatLevel(self._screen,self._allies,self._enemies,self._combatSprites)
        self._backWorld = Button("Back to World",(875,210),self._font,(0,0,0),
                                 (124,252,0),80,150,borderWidth = 2)

    def createCombatSprites(self):
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
        self._background.draw(screen)
        if combatFSM.getCurrentState() == "player turn":
            self._lev.drawPlayerTurn()

        elif combatFSM.getCurrentState() == "fortify": 
            self._lev.drawFortify()
 
        elif combatFSM.getCurrentState() == "attack":
            self._lev.drawAttack()

        elif combatFSM.getCurrentState() == "heal":
            self._lev.drawHeal()
            self._lev.updateHeal()

        elif combatFSM.getCurrentState() == "waiting":
            self._lev.updateWait()
            self._lev.update()
            self._lev.drawWait()
            time.sleep(1.2)

        elif combatFSM.getCurrentState() == "victory":
            self._lev.drawVictory()
            self._backWorld.draw(self._screen)

        elif combatFSM.getCurrentState() == "retreat":
            self._lev.drawRetreat()
            self._backWorld.draw(self._screen)

        elif combatFSM.getCurrentState() == "dead":
            self._lev.drawDead()

    def handleEvent(self, event):
        self._lev.handleEvent(event) # for the item popups

        if combatFSM.getCurrentState() == "heal":
            self._lev.handleHeal(event)

        elif combatFSM.getCurrentState() == "player turn":
            self._lev.handlePlayerTurn(event)

        elif combatFSM.getCurrentState() == "attack":
            self._lev.handleAttack(event)
                            
        elif combatFSM.getCurrentState() == "fortify":
            self._lev.handleFortify(event)
                            
        elif combatFSM.getCurrentState() == "retreat":
            retreat(self._allies[0])
            self._backWorld.handleEvent(event, self.setActive, False)
            if not self.isActive():
                combatFSM.changeState("exit")
                return (0,)
            
        elif combatFSM.getCurrentState() == "victory":
            self._lev.handleVictory(event)
            self._backWorld.handleEvent(event, self.setActive, False)
            if not self.isActive():
                combatFSM.changeState("exit")
                return (0,)

    def update(self, ticks):
        if combatFSM.getCurrentState() != "waiting":
            self._lev.update()
