from .abstractManager import AbstractManager

class ConstantManager():

    # The singleton instance variable
    _INSTANCE = None
   
    @classmethod
    def getInstance(cls):
        """Used to obtain the singleton instance"""
        if cls._INSTANCE == None:
            cls._INSTANCE = cls._CM()
        return cls._INSTANCE

    class _CM(AbstractManager):

        def __init__(self):
            self._constants = {}

        def setResourcePath(self, path):
            AbstractManager.__init__(self,path,
                                     self._constants, lower=False,
                                     ignoreFields=["description"])
    
        def get(self, constant):
            return self._constants[constant]["value"]

CONSTANTS = ConstantManager.getInstance()
