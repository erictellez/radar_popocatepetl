# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 13:01:06 2022

@author: Eric Téllez

This software is to plot the netCDF files into a map with basemap

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
import os.path
from mpl_toolkits.basemap import Basemap
import numpy
from netCDF4 import Dataset as NetCDFFile

raw = NetCDFFile('CFRadial1/0087_20200611/0087_20200611_154000.nc') # Remember that we already defined the main path
#f = wradlib.util.get_wradlib_data_file(fpath)
#raw = wradlib.io.read_opera_hdf5(f)

#To get the name of the file and paste it into the name of the plots
#filename = os.path.basename(filename_with_path) #Filename with extension
#file = os.path.splitext(filename)  #Tuple of string with filename and extension

lat = raw.variables['latitude'][:]
lon = raw.variables['longitude'][:]
time = raw.variables['time'][:]
t2 = raw.variables['p2t'][:] # 2 meter temperature
mslp = nc.variables['msl'][:] # mean sea level pressure
u = nc.variables['p10u'][:] # 10m u-component of winds
v = nc.variables['p10v'][:] # 10m v-component of winds

#save_results_to='C:/Users/radar1/Desktop/Carpeta_Imag/'

#To create a basemap
map = Basemap(projection='merc',llcrnrlon=-100.,llcrnrlat=19.,urcrnrlon=-98.,urcrnrlat=20.,resolution='i')

for i in range(10):  #This number has to change if the number of elevation angle changes
   
    DBZH_horizontal_reflectivity=raw["dataset%d/data2/what" % (i + 1)]["offset"] +(raw["dataset%d/data2/what" % (i + 1)]["gain"])*raw["dataset%d/data2/data" % (i + 1)]
    
    #elevation angle (very important)
    elangle = raw['dataset%d/where' % (i + 1)]['elangle'] #to obtain the elevation angle
    azimuth = raw['dataset%d/how' % (i + 1)]['startazA'] #to obtain all the azimuth angles
    rscale= raw['dataset%d/where' % (i + 1)]['rscale'] #to obtain the conversion factor of the distance
    
    #date and time is almost the same as the name of the archive
    dateGMT = raw['what']['startdate']
    timeGMT = raw['what']['starttime']
    
    #Coordinates
    sitecoords = (raw["where"]["lon"], 
                  raw["where"]["lat"],
                  raw["where"]["height"])

    lons,lats=numpy.meshgrid(lon-180,lat)
    x,y=map(lons,lats)

    clevs=numpy.arange(960,1040,4)
    cs = map.contour(x,ymslp[0,:,:]/100.,clevs,colors='blue',linewidths=1.)
    


