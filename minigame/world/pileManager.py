
class PileManager():

    def __init__(self):
        self._spawnedPiles = []
        self._playerPiles  = []

    def addSpawnedPile(self, pile):
        self._spawnedPiles.append(pile)

    def addPlayerPile(self, pile):
        self._playerPiles.append(pile)

    def abandonPile(self, pile):
        self._playerPiles.remove(pile)
        pile.setName("Abandoned Pile")
        self._spawnedPiles.append(pile)

    def removePile(self, pile):
        if pile in self._spawnedPiles:
            self._spawnedPiles.remove(pile)
        if pile in self._playerPiles:
            self._playerPiles.remove(pile)

    def getNumberOfPlayerPiles(self):
        return len(self._playerPiles)

    def getPlayerPiles(self):
        return self._playerPiles

    def getSpawnedPiles(self):
        return self._spawnedPiles

    def getAllPiles(self):
        return self._playerPiles + self._spawnedPiles
