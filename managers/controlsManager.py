from .abstractManager import AbstractManager
import pygame, random,pprint
from event import EventWrapper

class ControlsManager():

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
            self._temp = {}
            AbstractManager.__init__(self,"default_controls.csv",self._temp)

            self._controls = {}
            for action, control in self._temp.items():
                t = eval("pygame." + control["event_type"])
                if t == pygame.MOUSEBUTTONDOWN:
                    key = control["event_key"]
                else:
                    key = eval("pygame." + control["event_key"])
                mods = control["event_mods"].split(",")
                mods = [eval("pygame." + mod) for mod in mods if mod !=""]
                self._controls[action] = EventWrapper(t, key, mods)

        def get(self, action):
            """Return all available names"""
            return self._controls[action]

CONTROLS = ControlsManager.getInstance()
