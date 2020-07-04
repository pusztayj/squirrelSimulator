"""
A Singleton Sound Manager class
Author: Liz Matthews, 9/20/2019
Edited by: Trevor Stalnaker

Provides on-demand loading of sounds for a pygame program.

"""

from pygame import image, Surface, Rect
from .abstractManager import AbstractManager
import os


class FrameManager():
   """A singleton factory class to create and store frames on demand."""
   
   # The singleton instance variable
   _INSTANCE = None
   
   @classmethod
   def getInstance(cls):
      """Used to obtain the singleton instance"""
      if cls._INSTANCE == None:
         cls._INSTANCE = cls._FM()
      
      return cls._INSTANCE
   
   # Do not directly instantiate this class!
   class _FM(AbstractManager):
      """An internal FrameManager class to contain the actual code. Is a private class."""
      
      # Folder in which images are stored
      _IMAGE_FOLDER = os.path.join("resources","images")
      
      def __init__(self):
         self._surfaces = {}
         self._images = {}
         AbstractManager.__init__(self, "images.csv", self._images, lower=False)
        
      def __getitem__(self, key):
         return self._surfaces[key]
   
      def __setitem__(self, key, item):
         self._surfaces[key] = item
      
      def getFrame(self, fileName, offset=None):
         # If this frame has not already been loaded, load the image from memory
         if fileName not in self._surfaces.keys():
            self._loadImage(fileName, offset != None)
         
         # If this is an image sheet, return the correctly offset sub surface
         if offset != None:
            return self[fileName][offset[1]][offset[0]]
         
         # Otherwise, return the sheet created
         return self[fileName]
      
      def _loadImage(self, fileName, sheet=False):
         # Load the full image
         fullImage = image.load(os.path.join(FrameManager._FM._IMAGE_FOLDER, fileName))
         
         colorKey = self._images[fileName]["color_key"]
         fullImage = fullImage.convert()
         
         # If the image to be loaded is an image sheet, split it up based on the frame size
         if sheet:
               
            self[fileName] = []
            spriteSize = self._images[fileName]["frame_dimensions"]
            
            sheetDimensions = fullImage.get_size()
            
            for y in range(0, sheetDimensions[1], spriteSize[1]):
               self[fileName].append([])
               for x in range(0, sheetDimensions[0], spriteSize[0]):
                  
                  frame = Surface(spriteSize)    
                  frame.blit(fullImage, (0,0), Rect((x,y), spriteSize))
                  
                  # If we need to set the color key
                  if colorKey:
                     frame.set_colorkey(frame.get_at((0,0)))
                  
                  self[fileName][-1].append(frame)
         else:
            
            self[fileName] = fullImage
               
            # If we need to set the color key
            if colorKey:
               self[fileName].set_colorkey(self[fileName].get_at((0,0)))
               
            
         
         
# Set up an instance for others to import         
FRAMES = FrameManager.getInstance()
