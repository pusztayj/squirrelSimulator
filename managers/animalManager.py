from .abstractManager import AbstractManager

class AnimalManager():

    # The singleton instance variable
    _INSTANCE = None
   
    @classmethod
    def getInstance(cls):
        """Used to obtain the singleton instance"""
        if cls._INSTANCE == None:
            cls._INSTANCE = cls._AM()
        return cls._INSTANCE

    class _AM(AbstractManager):

        def __init__(self):
            self._animals = {}
            AbstractManager.__init__(self,"animals.csv",self._animals)
                            
        def getStats(self, animal):
            return self._animals[animal]

        def getSpawnableAnimals(self):
            return [k for k,v in self._animals.items() if v["spawnable"]]

        def getMerchantRaces(self):
            return [k for k,v in self._animals.items() if v["merchant"]]

ANIMALS = AnimalManager.getInstance()
