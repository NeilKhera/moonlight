#! /usr/bin/env python3

import math
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

def inBounds(row, col):
  if row >= dem_data[0].shape[0] or col >= dem_data[0].shape[1]:
    return False
  if row < 0 or col < 0:
    return False

  return True

def lineWalk(row, col):
  r = row
  c = col

  dr = sun_direction[0]
  dc = sun_direction[1]

  while (inBounds(r, c)):
    yield (int(r), int(c))
    r = r + dr
    c = c + dc

def moonlight(dem_data, sun_position):
  tan_incl = math.tan(sun_position[1] * math.pi / 180.0)
  lightmap = np.zeros(dem_data[0].shape)

  for row in range(lightmap.shape[0]):
    for col in range(lightmap.shape[1]):
      start_point = (row, col)

      if (lightmap[row, col] != -50 and lightmap[row, col] != -10):
        for xy in lineWalk(row, col):
          horizontal_displacement = math.sqrt((xy[0] - start_point[0]) ** 2 + (xy[1] - start_point[1]) ** 2) * dem_data[1]
          vertical_displacement = dem_data[0][xy[0], xy[1]] - dem_data[0][start_point[0], start_point[1]]

          if vertical_displacement > (tan_incl * horizontal_displacement):
            while len(line_stack) != 0:
              coords = line_stack.pop()
              lightmap[coords[0], coords[1]] = -50

            start_point = xy

          line_stack.append(xy)

        lightmap[start_point[0], start_point[1]] = -10
        line_stack.clear()

  return lightmap

if __name__ == "__main__":
  dem_heightmap = np.array(Image.open('moon.png'), dtype='float32')
  dem_scale = 5
  dem_data = (dem_heightmap, dem_scale)

  sun_direction = (0.866, -0.5)
  sun_inclination = 15
  sun_position = (sun_direction, sun_inclination)

  line_stack = []

  lightmap = moonlight(dem_data, sun_position)
  plt.imshow(lightmap)
  plt.show()
