# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 17:03:38 2022

@author: Eric Téllez

Plot netCDF over a map with basemap

https://www.youtube.com/watch?v=r5m_aU5V6oY
https://www.youtube.com/watch?v=dSv3-obKv3M

"""

from netCDF4 import Dataset
import numpy
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

#This files should be .nc
#data = Dataset(r'd:\')
#data.variables.keys

lats=data.variables['lat'][:]
lons=data.variables['lon'][:]
time=data.variables['time'][:]

#tave is another varaible

#for reflectivity
othervariables=data.variables[''][:]

#To create de corners of the map
mp=Basemap(projection='merc',
           llcrnrlon= ,
           llcrnrlat= ,
           urcrnrlon= ,
           urcrnrlat= ,
           resolution='i')

lon, lat = numpy-meshgrid(lons,lats)
x,y = mp(lon,lat)

c_scheme = mp.pcolor(x,y,numpy.squeez(tave[0,:,:]),cmap='jet')

mp.drawcoastlines()
mp.drawstates()
mp.drawcontries()

cbar=mp.colorbar(c_scheme, location = 'right', pad = '10%')

plt.title('Reflectivity')
plt.show()