
from npc import NPC
from animated import Animated

AGGRESSION   = (8,10)
HEALTH       = (50,75)
SPEED        = (15,20)
ENDURANCE    = (8,10)
DAMAGE       = (20,24)
ATTACK_SPEED = (6,8)
DEFENSE      = (10,12)

class Rabbit(NPC, Animated):

    def __init__(self, name="", pos=(0,0)):

        NPC.__init__(self, name, AGGRESSION, HEALTH, SPEED,
                         ENDURANCE,DAMAGE,ATTACK_SPEED,DEFENSE)

        Animated.__init__(self, "tempRabbit.png", pos)
