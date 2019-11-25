"""
Author: Trevor Stalnaker, Justin Pusztay
File: pack.py

A class that models a pack or clan of animals
"""

from player import Player

class Pack():

    def __init__(self, leader, name=""):
        """Initialize the pack with a leader and a max size"""
        self._maxSize = 3
        self._members = [leader, None, None]
        self._leader = leader
        self._name = name
        self._nextToAttackIndex = 0
        self._nextToAttack = self[self._nextToAttackIndex]

    def getNextToAttack(self):
        if self._nextToAttack != None and self._nextToAttack.isDead():
            return None
        else:
            return self._nextToAttack

    def getNextToAttackIndex(self):
        return self._nextToAttackIndex

    def getPackName(self):
        return self._name

    def setPackName(self, name):
        self._name = name

    def getLeader(self):
        """Return the leader of the pack"""
        return self._leader

    def isLeader(self,animal):
        return animal == self._leader

    def resetLeader(self, newLeader):
        """Reset the leader of the pack"""
        self._leader = newLeader

    def addMember(self, member):
        """Add a new member to the pack if able"""
        if None not in self._members:
            pass
        for i,animal in enumerate(self):
            if animal == None:
                self._members[i] = member
                break

    def removeMember(self, member):
        """Remove a current member of the pack"""
        self._members = [None if m==member else m for m in self._members]
##        if member in self._members:
##            self._members.replace(member,None)

    def getMembers(self):
        """Return the members of the pack"""
        return self._members

    def getSize(self):
        """Return the current size of the pack"""
        return len(self._members)

    def getMaxSize(self):
        """Return the max size of the pack"""
        return 3

    def updatePack(self):
        """Removes dead pack members and updates the leader accordingly"""
        self._members = [x if x!=None and not x.isDead() else None for x in self._members]
        if self._leader.isDead():
            for i,animal in enumerate(self):
                if animal != None and i <= len(self)-1:
                    self.resetLeader(self._members[i])
                    break

    def isDead(self):
        return all(v is None for v in self)

    def hasAttacked(self):
        if self._nextToAttackIndex % 3 == 2:
            self._nextToAttackIndex = 0
        else:
            self._nextToAttackIndex += 1
##        if self[self._nextToAttackIndex] == None and not self.isDead():
##            self.hasAttacked()
        self._nextToAttack = self[self._nextToAttackIndex]

    def __repr__(self):
        """Representation of the pack class"""
        return str([x.getName() if x != None else None for x in self._members])

    def __iter__(self):
        """Iterator for the pack class"""
        for member in self._members:
            yield member

    def __getitem__(self, index):
        """Allow for the indexing of a pack"""
        return self._members[index]

    def __len__(self):
        return len(self._members)

    def __contains__(self,animal):
        return animal in self._members

    def trueLen(self):
        return len([animal for animal in self._members if animal != None])

    def draw(self, screen):
        sortedMembers = [x for x in self._members if x != None]
        sortedMembers.sort(key= lambda x: x._position.y + x.getHeight()) 
        for animal in sortedMembers:
            animal.draw(screen)

    def update(self, worldsize, ticks):
        if type(self.getLeader()) == Player:
            flank = 1
            for animal in self._members:
                if animal != None and not self.isLeader(animal):
                    animal.followPlayer(ticks, self.getLeader(), flank)
                    flank += 1
        else:
            flank = 1
            for animal in self._members:
                if animal != None and not self.isLeader(animal):
                    animal.follow(ticks, self.getLeader())
                    flank += 1

            
