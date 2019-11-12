from .npc import NPC

AGGRESSION   = (0,5)
SPEED        = (15,20)
ENDURANCE    = (8,10)
ATTACK_SPEED = (3,4)
STRENGTH     = 10

class Turtle(NPC):

    def __init__(self, name="", pos=(0,0), worldBound=True):

        NPC.__init__(self,name,"turtle.png", pos,AGGRESSION, SPEED,
                         ENDURANCE,ATTACK_SPEED,STRENGTH)
        self.setWorldBound(worldBound)
