
from drawable import Drawable
from inventory import Inventory
import pygame

class DirtPile(Drawable):

    def __init__(self,pos,name="Unnamed Pile",capacity=10):
        super().__init__("dirtpile.png",pos)
        self._name = name
        self._acorns = 0
        self._capacity = capacity

    def getName(self):
        return self._name

    def setName(self, name):
        print("Name updated")
        self._name = name

    def isEmpty(self):
        return self._acorns == 0

    def addAcorn(self):
        self._acorns += 1

    def removeAcorn(self):
        self._acorns -= 1

    def getAcorns(self):
        return self._acorns

    def setAcorns(self, acorns):
        self._acorns = acorns

    def handleEvent(self, event, player):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
            if self.getCollideRect().collidepoint((event.pos[0] + Drawable.WINDOW_OFFSET[0],
                                                  event.pos[1] + Drawable.WINDOW_OFFSET[1])):
                if player.getCheekCapacity() - player.getAcorns() > 0:
                    player.setAcorns(player.getAcorns() + self.getAcorns())
                    self.setAcorns(0)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button==3:
            if self.getCollideRect().collidepoint((event.pos[0] + Drawable.WINDOW_OFFSET[0],
                                                  event.pos[1] + Drawable.WINDOW_OFFSET[1])):
                print(self.getAcorns())
