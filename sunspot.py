#! /usr/bin/env python3
import os
from skyfield.api import PlanetaryConstants, Loader, Topos, pi, tau
import matplotlib.pyplot as plt
import numpy as np
import datetime

script_directory = os.path.dirname(__file__)
load = Loader(os.path.join(script_directory, 'data'))

def years_in_seconds(y):
    return int(y*31556926)

def hours_in_seconds(h):
    return int(h*60*60)

def wrap180(a):
    return (a + 180.0) % (2 * 180.0) - 180.0

def moon_subsolar_point(t):
    eph = load('de421.bsp')
    sun = eph['sun']
    moon = eph['moon']

    pc = PlanetaryConstants()
    pc.read_text(load('moon_080317.tf'))
    pc.read_text(load('pck00008.tpc'))
    pc.read_binary(load('moon_pa_de421_1900-2050.bpc'))
    frame = pc.build_frame_named('MOON_ME_DE421')

    place = moon + pc.build_latlon_degrees(frame, 90.0, 180.0)
    sunpos = place.at(t).observe(sun).apparent()
    lat, lon, dist = sunpos.altaz()
    return lat.degrees, wrap180(lon.degrees), dist.km

def earth_subsolar_point(t):
    eph = load('de421.bsp')
    sun = eph['sun']
    earth = eph['earth']
    place = earth + Topos(90.0, 180.0)
    sunpos = place.at(t).observe(sun).apparent()
    lat, lon, dist = sunpos.altaz()
    return lat.degrees, wrap180(-1*lon.degrees), dist.km


ts = load.timescale(builtin=False)
# Jan. 2, 2020 at 04:34:00 pm
t = ts.utc(2020, 1, 2, 16, 34, 0)

lat, lon, dist = earth_subsolar_point(t)
coords = np.vstack([lat, lon, dist]).transpose()

print("Jan 2, 2020 16:34:00...")
print("\tOn Earth, the closest point to the Sun is: ({:7.4f} W, {:7.4f} N)".format(lat, lon))

lat, lon, dist = moon_subsolar_point(t)
coords = np.vstack([lat, lon, dist]).transpose()

print("\tOn the Moon, the closest point to the Sun is: ({:7.4f} W, {:7.4f} N)".format(lat, lon))
