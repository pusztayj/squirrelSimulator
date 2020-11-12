
class GameData():

    def saveTimers(self, timers):
        self._timers = timers

    def saveEntities(self, player, packs, merchants):
        self._player = player
        self._packs = packs
        self._merchants = merchants

    def saveEnvironment(self, acorns, piles, trees, time):
        self._acorns = acorns
        self._piles = piles
        self._trees = trees
        self._time = time

    def makeCreaturePickleSafe(self, c):
        c.makePickleSafe()
        if c.hasArmor():
            c.getArmor().makePickleSafe()
        if c.isEquipped():
            c.getEquipItem().makePickleSafe()
        for i in c.getInventory().getItems():
            i.makePickleSafe()

    def undoCreaturePickleSafe(self, c):
        c.undoPickleSafe()
        if c.hasArmor():
            c.getArmor().undoPickleSafe()
        if c.isEquipped():
            c.getEquipItem().undoPickleSafe()
        for i in c.getInventory().getItems():
            i.undoPickleSafe()

    def makePickleSafe(self):
        for c in self._player.getPack().getTrueMembers():
            self.makeCreaturePickleSafe(c)    
        for p in self._packs:
            for c in p.getTrueMembers():
                self.makeCreaturePickleSafe(c)
        for m in self._merchants:
            m.makePickleSafe()
            for i in m.getInventory().getItems():
                i.makePickleSafe()
        for a in self._acorns:
            a.makePickleSafe()
        for p in self._piles.getAllPiles():
            p.makePickleSafe()
        for t in self._trees:
            t.makePickleSafe()

    def undoPickleSafe(self):
        for c in self._player.getPack().getTrueMembers():
            self.undoCreaturePickleSafe(c)
        for p in self._packs:
            for c in p.getTrueMembers():
                self.undoCreaturePickleSafe(c)
        for m in self._merchants:
            m.undoPickleSafe()
            for i in m.getInventory().getItems():
                i.undoPickleSafe()
        for a in self._acorns:
            a.undoPickleSafe()
        for p in self._piles.getAllPiles():
            p.undoPickleSafe()
        for t in self._trees:
            t.undoPickleSafe()
