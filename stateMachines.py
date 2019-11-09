
from fsm import *

playerStartState = "standing"
playerStates = ["standing","walking"]
playerTransitions = [Rule("standing","walk","walking"),
                     Rule("walking","walk","walking"),
                     Rule("walking","stop","standing"),
                     Rule("standing","stop","standing"),
                     Rule("standing","bury","digging"),
                     Rule("walking","bury","digging"),
                     Rule("digging","done","standing")]
playerFSM = FSM(playerStartState, playerStates, playerTransitions)

# A Finite State Machine for the Combat Game
combatStartState = "options_menu"
combatStates = ["options_menu", "attack",
                "block", "use_item",
                "retreat", "target_selected",
                "player_attack","allied_options",
                "enemy_options","increase_defense",
                "item_selected","apply_item",
                "win","lose", "allied_deal_damage",
                "allied_increase_defense","allied_apply_item",
                "enemy_retreat","enemy_deal_damage",
                "enemy_use_item","enemy_increase_defense"]
combatActions = [Rule("options_menu","attack","attack"),
                 Rule("options_menu","block","block"),
                 Rule("options_menu","use_item","use_item"),
                 Rule("options_menu","retreat","retreat"),
                 Rule("attack","select_target","target_selected"),
                 Rule("block","confirm","increase_defense"),
                 Rule("use_item","select_item","item_selected"),
                 Rule("retreat","confirm","lose"),
                 Rule("attack", "back", "options_menu"),
                 Rule("block","back","options_menu"),
                 Rule("use_item","back","options_menu"),
                 Rule("retreat","back","options_menu"),
                 Rule("target_selected","select_target","target_selected"),
                 Rule("item_selected","select_item","item_selected"),
                 Rule("target_selected","confirm","player_attack"),
                 Rule("player_attack","all_enemies_dead","win"),
                 Rule("player_attack","has_new_ally","allied_options"),
                 Rule("player_attack","no_new_ally","enemy_options"),
                 Rule("allied_options","allied_attack","allied_deal_damage"),
                 Rule("allied_options","allied_block","allied_increase_defense"),
                 Rule("allied_options","allied_use_item","allied_apply_item"),
                 Rule("allied_deal_damage","has_new_ally","allied_options"),
                 Rule("allied_deal_damage","no_new_ally","enemy_options"),
                 Rule("allied_deal_damage","all_enemies_dead","win"),
                 Rule("enemy_options","enemy_attack","enemy_deal_damage"),
                 Rule("enemy_deal_damage","has_new_enemy","enemy_options"),
                 Rule("enemy_deal_damage","no_new_enemy","options_menu"),
                 Rule("enemy_deal_damage","player_dead","lose")
                 ]
combatFSM = FSM(combatStartState, combatStates, combatActions)

print(len(combatActions))
