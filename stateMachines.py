
from fsm import *

playerStartState = "standing"
playerStates = ["standing","walking"]
playerTransitions = [Rule("standing","walk","walking"),
                     Rule("walking","walk","walking"),
                     Rule("walking","stop","standing"),
                     Rule("standing","stop","standing"),
                     Rule("standing","bury","digging"),
                     Rule("walking","bury","digging"),
                     Rule("digging","done","standing"),
                     Rule("standing","eat","eating"),
                     Rule("walking","eat","eating"),
                     Rule("eating","done","standing")]
playerFSM = FSM(playerStartState, playerStates, playerTransitions)
