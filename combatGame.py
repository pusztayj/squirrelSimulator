
from animal import Animal
from chipmunk import Chipmunk
from fox import Fox
from bear import Bear
from deer import Deer
import item, random, buff, pack
from utils import *

class CombatGame():

    def __init__(self, allies, enemies):
        """Initializes a combat minigame"""
        self._player = allies.getLeader()
        self._allies = allies
        self._enemies = enemies

    def getAllies(self):
        return self._allies

    def getEnemies(self):
        return self._enemies

    def gameLoop(self):
        """The main loop for the combat minigame"""
        while (not self._player.isDead()) and \
              (not self._enemies.getSize()==0):
            self.gameCycle()
        if self._player.isDead():
            print(self._player.getName(), "is dead...")
        if self._enemies.getSize() == 0:
            print("All enemies have been defeated")

    def gameCycle(self):
        """An individual game cycle"""
        
        # Player Attack
        target = int(input("Choose a target " + str([x+1 for x in range(len(self._enemies))]) + ": "))
        assert type(target)==int
        target = self._enemies[target-1]
        print(self._player.getName(), "attacks", target.getName())
        self.fight(self._player, target)
        self._enemies.updatePack()

        # Allied Attack
        for ally in self._allies:
            if ally != self._player and len(self._enemies) > 0:
                target = self._enemies[random.randint(0,len(self._enemies)-1)]
                print(ally.getName(), "attacks", target.getName())
                self.fight(ally, target)
                self._enemies.updatePack()
    
        # Enemy Attack
        for enemy in self._enemies:
            target = self._allies[random.randint(0,len(self._enemies)-1)]
            print(enemy.getName(), "attacks", target.getName())
            self.fight(enemy, target)
            self._allies.updatePack()

        # Stat Regen
        ##Increase stamina back here

    def fight(self, entityOne, entityTwo):
        """Simulates a fight between two enemies"""
        attackStat = entityOne.dealDamage()
        defenseStat = entityTwo.defend()
        damageDealt = max(0, attackStat - defenseStat)
        if entityOne.hasToolInHand():
            if random.randint(0,4)==0:
                entityOne.getToolInHand().decrementDurability()
        print(damageDealt, "damage dealt")
        entityTwo.loseHealth(damageDealt)

if __name__=="__main__":

    # Create the allies
    c1 = Chipmunk("Alvin")
    c2 = Chipmunk("Simon")
    c3 = Chipmunk("Theodore")
    stick1 = item.Stick(20)
    stick1.rename("Breath Taker")
    stick2 = item.Stick(10)
    stick2.rename("Call of the Wild")
    stick3 = item.Stick(15)
    stick3.rename("Bane of Bears")
    c1.equipTool(stick1)
    c2.equipTool(stick2)
    c3.equipTool(stick3)
    allies = pack.Pack(c1)
    allies.addMember(c2)
    allies.addMember(c3)

    # Create the enemies
    b1 = Chipmunk("Monk of Ages")
    b2 = Fox("Mr. Fox")
    b3 = Chipmunk("The Chunk Munk")
    enemies = pack.Pack(b1)
    enemies.addMember(b2)
    enemies.addMember(b3)

    #Begin the game
    game = CombatGame(allies, enemies)
    game.gameLoop()
    
            
        
