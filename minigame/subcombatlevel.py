import pygame
from modules import Drawable,Vector2
from animals import *
from graphics import *
from combatUtils import *
from stateMachines import combatStartState,combatPlayerStates,\
     playerTransitions, combatFSM
import time
from .itemselect import ItemSelect

class SubCombatLevel(object):

    def __init__(self,screen,allies,enemies,healhBars):
        self._screen = screen
        self._allies = allies
        self._enemies = enemies
        self._healthBars = healhBars
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

        self._combatText = TextBox("",(385,100),self._textFont,(255,255,255))

        self._potionSelect = None

        self._turn = True

        self._orbColor = (255,255,255)

    def alwaysDraw(self):
        for a in self._allies:
            if a != None:
                a.draw(self._screen)
        for e in self._enemies:
            if e != None:
                e.draw(self._screen)
        for x in self._healthBars:
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
        potions = [x for x in self._allies[0].getInventory() \
                   if type(x) == type(Potions())]
        self._potionSelect = ItemSelect((255,100),potions)
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
    
    def handlePlayerTurn(self,event):
        self._attackButton.handleEvent(event,combatFSM.changeState,"attack button")
        self._fortifyButton.handleEvent(event,combatFSM.changeState,"fortify button")
        self._healButton.handleEvent(event,combatFSM.changeState,"heal button")
        self._retreatButton.handleEvent(event,combatFSM.changeState,"retreat button")

    def handleAttack(self,event):
        self._attackUndoButton.handleEvent(event,combatFSM.changeState,"go back")
        if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
            for creature in self._enemies:
                x,y = creature.getPosition()
                for rect in creature.getCollideRects():
                    r = rect.move(x,y)
                    if r.collidepoint(event.pos):
                        attack(self._allies[0],creature)
                        self._enemies.updatePack()
                        combatFSM.changeState("animal click")
                        self._allies.hasAttacked()

    def handleFortify(self,event):
        fortify(self._allies[0])
        combatFSM.changeState("action complete")
        self._allies.hasAttacked()

    def handleHeal(self,event):
        self._potionSelect.handleEvent(event)
        potionPick = self._potionSelect.getItemSelected()
        if self._potionPick != None:
            heal(self._allies[0],potionPick)
            combatFSM.changeState("action complete")
        self._allies.hasAttacked()

    def update(self):
        self._healthBars = [x for x in self._healthBars if not x.getEntity().isDead()]
        for x in self._healthBars:
            x.update()
        self.updateHeal()
        self._allies.updatePack()
        self._enemies.updatePack()

    def updateHeal(self):
        if combatFSM.getCurrentState() == "heal" and self._potionSelect != None:
            self._potionSelect.update()

    def updateWait(self):
        if self._turn == True:
            move(self._enemies.getNextToAttack(),self._allies)
            self._combatText.setText(self._enemies.getNextToAttack().getCombatStatus())
            self._orbColor = (222,44,44)
            self._turnText.setText(self._enemies.getNextToAttack().getName()+"'s turn")
            self._allies.updatePack()
            self._enemies.updatePack()
            self._enemies.hasAttacked()
            self._turn = not self._turn
        elif self._turn == False and self._allies.getNextToAttack() != self._allies[0]:
            move(self._allies.getNextToAttack(),self._enemies)
            self._combatText.setText(self._allies.getNextToAttack().getCombatStatus())
            self._orbColor = (15,245,107)
            self._turnText.setText(self._allies.getNextToAttack().getName()+"'s turn")
            self._allies.updatePack()
            self._enemies.updatePack()
            self._allies.hasAttacked()
            self._turn = not self._turn
        else:
            combatFSM.changeState("done")
            
