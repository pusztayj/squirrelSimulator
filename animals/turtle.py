from .npc import NPC
from modules.animated import Animated
from modules.drawable import Drawable

AGGRESSION   = (0,5)
HEALTH       = (25,30)
SPEED        = (15,20)
ENDURANCE    = (8,10)
DAMAGE       = (12,15)
ATTACK_SPEED = (3,4)
DEFENSE      = (6,8)

class Turtle(NPC, Drawable):

    def __init__(self, name="", pos=(0,0), worldBound=True):

        NPC.__init__(self,name, AGGRESSION, HEALTH, SPEED,
                         ENDURANCE,DAMAGE,ATTACK_SPEED,DEFENSE)
        Drawable.__init__(self, "turtle.png", pos, worldBound=worldBound)
