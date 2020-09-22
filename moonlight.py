#! /usr/bin/env python3

import math
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
dem = Image.open('moon.png')
heightmap = np.array(dem, dtype='int16')
heightmap = np.array(heightmap / 2, dtype='float32')
lightmap = np.zeros(heightmap.shape)
scale = 5

direction = (-0.985, -0.174)
inclination = 15

line_stack = []

def inBounds(row, col):
  if row >= heightmap.shape[0] or col >= heightmap.shape[1]:
    return False
  if row < 0 or col < 0:
    return False

  return True

def lineWalk(row, col):
  r = row
  c = col

  dr = direction[0]
  dc = direction[1]

  while (inBounds(r, c)):
    yield (int(r), int(c))
    r = r + dr
    c = c + dc

def clearStack():
  while len(line_stack) != 0:
    coords = line_stack.pop()
    lightmap[coords[0], coords[1]] = -50

def sunlit():
  tan_incl = math.tan(inclination * math.pi / 180.0)

  for row in range(heightmap.shape[0]):
    for col in range(heightmap.shape[1]):
      start_point = (row, col)

      if (lightmap[row, col] != -50 and lightmap[row, col] != -10):
        for xy in lineWalk(row, col):
          horizontal_displacement = math.sqrt((xy[0] - start_point[0]) ** 2 + (xy[1] - start_point[1]) ** 2) * scale
          vertical_displacement = heightmap[xy[0], xy[1]] - heightmap[start_point[0], start_point[1]]

          if vertical_displacement > (tan_incl * horizontal_displacement):
            clearStack()
            start_point = xy

          line_stack.append(xy)

        lightmap[start_point[0], start_point[1]] = -10
        line_stack.clear()

if __name__ == "__main__":
  plt.imshow(heightmap)
  plt.show()
  sunlit()
  plt.imshow(lightmap)
  plt.show()
