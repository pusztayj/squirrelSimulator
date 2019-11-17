"""
Author: Trevor Stalnaker
File: pack.py

A class that models a pack or clan of animals
"""
class Pack():

    def __init__(self, leader, name=""):
        """Initialize the pack with a leader and a max size"""
        self._maxSize = 3
        self._members = [leader]
        self._leader = leader
        self._name = name

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
        if self.getSize() < self.getMaxSize():
            self._members.append(member)

    def removeMemeber(self, member):
        """Remove a current member of the pack"""
        if member in self._members:
            self._members.replace(member,None)

    def getMembers(self):
        """Return the members of the pack"""
        return self._members

    def getSize(self):
        """Return the current size of the pack"""
        return len(self._members)

    def getMaxSize(self):
        """Return the max size of the pack"""
        return self._maxSize

    def updatePack(self):
        """Removes dead pack members and updates the leader accordingly"""
        self._members = [x if not x.isDead() else None for x in self._members]
        #self._members = [m for m in self._members if not m.isDead()]
        if self._leader.isDead():
            if self.getSize() > 0:
                self.resetLeader(self._members[0])

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
                
            
