
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


combatStartState = "player turn"
combatPlayerStates = ["player turn","attack","waiting","retreat",
                      "heal","fortify"]
playerTransitions = [Rule("player turn","attack button","attack"),
                     Rule("attack","go back","player turn"),
                     Rule("attack","animal click","waiting"),
                     Rule("waiting","done","player turn"),
                     Rule("player turn","heal button","heal"),
                     Rule("player turn","fortify button","fortify"),
                     Rule("player turn","retreat button","retreat"),
                     Rule("heal","action complete","waiting"),
                     Rule("fortify","action complete","waiting")]
combatFSM = FSM(combatStartState,combatPlayerStates,playerTransitions)



