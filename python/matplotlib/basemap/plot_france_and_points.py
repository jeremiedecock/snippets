#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Plot coast lines, countries, states and given points.

Refs: "Python for Data Analysis" by Wes McKinney, ed. O'Reilly, 2013 (p.261)

Install: basemap is not included in Matplotlib. To install it with conda: conda install basemap

Warning:

    "Starting in 2016, Basemap came under new management. The Cartopy project
    will replace Basemap, but it hasn’t yet implemented all of Basemap’s
    features. All new software development should try to use Cartopy whenever
    possible, and existing software should start the process of switching over
    to use Cartopy. All maintenance and development efforts should be focused
    on Cartopy." (http://matplotlib.org/basemap/users/intro.html)

"""

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

lllat = 41.0 # latitude of lower left hand corner of the desired map domain (degrees).
urlat = 52.0 # latitude of upper right hand corner of the desired map domain (degrees).

lllon = -5.0 # longitude of lower left hand corner of the desired map domain (degrees).
urlon =  9.5 # longitude of upper right hand corner of the desired map domain (degrees).

m = Basemap(ax=ax,
            projection='stere',
            lon_0=(urlon+lllon)/2.,
            lat_0=(urlat+lllat)/2.,
            llcrnrlat=lllat,
            urcrnrlat=urlat,
            llcrnrlon=lllon,
            urcrnrlon=urlon,
            resolution='l')    # Can be ``c`` (crude), ``l`` (low), ``i`` (intermediate), ``h`` (high), ``f`` (full) or None.

m.drawcoastlines()
m.drawstates()
m.drawcountries()
#m.drawrivers()
#m.drawcounties()

# Eiffel tower's coordinates
pt_lat = 48.858223
pt_lon = 2.2921653

x, y = m(pt_lon, pt_lat)

print(pt_lat, pt_lon)
print(x, y)

m.plot(x, y, 'ro')

# Save file #################

plt.savefig("plot_france_and_points.png")

# Plot ######################

plt.show()
