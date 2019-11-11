
from .animal import Animal
from graphics.popup import Popup
import random, pygame, copy
from items.items import *
from combatUtils import *

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
        damage = [(type(x),attackComputation(self,x),x.getHealth()) \
                  for x in opponents]
        attacks = [x for x in damage if x[1] >= x[2]]
        if self._health <= 20 and len(attacks) == 0:
            for x in self._inventory:
                if type(x) == type(Potions()) and self._health <= 20:
                    return True
            return False
        else:
            return False
        
    def fortifyLogic(self,opponents):
        if self.getHealth() >= 20 and self.getHealth() <= 75:
            damage = [(type(x),attackComputation(self,x),x.getHealth()) \
                      for x in opponents]
            attacks = [x for x in damage if x[1] <= 5]
            print(damage)
            if len(attacks) == len(opponents):
                return True
            elif 6 < random.randint(0,9):
                return True
            else:
                return False
        else:
            return False

    def attackLogic(self,opponents):
        damage = [(type(x),attackComputation(self,x),x.getHealth()) \
                  for x in opponents]
        kills = [x for x in damage if x[1] >= x[2]]
        if len(kills) > 0:
            return kills[0]
        else:
            damage.sort(key = lambda x: x[1])
            return damage[-1]
        

        
         
            
            

            

