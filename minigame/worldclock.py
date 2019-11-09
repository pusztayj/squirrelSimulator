
import pygame
from modules.drawable import Drawable
from graphics.textbox import TextBox

class WorldClock(Drawable):

    def __init__(self, screenWidth, hourLength=5, seasonLength=20):
        

        self._width = 200
        self._height = 200

        position = ((screenWidth//2)-(self._width//2),5)

        super().__init__("", position, worldBound=False)

        # Save fonts for the clock
        self._large_font = pygame.font.SysFont("Times New Roman", 32)
        self._small_font = pygame.font.SysFont("Times New Roman", 20)

        self._seasons = ["Spring", "Summer", "Fall", "Winter"]

        self._time = 0

        # Establish lengths for measure
        self._hour_length = hourLength # ticks / seconds
        self._day_length = 24 * self._hour_length
        self._minute_length = self._hour_length / 60
        self._season_length = seasonLength #days
        self._year_length = self._season_length * 4

        self._current_season = 0

        # Create Text Boxes
        self._txtDay = TextBox("", (0,0), self._small_font, (255,255,255))
        self._txtHour = TextBox("", (0,0), self._large_font, (255,255,255))
        self._txtSeason = TextBox("", (0,0), self._small_font, (255,255,255))

        self.update()

    def getHourLength(self):
        return self._hour_length

    def getSeason(self):
        return self._current_season

    def getTime(self):
        return self._time

    def update(self, ticks=0):
        self._time += ticks
        surf = pygame.Surface((self._width, self._height))
        surf.fill((0,0,0,255))
        self._txtDay.setText("Day: " + str(int(self._time // self._day_length)+1))
        self._txtDay.setPosition((((self._width // 2)-(self._txtDay.getWidth()//2)),5))
        self._txtHour.setText(str(int((self._time // self._hour_length) % 12)+1) + ":" +
                      str(int(self._time // self._minute_length)%60).zfill(2) + " " +
                      ("pm" if (int((self._time // self._hour_length) % 24)+1 >= 12) else "am"))
        self._txtHour.setPosition((((self._width // 2)-(self._txtHour.getWidth()//2)),25))
        self._current_season = int((((self._time // self._day_length) + 1) // self._season_length) % 4)
        self._txtSeason.setText(self._seasons[self._current_season])
        self._txtSeason.setPosition((((self._width // 2)-(self._txtSeason.getWidth()//2)),60))

        self._txtDay.draw(surf)
        self._txtHour.draw(surf)
        self._txtSeason.draw(surf)

        surf.set_colorkey(surf.get_at((0,0)))

        self._image = surf
