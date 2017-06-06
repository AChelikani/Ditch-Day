from PIL import Image
from numpy import std
import math

BLACK_THRESHOLD = (1, 1, 1) # Threshold for R, G, B relative to black (0, 0, 0)
CENTER_LENGTH_THRESHOLD = 1

class CircleAnalyzer(object):
    def __init__(self, filename):
        self.im = Image.open(filename)
        self.pix = self.im.load()
        self.x, self.y = self.im.size
        self.darkPixels = []

    def storeDarkPixels(self):
        for x in range(self.x):
            for y in range(self.y):
                pix = self.pix[x, y]
                resPix = tuple(a - b for a,b in zip(pix, BLACK_THRESHOLD))
                if (all(cVal <= 0 for cVal in resPix)):
                    self.darkPixels.append((x, y))
        print "All dark pixels stored.\n"
        return len(self.darkPixels)

    def findCenter(self):
        # Average all x coordinates and y coordinates
        centerX = centerY = 0.0
        for pixel in self.darkPixels:
            centerX += pixel[0]
            centerY += pixel[1]
        centerX /= len(self.darkPixels)
        centerY /= len(self.darkPixels)
        print "Center found.\n"
        print "x-coord: %0.2f, y-coord: %0.2f\n" %(centerX, centerY)
        return (centerX, centerY)

    def __distance(self, p1, p2):
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    def computeScore(self, c):
        lengths = []
        for pixel in self.darkPixels:
            dist = self.__distance(c, pixel)
            if (dist > CENTER_LENGTH_THRESHOLD):
                lengths.append(dist)
        return std(lengths)

    def analyze(self):
        self.storeDarkPixels()
        center = self.findCenter()
        result = self.computeScore(center)
        print "Done analyzing...\n"
        print "Score is: %0.2f" %result


if __name__ == "__main__":
    ca = CircleAnalyzer("circle.jpg")
    ca.analyze()
