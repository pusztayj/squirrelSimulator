from .abstractManager import AbstractManager

class UIManager():

    # The singleton instance variable
    _INSTANCE = None
   
    @classmethod
    def getInstance(cls):
        """Used to obtain the singleton instance"""
        if cls._INSTANCE == None:
            cls._INSTANCE = cls._UIM()
        return cls._INSTANCE

    class _UIM(AbstractManager):

        def __init__(self):
            self._menuButtons = {}
            AbstractManager.__init__(self,"menuButtons.csv",self._menuButtons,toLyst=[0])
    
        def getControlsForMenu(self, menu):
            return self._menuButtons[menu]

USER_INTERFACE = UIManager.getInstance()
