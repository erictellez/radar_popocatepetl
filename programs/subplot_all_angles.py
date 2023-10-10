# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 01:47:51 2022

@author: Eric Tellez

subplot all the angles


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
from osgeo import osr

# define your cartesian reference system
# For Mexico City: https://epsg.io/?q=Mexico
proj = osr.SpatialReference()
proj.ImportFromEPSG(6371)


filenameclutter =wradlib.util.get_wradlib_data_file('radar_data_examples/Explosiones/20210915_044742/ODIM_H5/0087_20210915_044742.h5') 
rawclutter1 = wradlib.io.read_opera_hdf5(filenameclutter)
filenameclutter2 =wradlib.util.get_wradlib_data_file('radar_data_examples/Explosiones/20210915_044742/ODIM_H5/0087_20210915_044824.h5')
rawclutter2 = wradlib.io.read_opera_hdf5(filenameclutter2)
filenameclutter3 =wradlib.util.get_wradlib_data_file('radar_data_examples/Explosiones/20210915_044742/ODIM_H5/0087_20210915_044949.h5')
rawclutter3 = wradlib.io.read_opera_hdf5(filenameclutter3)

#to average the ground clutter
rawclutteraverage=(rawclutter1[
    "dataset5/data7/data"]+rawclutter2[
    "dataset5/data7/data"]+rawclutter3[
    "dataset5/data7/data"])/3


filename = wradlib.util.get_wradlib_data_file('radar_data_examples/Explosiones/20210915_044742/ODIM_H5/0087_20210915_045031.h5')
raw = wradlib.io.read_opera_hdf5(filename)

#RATE_rainfall_intensity=raw['dataset4/data1/data'] #This dataset is not that important
DBZH_horizontal_reflectivity=raw["dataset5/data2/what"]["offset"] +(raw[
    "dataset5/data2/what"]["gain"])*(raw["dataset5/data2/data"]-rawclutteraverage)
RHOHV_copolar_correlation_coefficient=raw["dataset5/data7/what"]["offset"] +(raw[
    "dataset5/data7/what"]["gain"])*(raw["dataset5/data7/data"]-rawclutteraverage)
#Coordinates
sitecoords = (raw["where"]["lon"], 
              raw["where"]["lat"],
              raw["where"]["height"])

azimuth = raw['dataset1/how']['startazA'] #to obtain all the azimuth angles
elangle = raw['dataset1/how']['elangles']
rscale= raw['dataset1/where']['rscale']

#plot the horizontal reflectivity at first angle
fig1= pl.figure(figsize=(10, 10))
ax, im = wradlib.vis.plot_ppi(DBZH_horizontal_reflectivity[:,0:200], #The first coordinate is angle and the second is radius
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
title = ax.set_title('DBZH [dBz]')
cb = pl.colorbar(im, ax=ax)


"""
#plot the horizontal reflectivity
fig2= pl.figure(figsize=(10, 10))
ax, im = wradlib.vis.plot_ppi(DBZH_horizontal_reflectivity[:,0:200], #The first coordinate is angle and the second is radius
                                #reflectivity,
                                rf= 1/rscale,
                                az= azimuth,
                                elev= elangle,
                                fig= fig2,
                                site= sitecoords,
                                #proj='cg', #Another type of projection
                                proj= proj, #Plot
                                ax=111,
                                func='pcolormesh')
xlabel = ax.set_xlabel('distancia [m]')
ylabel = ax.set_ylabel('distancia [m]')
title = ax.set_title('DBZH [dBz]')
cb = pl.colorbar(im, ax=ax)

#plot the horizontal reflectivity
fig2= pl.figure(figsize=(10, 10))
ax, im = wradlib.vis.plot_ppi(DBZH_horizontal_reflectivity[:,0:200], #The first coordinate is angle and the second is radius
                                #reflectivity,
                                rf= 1/rscale,
                                az= azimuth,
                                elev= elangle,
                                fig= fig2,
                                site= sitecoords,
                                #proj='cg', #Another type of projection
                                proj= proj, #Plot
                                ax=111,
                                func='pcolormesh')
xlabel = ax.set_xlabel('distancia [m]')
ylabel = ax.set_ylabel('distancia [m]')
title = ax.set_title('DBZH [dBz]')
cb = pl.colorbar(im, ax=ax)

#plot the horizontal reflectivity
fig2= pl.figure(figsize=(10, 10))
ax, im = wradlib.vis.plot_ppi(DBZH_horizontal_reflectivity[:,0:200], #The first coordinate is angle and the second is radius
                                #reflectivity,
                                rf= 1/rscale,
                                az= azimuth,
                                elev= elangle,
                                fig= fig2,
                                site= sitecoords,
                                #proj='cg', #Another type of projection
                                proj= proj, #Plot
                                ax=111,
                                func='pcolormesh')
xlabel = ax.set_xlabel('distancia [m]')
ylabel = ax.set_ylabel('distancia [m]')
title = ax.set_title('DBZH [dBz]')
cb = pl.colorbar(im, ax=ax)

#plot the horizontal reflectivity
fig2= pl.figure(figsize=(10, 10))
ax, im = wradlib.vis.plot_ppi(DBZH_horizontal_reflectivity[:,0:200], #The first coordinate is angle and the second is radius
                                #reflectivity,
                                rf= 1/rscale,
                                az= azimuth,
                                elev= elangle,
                                fig= fig2,
                                site= sitecoords,
                                #proj='cg', #Another type of projection
                                proj= proj, #Plot
                                ax=111,
                                func='pcolormesh')
xlabel = ax.set_xlabel('distancia [m]')
ylabel = ax.set_ylabel('distancia [m]')
title = ax.set_title('DBZH [dBz]')
cb = pl.colorbar(im, ax=ax)
"""

#plot the horizontal reflectivity
fig2= pl.figure(figsize=(10, 10))
ax, im = wradlib.vis.plot_ppi(RHOHV_copolar_correlation_coefficient[:,0:200], #The first coordinate is angle and the second is radius
                                #reflectivity,
                                rf= 1/rscale,
                                az= azimuth,
                                elev= elangle,
                                fig= fig2,
                                site= sitecoords,
                                #proj='cg', #Another type of projection
                                proj= proj, #Plot
                                ax=111,
                                func='pcolormesh')

xlabel = ax.set_xlabel('distancia [m]')
ylabel = ax.set_ylabel('distancia [m]')
title = ax.set_title('RHOHV')
cb = pl.colorbar(im, ax=ax)
"""
#plot the horizontal reflectivity
fig2= pl.figure(figsize=(10, 10))
ax, im = wradlib.vis.plot_ppi(DBZH_horizontal_reflectivity[:,0:200], #The first coordinate is angle and the second is radius
                                #reflectivity,
                                rf= 1/rscale,
                                az= azimuth,
                                elev= elangle,
                                fig= fig2,
                                site= sitecoords,
                                #proj='cg', #Another type of projection
                                proj= proj, #Plot
                                ax=111,
                                func='pcolormesh')
xlabel = ax.set_xlabel('distancia [m]')
ylabel = ax.set_ylabel('distancia [m]')
title = ax.set_title('DBZH [dBz]')
cb = pl.colorbar(im, ax=ax)

"""