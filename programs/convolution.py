# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 14:28:11 2022

@author: Eric Tellez
This program is to convolute the data of the radar to see the edges of the plume
"""

import wradlib
import numpy
import matplotlib.pyplot as pl
from osgeo import osr
import glob
import os.path
import warnings
warnings.filterwarnings('ignore')

# define your cartesian reference system
# For Mexico City: https://epsg.io/?q=Mexico
proj = osr.SpatialReference()
proj.ImportFromEPSG(6371)


#filename = wradlib.util.get_wradlib_data_file('radar_data_examples/Explosiones/20210915_044742/ODIM_H5/0087_20210915_045031.h5')
#filename = wradlib.util.get_wradlib_data_file('radar_data_examples/Explosiones/20200722_151800/0087_20200722_151500.h5')
filename = wradlib.util.get_wradlib_data_file('D:/ODIM_H5/0087_20221006/0087_20221006_030000.h5')
raw = wradlib.io.read_opera_hdf5(filename)

#dataset# is angle
#data# is phsyical variable   
data = raw["dataset5/data2/what"]["offset"] +(raw["dataset5/data2/what"]["gain"])*raw["dataset5/data2/data"]

kernel=numpy.array([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]])  
dataconvolved=numpy.convolve(data,kernel, 'same')
   
#elevation angle (very important)
elangle = raw['dataset1/where']['elangle'] #to obtain the elevation angle
azimuth = raw['dataset1/how']['startazA'][132:157] #to obtain all the azimuth angles
rscale = raw['dataset1/where']['rscale'] #to obtain the conversion factor of the distance
    
#date and time is almost the same as the name of the archive
dateGMT = raw['what']['startdate']
timeGMT = raw['what']['starttime']
    
#Coordinates
sitecoords = (raw["where"]["lon"], 
              raw["where"]["lat"],
              raw["where"]["height"])

    
#plot the horizontal reflectivity
fig2 = pl.figure(figsize=(10, 10))

#to plot all the data you use 
#ax, im = wradlib.vis.plot_ppi(data,

#To plot only the 30 degree angle and 15km range that corresponds to the volcano you use
#ax, im = wradlib.vis.plot_ppi(data[132:157,0:200]

ax, im = wradlib.vis.plot_ppi(dataconvolved[132:157,0:200], #The first coordinate is angle and the second is radius
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
#To plot the exact point over the crater with a dotted white line
axe = wradlib.vis.plot_ppi_crosshair(site=sitecoords, 
                                     ranges=[11238],
                                     angles=[165],
                                     proj=None,
                                     elev=elangle,
                                     line=dict(color='white'),
                                     circle={'edgecolor': 'white'},
                                     )

xlabel = ax.set_xlabel('distancia [m]')
ylabel = ax.set_ylabel('distancia [m]')
title = ax.set_title('Fecha {} hora {} GMT \n DBZH [dBz],  Ángulo de elevación {}°'.format(dateGMT,timeGMT,elangle))
cb = pl.colorbar(im, ax=ax)