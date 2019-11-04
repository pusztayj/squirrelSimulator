
from modules.drawable import Drawable 

class TradeDesk(Drawable):

    def __init__(self,pos=(450,100)):
        Drawable.__init__(self, "tradeDesk.png", pos, worldBound=False)
