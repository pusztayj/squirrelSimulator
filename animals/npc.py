
from .animal import Animal
from graphics.popup import Popup
import random, pygame, copy
from items.items import *
from combatUtils import *
from modules.animated import Animated

class NPC(Animal, Animated):

    def __init__(self, name, image, pos, agression, speed, endurance,
                 attack_speed,strength):

        Animated.__init__(self, image, pos)
        
        Animal.__init__(self, name=name,
                         health=100,
                         speed=random.randint(speed[0],speed[1]),
                         endurance=random.randint(endurance[0],endurance[1]),
                         strength = strength,
                         attackSpeed=random.randint(attack_speed[0],attack_speed[1]))
        
        self._aggressionLevel = agression
        self._combatStatus = ""
        #self._realImage = copy.copy(self._image)
        self._walkTimer = 5

    def getCombatStatus(self):
        return self._combatStatus

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
        damage = [(x,attackComputation(self,x),x.getHealth()) \
                  for x in opponents]
        attacks = [x for x in damage if x[1] >= x[2]]
        if self._health <= 20 and len(attacks) == 0:
            for x in self._inventory:
                if type(x) == type(Potions()) and self._health <= 20:
                    self._combatStatus = self.getName() + "healed with a potion!"
                    return True
                    
            return False
        else:
            return False
        
    def fortifyLogic(self,opponents):
        if self.getHealth() >= 20 and self.getHealth() <= 75:
            damage = [(x,attackComputation(self,x),x.getHealth()) \
                      for x in opponents]
            attacks = [x for x in damage if x[1] <= 5]
            if len(attacks) == len(opponents):
                self._combatStatus = self.getName() + "has fortified!"
                return True
            elif 6 < random.randint(0,9):
                self._combatStatus = self.getName() + "has fortified!"
                return True
            else:
                return False
        else:
            return False

    def attackLogic(self,opponents):
        damage = [(x,attackComputation(self,x),x.getHealth()) \
                  for x in opponents]
        kills = [x for x in damage if x[1] >= x[2]]
        if len(kills) > 0:
            a = kills[0][0]
            self._combatStatus = self.getName() + "has killed " + a.getName()
            return kills[0][0]
        else:
            damage.sort(key = lambda x: x[1])
            self._combatStatus = self.getName() + " did " + str(damage[-1][1])+ " damage to " + \
                                 (damage[-1][0]).getName()
            return damage[-1][0]

    def wander(self, ticks):
        if self._walkTimer <= 0:
            w_x = self._position[0] + random.randint(self._position[0] - 10, self._position[0] + 10)
            w_y = self._position[1] + random.randint(self._position[1] - 10, self._position[1] + 10)
            self._position.x = min(max(0,w_x),1000)
            self._position.y = min(max(0,w_y),2000)
            print(self._position)
            self._walkTimer = 5
        else:
            self._walkTimer -= ticks
        
