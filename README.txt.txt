A game made by Justin Pusztay and Trevor Stalnaker

## Overview ##
In the fast paced world of Squirrel Simulator, the player guides a squirrel through a forested wood 
in the hopes of stashing enough nuts to survive. The player must be on guard against competitors. 
Will you befriend your fellow creatures to protect your hard won acorns, or will you strive to be 
the top of the food chain.  

### How to Play ###
To play the game you must only run main.py. 

The purpose of this game is survive. There is no way to win, but the only way to lose is too die.
The only way you survive is by collecting acorns. 

These are the following controls: 
ESC:     Pause the game
WASD:    Movemvent
Space:   Eat Acorns
B:       Create a dirtpile to bury acorns
E:       view your pack.
R:       Level up your skills using XP you earn.

Other controls:
Pick up acorns by walking over them
Use buttons in combat minigame for fighting strategy
To dig up abandoned piles you must own a tool and click on pile
To equip/use items right click on the item selected on your inventory display 
Click on an animal to interact with it.
Click on merchant hut to trade

Other controls:
When interacting with an animal you can:
Fight:       Initiates combat
Befriend:    Asks the animal to join your pack
Steal:       You attempt to steal acorns from the animal
Bribe:       You attempt to bribe the animal to increase their opinion of you

In the Combat Screen:
Attack:     You attack the animal to damage to it
Fortify:    Gain 10HP and increase defense strength by 25%
Heal:       Try to heal with a health potion you have
Retreat:    Leave the combat in defeat


### Bugs/Known Issues ###
-> Squirrel Simulator displays no issues on Windows machines but crashes randomly on UNIX machines. 
	-> In our experience these crashes happen randomly but are all loading issues. It can't load
	  the font, the images, and the sound. This is a very strange issue since it loads all these 
	  items but crashes at different points in the code. For example, it loads texts with the only
  	  font that we use- Times New Roman- but then claims that it can't be loaded. A similar issue
	  occurs for our images. We did not fix this issue because it was discovered on December 6, 2019
	  around 10pm which was too late to fix it. 

-> The player can walk through trees and merchant huts.