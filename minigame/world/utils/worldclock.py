"""
Author: Trevor Stalnaker
File: worldclock.py

A class that maintains and displays the in-game clock
"""

import pygame
from polybius.graphics import Drawable, TextBox
from polybius.managers import CONSTANTS

class WorldClock(Drawable):

    def __init__(self, hourLength=5, seasonLength=20):
        """Initializes the world clock"""

        self._width = 225
        self._height = 25

        screenWidth = CONSTANTS.get("screen_size")[0]

        position = ((screenWidth//2)-(self._width//2),5)

        super().__init__("", position, worldBound=False)

        # Save fonts for the clock
        self._large_font = pygame.font.SysFont("Times New Roman", 24)
        self._small_font = pygame.font.SysFont("Times New Roman", 20)

        self._seasons = ["Spring", "Summer", "Fall", "Winter"]

        self._time = 0

        # Establish lengths for measure
        self._hour_length = hourLength # ticks / seconds
        self._season_length = seasonLength #days
        self.calculateLengthsOfMeasure()

        self._current_season = 0

        # Create Text Boxes
        self._txtDay = TextBox("", (0,0), self._small_font, (255,255,255), False)
        self._txtHour = TextBox("", (0,0), self._small_font, (255,255,255), False)
        self._txtSeason = TextBox("", (0,0), self._small_font, (255,255,255), False)

        self._dayTimer = 0

        self.update()

    def calculateLengthsOfMeasure(self):
        """Calcuates the length of different periods of time
        based off of the hour length and season length"""
        self._day_length = 24 * self._hour_length
        self._minute_length = self._hour_length / 60
        self._year_length = self._season_length * 4

    def setHourLength(self, hourLen):
        self._hour_length = hourLen
        self.calculateLengthsOfMeasure()

    def setSeasonLength(self, seasonLen):
        self._season_length = seasonLen
        self.calculateLengthsOfMeasure()

    def getHourLength(self):
        """Returns the hour length"""
        return self._hour_length

    def getSeasonLength(self):
        return self._season_length

    def getDayLength(self):
        """Returns the day length"""
        return self._day_length

    def getSeason(self):
        """Returns the current season"""
        return self._current_season

    def getTime(self):
        """Returns the current time"""
        return self._time

    def setTime(self, time):
        self._time = time

    def dayPassed(self):
        """Returns true if a day has past since method was last called"""
        if self._dayTimer + self.getHourLength() >= self._day_length:
            self._dayTimer = 0
            return True
        else:
            return False

    def update(self, ticks=0):
        """Updates the world clock based on ticks from the game"""
        self._time += ticks
        self._dayTimer += ticks
        surf = pygame.Surface((self._width, self._height))
        surf.fill((0,0,0,255))
        self._txtDay.setText("Day: " + str(int((self._time + self.getHourLength()) // self._day_length)+1))
        self._txtDay.setPosition((0,0))
        self._txtHour.setText(str(int((self._time // self._hour_length) % 24)+1) + ":" +
                      str(int(self._time // self._minute_length)%60).zfill(2) + " " +
                      ("pm" if (int((self._time // self._hour_length) % 24)+1 >= 12) else "am"))
        self._txtHour.setPosition((((self._width // 2)-(self._txtHour.getWidth()//2)),0))
        self._current_season = int((((self._time // self._day_length) + 1) // self._season_length) % 4)
        self._txtSeason.setText(self._seasons[self._current_season])
        self._txtSeason.setPosition((self._width-self._txtSeason.getWidth(),0))

        self._txtDay.draw(surf)
        self._txtHour.draw(surf)
        self._txtSeason.draw(surf)

        surf.set_colorkey(surf.get_at((0,0)))

        self._image = surf
