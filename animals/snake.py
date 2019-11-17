
from .npc import NPC
from modules.animated import Animated

AGGRESSION   = (8,10)
SPEED        = (15,20)
ENDURANCE    = (8,10)
STRENGTH     = 23

class Snake(NPC):

    def __init__(self, name="", pos=(0,0)):

        NPC.__init__(self, name, "tempSnake.png", pos, AGGRESSION, SPEED,
                         ENDURANCE,STRENGTH)
