
from polybius.managers import CONSTANTS
from minigame.itemblock import ItemBlock
from minigame.inventoryhud import InventoryHUD

class InventoryGUI():

    def __init__(self):

        screen_size = CONSTANTS.get("screen_size")
        self._player = CONSTANTS.get("player")

        # Create the inventory hud
        pos_x = (screen_size[0]//2)-350
        pos_y = screen_size[1]-52
        self._invHud = self._hud = InventoryHUD((pos_x,pos_y), (700,50))

        # Create item blocks for equipped items
        self._weapon = ItemBlock((screen_size[0]-164,5))
        self._armor = ItemBlock((screen_size[0]-82,5))

    def getInHand(self):
        return self._weapon.getItem()

    def getArmor(self):
        return self._armor.getItem()

    def getActiveHUDItem(self):
        return self._invHud.getActiveItem()

    def draw(self, screen):
        self._invHud.draw(screen)
        self._armor.draw(screen)
        self._weapon.draw(screen)

    def handleEvent(self, event):
        self._invHud.handleEvent(event)

    def update(self, ticks):
        self._invHud.update(ticks)
        self._armor.setItem(self._player.getArmor())
        self._weapon.setItem(self._player.getEquipItem())
