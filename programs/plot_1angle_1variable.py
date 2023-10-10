# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 23:47:33 2022

@author: Eric Tellez
This software is to plot all the variables at a single constant elevation angle.
The plot draws the horizontal plane of an explosion seen from above. 


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


#filename = wradlib.util.get_wradlib_data_file('radar_data_examples/Explosiones/20210915_044742/ODIM_H5/0087_20210915_045031.h5')
#filename = wradlib.util.get_wradlib_data_file('radar_data_examples/Explosiones/20200722_151800/0087_20200722_151500.h5')
filename = wradlib.util.get_wradlib_data_file('D:/ODIM_H5/0087_20221006/0087_20221006_030000.h5')
raw = wradlib.io.read_opera_hdf5(filename)

"""
#dataset# is angle
#data# is phsyical variable  
RATE_rainfall_intensity  is dataset%d/data1/
DBZH_horizontal_reflectivity is dataset%d/data2/
VRAD_radial_velocity=raw["dataset%d/data3/
ZDR_reflection_factor_difference=raw["dataset%d/data4/
KDP_propagation_phase_difference_rate_of_change=raw["dataset%d/data5/
PHIDP_differential_propagation_phase=raw["dataset%d/data6/
RHOHV_copolar_correlation_coefficient=raw["dataset%d/data7/
WRAD_doppler_velocity_spectrum_width=raw["dataset%d/data8/
#raw['dataset4/data9/data'] #I dont know what this dataset means 
"""
data = raw["dataset5/data4/what"]["offset"] +(raw["dataset5/data4/what"]["gain"])*raw["dataset5/data4/data"]
   
    
#elevation angle (very important)
elangle = raw['dataset5/where']['elangle'] #to obtain the elevation angle
azimuth = raw['dataset5/how']['startazA'][132:157] #to obtain all the azimuth angles
rscale = raw['dataset5/where']['rscale'] #to obtain the conversion factor of the distance
    
#date and time is almost the same as the name of the archive
#This data has the format byte and UTF-8 is to convert to string
dateGMT = raw['what']['startdate'].decode('UTF-8')
dateGMT = dateGMT[:4]+"-"+ dateGMT[4:]
dateGMT = dateGMT[:7]+"-"+ dateGMT[7:]
timeGMT = raw['what']['starttime'].decode('UTF-8')
timeGMT = timeGMT[:2]+":"+ timeGMT[2:]
timeGMT = timeGMT[:5]+":"+ timeGMT[5:]

date = raw['what']['Local_date'].decode('UTF-8')
date = date[:4]+"-"+ date[4:]
date = date[:7]+"-"+ date[7:]
time = raw['what']['Local_time'].decode('UTF-8')
time = time[:2]+":"+ time[2:]
time = time[:5]+":"+ time[5:]
   
#Coordinates
sitecoords = (raw["where"]["lon"], 
              raw["where"]["lat"],
              raw["where"]["height"])

    
#plot the horizontal reflectivity
fig2 = pl.figure(figsize=(50, 50))

#to plot all the data you use 
#ax, im = wradlib.vis.plot_ppi(data,

#To plot only the 30 degree angle and 15km range that corresponds to the volcano you use
#ax, im = wradlib.vis.plot_ppi(data[132:157,0:200]

ax, im = wradlib.vis.plot_ppi(data[132:157,0:200], #The first coordinate is angle and the second is radius
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
                                     ranges=[11200],
                                     angles=[165],
                                     proj=None,
                                     elev=elangle,
                                     line=dict(color='white'),
                                     circle={'edgecolor': 'white'},
                                     )

xlabel = ax.set_xlabel('distancia [m]')
ylabel = ax.set_ylabel('distancia [m]')
title = ax.set_title('{} {} local, {} {} GMT \n DBZH [dBz],  Ángulo de elevación {}°'.format(date,time,dateGMT,timeGMT,elangle))
cb = pl.colorbar(im, ax=ax)