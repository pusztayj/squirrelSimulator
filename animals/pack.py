"""
@authors: Trevor Stalnaker, Justin Pusztay
File: pack.py

A class that models a pack of animals. A pack is a group of three
animals. In this class we create an object that can hold three
animal type objects. Here we update packs checking if animals are dead
set leaders of packs. We can also add and remove anmials from packs.
"""

from player import Player
from inventory import Inventory

class Pack():

    def __init__(self, leader, name=""):
        """
        Initialize the pack with a leader and with a name for the pack.
        """
        self._maxSize = 3 # the default max size is 3
        self._members = [leader, None, None]
        self._leader = leader
        self._name = name
        self._nextToAttackIndex = 0 # sets the next to attack to 0
        self._nextToAttack = self[self._nextToAttackIndex]
        self._resourcePool = Inventory() # shared resources for the pack

    def updateResourcePool(self,member):
        """
        Will add sharable items to the resource pool.
        """
        return 0

    def getNextToAttack(self):
        """
        This method is very useful for the combat turn order, where the
        next animal from a pack to attack is returned. 
        """
        if self._nextToAttack != None and self._nextToAttack.isDead():
            return None
        else:
            return self._nextToAttack

    def getNextToAttackIndex(self):
        """
        Returns the index of the next animal in the pack that needs to attack.
        """
        return self._nextToAttackIndex

    def getPackName(self):
        """
        Returns the name of the pack.
        """
        return self._name

    def setPackName(self, name):
        """
        Sets of the name of the pack. 
        """
        self._name = name

    def getLeader(self):
        """Return the leader of the pack"""
        return self._leader

    def isLeader(self,animal):
        """
        Returns a boolean if the animal is the leader of the pack.
        """
        return animal == self._leader

    def resetLeader(self, newLeader):
        """Reset the leader of the pack."""
        self._leader = newLeader

    def addMember(self, member):
        """
        Add a new member to the pack if there is room to add an animal.
        """
        if None not in self._members: # checks if there is room
            pass
        for i,animal in enumerate(self): # Adds the animal to the pack
            if animal == None:
                self._members[i] = member
##                member.setPack(self)
                break

    def removeMember(self, member):
        """Remove a current member of the pack"""
        self._members = [None if m==member else m for m in self._members]

    def getMembers(self):
        """Returns the members of the pack"""
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
        """
        Returns a boolean if all the animals are dead in the pack.
        """
        return all(v is None for v in self)

    def hasAttacked(self):
        """
        Updates the get next to attack index and then sets the next animal
        to attack.
        """
        if self._nextToAttackIndex % 3 == 2:
            self._nextToAttackIndex = 0
        else:
            self._nextToAttackIndex += 1
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
        """
        Returns the length of the pack.
        """
        return len(self._members)

    def __contains__(self,animal):
        """
        Returns a boolean if an animal is in the pack.
        """
        return animal in self._members

    def trueLen(self):
        """
        Returns the number of elements in a pack that are not None.
        """
        return len([animal for animal in self._members if animal != None])

    def draw(self, screen):
        """
        Calls the draw method on every method in the pack. In the order that
        generates the best layering based on the y-positions. 
        """
        sortedMembers = [x for x in self._members if x != None]
        sortedMembers.sort(key= lambda x: x._position.y + x.getHeight()) 
        for animal in sortedMembers:
            animal.draw(screen)

    def update(self, worldsize, ticks):
        """
        Handles the updates for each animal in the pack that is not the leader
        and calls the respective follow player. 
        """
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

            
