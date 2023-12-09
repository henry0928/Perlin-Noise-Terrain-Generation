from PIL import Image as pImage
import numpy as np

class imgWrapper:
    def __init__(self, initData):
        if isinstance(initData, str):
            img = pImage.open(initData)
            self.x = img.size[0]
            self.y = img.size[1]
            self.pixels_map = list(img.getdata())
            self.pixels_map = [self.pixels_map [i * self.y : (i + 1) * self.y] for i in range(self.x)]
        else:
            self.pixels_map = initData
            self.x = len(initData)
            self.y = len(initData[0])

    def getx(self):
        return self.x
    
    def gety(self):
        return self.y
    
    def getpixels_map(self):
        return self.pixels_map
    
    def getpixel(self, i, j):
        return self.pixels_map[i % self.x][j % self.y][0:3]
    
    def save_img(self, filename):
        img = pImage.fromarray(np.array(self.pixels_map, np.uint8))
        img.save(filename)
