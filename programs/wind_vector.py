# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 20:16:44 2022

@author: Eric Tellez

This software is to plot the wind and its standard deviation in vectorial form


This software is based upon work supported by the Ministry of Education, 
Science, Technology and Innovation of Mexico City under agreement SECITI/90/2017.


MIT License

Copyright (c) 2021 Eric Tellez

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

#I have to define this program as a function
#def plot_ppi_angle

import wradlib
import matplotlib.pyplot as pl
import numpy
from osgeo import osr

# define your cartesian reference system
# For Mexico City: https://epsg.io/?q=Mexico
proj = osr.SpatialReference()
proj.ImportFromEPSG(6371)


filename = wradlib.util.get_wradlib_data_file('radar_data_examples/Explosiones/20210915_044742/ODIM_H5/0087_20210915_045031.h5')
raw = wradlib.io.read_opera_hdf5(filename)

VRAD_radial_velocity=raw["dataset4/data3/what"]["offset"] +(raw["dataset4/data3/what"]["gain"])*raw["dataset4/data3/data"]
WRAD_doppler_velocity_spectrum_width=raw["dataset4/data8/what"]["offset"] +(raw["dataset4/data8/what"]["gain"])*raw["dataset4/data8/data"]

#Coordinates
sitecoords = (raw["where"]["lon"], 
              raw["where"]["lat"],
              raw["where"]["height"])

azimuth = raw['dataset1/how']['startazA'] #to obtain all the azimuth angles
elangle = raw['dataset1/how']['elangles']
rscale= raw['dataset1/where']['rscale']
"""
#plot the radial velocity of the wind
fig1= pl.figure(figsize=(10, 10))
ax, im = wradlib.vis.plot_ppi(VRAD_radial_velocity[:,0:200], #The first coordinate is angle and the second is radius
                          #reflectivity,
                          rf= 1/rscale,
                          az= azimuth,
                          elev= elangle,
                          fig= fig1,
                          site= sitecoords,
                          #proj='cg', #Another type of projection
                          proj= proj, #Plot
                          ax=111,
                          func='pcolormesh')
xlabel = ax.set_xlabel('distancia [m]')
ylabel = ax.set_ylabel('distancia [m]')
title = ax.set_title('VRAD [m/s]')
cb = pl.colorbar(im, ax=ax)
"""
fig2=pl.figure(figsize=(10,10))
ax=fig2.add_subplot(111, projection='polar')
pl.quiver(VRAD_radial_velocity[:,0:200],VRAD_radial_velocity[:,0:200],numpy.cos(VRAD_radial_velocity[:,0:200]),numpy.sin(VRAD_radial_velocity[:,0:200]))

theta=(numpy.pi)/6
ax.plot(theta, 200)
pl.show()
"""
#Plot the standard deviation of the wind velocity
fig8= pl.figure(figsize=(10, 10))
ax, im = wradlib.vis.plot_ppi(WRAD_doppler_velocity_spectrum_width[:,0:200], #The first coordinate is angle and the second is radius
                          #reflectivity,
                          rf= 1/rscale,
                          az= azimuth,
                          elev= elangle,
                          fig= fig8,
                          site= sitecoords,
                          #proj='cg', #Another type of projection
                          proj= proj, #Plot
                          ax=111,
                          func='pcolormesh')
xlabel = ax.set_xlabel('distancia [m]')
ylabel = ax.set_ylabel('distancia [m]')
title = ax.set_title('WRAD [m/s]')
cb = pl.colorbar(im, ax=ax)
"""
