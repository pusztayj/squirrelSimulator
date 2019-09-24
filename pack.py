"""
Author: Trevor Stalnaker
File: pack.py

A class that models a pack or clan of animals
"""
class Pack():

    def __init__(self, leader, size=3):
        """Initialize the pack with a leader and a max size"""
        self._maxSize = size
        self._members = [leader]
        self._leader = leader

    def getLeader(self):
        """Return the leader of the pack"""
        return self._leader

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
            self._members.remove(member)

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
        self._members = [m for m in self._members if not m.isDead()]
        if self._leader.isDead():
            if self.getSize > 0:
                self._resetLeader(self._members[0])

    def __repr__(self):
        """Representation of the pack class"""
        return str([m.getName() for m in self._members])

    def __iter__(self):
        """Iterator for the pack class"""
        for member in self._members:
            yield member
                
            
