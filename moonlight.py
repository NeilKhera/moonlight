#! /usr/bin/env python3

import math
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
heightmap = np.array(Image.open('small_dem.tif'), dtype='uint16')
scale = 1

line_stack = []

def inBounds(row, col):
  if row >= heightmap.shape[0] or col >= heightmap.shape[1]:
    return False
  if row < 0 or col < 0:
    return False

  return True

def lineWalk(direction, row, col):
  r = row
  c = col

  dx = direction[0]
  dy = direction[1]

  while (inBounds(r, c)):
    yield (int(r), int(c))
    r = r + dx
    c = c + dy

def clearStack(val):
  while len(line_stack) != 0:
    coords = line_stack.pop()
    heightmap[coords[0], coords[1]] = val

def sunlit(direction, inclination):
  tan_incl = math.tan(inclination * math.pi / 180.0)

  for row in range(heightmap.shape[0]):
    for col in range(heightmap.shape[1]):
      start_point = (row, col)

      if (heightmap[row, col] != 0 and heightmap[row, col] != 1):
        for xy in lineWalk(direction, row, col):
          horizontal_displacement = math.sqrt((xy[0] - start_point[0])**2 + (xy[1] - start_point[1])**2) * scale
          vertical_displacement = heightmap[xy[0], xy[1]] - heightmap[start_point[0], start_point[1]]
          
          if vertical_displacement > (tan_incl * horizontal_displacement):
            clearStack(0)
            start_point = xy

          line_stack.append(xy)

        clearStack(1)

if __name__ == "__main__":
  direction = (1, 0)
  inclination = 20

  sunlit(direction, inclination)
  plt.imshow(heightmap)
  plt.show()

  from mayavi import mlab
  mlab.surf(heightmap / 10)
  mlab.show()
