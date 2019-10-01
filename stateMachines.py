
from fsm import *

# A Finite State Machine for the Combat Game
combatStartState = "options_menu"
combatStates = ["options_menu", "attack",
                "block", "use_item",
                "retreat", ]
combatActions = []
combatFSM(combatStartState, combatStates, combatActions)
