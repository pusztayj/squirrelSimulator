from polybius.managers.abstractManager import AbstractManager
import random

class NameManager():

    # The singleton instance variable
    _INSTANCE = None
   
    @classmethod
    def getInstance(cls):
        """Used to obtain the singleton instance"""
        if cls._INSTANCE == None:
            cls._INSTANCE = cls._NM()
        return cls._INSTANCE

    class _NM(AbstractManager):

        def __init__(self):
            self._names = {}
            
        def setResourcePath(self, path):
            AbstractManager.__init__(self,path,self._names,False)

        def getNames(self):
            """Return all available names"""
            return list(self._names.keys())

        def getNamesByType(self, t):
            """Return only names of a given type"""
            return [k for k,v in self._names.items() if v["type"]==t]

        def getRandomName(self, t="all"):
            if t == "all":
                return random.choice(self.getNames())
            else:
                return random.choice(self.getNamesByType(t))

NAMES = NameManager.getInstance()
