from .abstractManager import AbstractManager

class ItemManager():

    # The singleton instance variable
    _INSTANCE = None
   
    @classmethod
    def getInstance(cls):
        """Used to obtain the singleton instance"""
        if cls._INSTANCE == None:
            cls._INSTANCE = cls._IM()
        return cls._INSTANCE

    class _IM(AbstractManager):

        def __init__(self):
            self._items = {}
            AbstractManager.__init__(self,"items.csv",self._items)
    
        def getAttributes(self, item):
            return self._items[item]

        def getItems(self):
            return self._items.keys()

        def getItemsByType(self, t):
            return [k for k,v in self._items.items() if v["type"]==t]
          
ITEMS = ItemManager.getInstance()
