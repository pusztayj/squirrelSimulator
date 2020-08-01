"""
@author: Justin Pusztay

In this file we create a class that holds the trade desk image that appears
in the merchant minigame GUI.
"""

from polybius.graphics import Drawable 

class TradeDesk(Drawable):

    def __init__(self,pos=(450,100)):
        """Sets up the trade desk image."""
        Drawable.__init__(self, "tradeDesk.png", pos, worldBound=False)
