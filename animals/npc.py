
from .animal import Animal
from graphics.popup import Popup
import random, pygame, copy

class NPC(Animal):


    def __init__(self, name, agression, health, speed, endurance, damage,
                 attack_speed, defense):
        
        super().__init__(name=name,
                         health=random.randint(health[0],health[1]),
                         speed=random.randint(speed[0],speed[1]),
                         endurance=random.randint(endurance[0],endurance[1]),
                         combatDamage=random.randint(damage[0],damage[1]),
                         attackSpeed=random.randint(attack_speed[0],attack_speed[1]),
                         defensiveStat=random.randint(defense[0],defense[1]))
        
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

            

