
from .animal import Animal
from graphics.popup import Popup
import random, pygame, copy
from items.items import *
from combatutils import *

class NPC(Animal):


    def __init__(self, name, agression, speed, endurance,
                 attack_speed,strength):
        
        super().__init__(name=name,
                         health=100,
                         speed=random.randint(speed[0],speed[1]),
                         endurance=random.randint(endurance[0],endurance[1]),
                         strength = strength,
                         attackSpeed=random.randint(attack_speed[0],attack_speed[1]))
        
        self._aggressionLevel = agression
        #self._realImage = copy.copy(self._image)

    def handleEvent(self, event, screen):     
        popupFont = pygame.font.SysFont("Times New Roman", 16)
        x,y = self.getPosition()
        pos = pygame.mouse.get_pos()
        for rect in self.getCollideRects(): 
            r = rect.move(x,y)
            if r.collidepoint(pos):
                print("yeah")
                #self._image = copy.copy(self._realImage)
                popup = Popup(self.getName(), (pos[0]+5,pos[1]+5),
                                popupFont)
                popup.draw(screen)
                break
##        else:
            #self._image = copy.copy(self._realImage)

    def healLogic(self,opponents):
        # opponents is a list
        damage = [(type(x),attackComputation(self,x)) for x in opponents]

        print(damage)
            
        if self._health <= 20:
            for x in self._inventory:
                if type(x) == type(Potions()) and self._health <= 20:
                    heal(self,x)
         
            
            

            

