from animals.pack import Pack

class TurnOrder():

    def __init__(self, allies, enemies):

        self._allies = allies
        self._enemies = enemies
        
        self._current = self._allies[0]
        self._lastIndex = 0

    def getCurrent(self):
        """Get the current combatant"""
        return self._current

    def getOrder(self):
        """Return the current combat order"""
        currentAllies = self._allies.getTrueMembers()
        currentEnemies = self._enemies.getTrueMembers()
        largestPackSize = max(len(currentAllies),len(currentEnemies))
        order = []
        for x in range(largestPackSize):
            if x < len(currentAllies):
                order.append(currentAllies[x])
            if x < len(currentEnemies):
                order.append(currentEnemies[x])
        return order

    def getNext(self):
        """Get the next combatant (assumes a player can't
        die on their own turn)"""
        order = self.getOrder()
        currentIndex = order.index(self._current)
        if currentIndex == len(order)-1:
            newCurrentIndex = 0
        else:
            newCurrentIndex = currentIndex + 1
        self._current = order[newCurrentIndex]
        self._lastIndex = newCurrentIndex
        return self._current
