from animals.pack import Pack

class TurnOrder():

    def __init__(self, allies, enemies):

        self._allies = allies
        self._enemies = enemies

        allAnimals = self._allies.getTrueMembers() + \
                     self._enemies.getTrueMembers()

        # Create a dictionary to keep track of who has already taken their turn
        self._turnTracker = dict(zip(allAnimals,
                                     [False for x in range(len(allAnimals))]))

        # Set the ally turn flag to true
        self._allyTurn = True

        # Set the current to the player
        self._current = self._allies[0]

    def getCurrent(self):
        """Get the current combatant"""
        return self._current

    def getOrder(self):
        """Return the current combat order"""
        currentAllies = self._allies.getTrueMembers()
        currentEnemies = self._enemies.getTrueMembers()
        order= currentAllies + currentEnemies
        order.sort(key=self.prioritySort)
        return order

    def getNext(self):
        """Get the next combatant (assumes a player can't
        die on their own turn)"""

        # Set the previous turn taken to True
        self._turnTracker[self._current] = True

        # Determine which team's turn it is
        if self._allyTurn and any([not self._turnTracker[k]
                                   for k in self._enemies.getTrueMembers()]):
            self._allyTurn = False
        elif not self._allyTurn and any([not self._turnTracker[k]
                                   for k in self._allies.getTrueMembers()]):
            self._allyTurn = True

        # If the round is over, start the next one
        if self.roundOver():
            self.resetRound()

        # Determine the newest turn order
        order = self.getOrder()

        # Update the current combatant
        self._current = order[0]
        
        return self._current

    def roundOver(self):
        """Check if all combatants have had their turns"""
        currentAllies = self._allies.getTrueMembers()
        currentEnemies = self._enemies.getTrueMembers()
        return all([self._turnTracker[x] for x in currentAllies + currentEnemies])
        

    def resetRound(self):
        """Reset the combat state"""
        for key in self._turnTracker.keys():
            self._turnTracker[key] = False
        self._allyTurn = True

    def prioritySort(self, entity):
        """Sort the combatants into their turn order"""
        if entity in self._allies.getTrueMembers():
            index = self._allies.getTrueMembers().index(entity)
            teamsTurn = not self._allyTurn    
        else:
            index = self._enemies.getTrueMembers().index(entity)
            teamsTurn = self._allyTurn
        # Sort entities based on:
        # 1.) if they have already taken their turn this round
        # 2.) there position in the pack
        # 3.) which team's turn it is
        return (self._turnTracker[entity], index, teamsTurn)
        
