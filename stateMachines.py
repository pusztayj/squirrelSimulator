"""
In this file we create the state machine instances for the state
machines that we need. 
"""
from polybius.utils.fsm import *

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

npcStartState = "standing"
npcStates = ["standing","walking"]
npcTransitions = [Rule("standing","walk","walking"),
                     Rule("walking","walk","walking"),
                     Rule("walking","stop","standing"),
                     Rule("standing","stop","standing")]
npcFSM = FSM(npcStartState, npcStates, npcTransitions)





