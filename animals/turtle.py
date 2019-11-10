from .npc import NPC
from modules.animated import Animated
from modules.drawable import Drawable

AGGRESSION   = (0,5)
SPEED        = (15,20)
ENDURANCE    = (8,10)
ATTACK_SPEED = (3,4)
STRENGTH     = 10

class Turtle(NPC, Drawable):

    def __init__(self, name="", pos=(0,0), worldBound=True):

        NPC.__init__(self,name, AGGRESSION, SPEED,
                         ENDURANCE,ATTACK_SPEED,STRENGTH)
        Drawable.__init__(self, "turtle.png", pos, worldBound=worldBound)
