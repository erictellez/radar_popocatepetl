# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 15:06:44 2021

@author: ERIC TELLEZ
"""

#This file is to read and write CFRadial1 data files using 
#xarray cfradial1 backend.

#Most of the code is taken from wradlib_cfradial_backend.ipynb
#from the wradlib example notebooks.



import wradlib as wrl
import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as pl
import numpy as np
import xarray as xr
try: 
    get_ipython().magic("matplotlib inline")
except:
    pl.ionn()
    
#Load CFRadial1 Volume Data
#Be sure to change the address of the files
fpath ='Explosiones_CFRadial1/0087_20210915/0087_20210915_044742.nc' #Here goes the name of the file
f = wrl.util.get_wradlib_data_file(fpath)
vol = wrl.io.open_cfradial1_dataset(f)

#Fix issues of CFRadial azimuth's
for i, swp in enumerate (vol):
    num_rays =int(360 // swp.azimuth.diff("azimuth").median())
    start_rays = swp.dims["azimuth"] - num_rays
    vol[i] = swp.isel(azimuth=slice(start_rays, start_rays + num_rays )).sortby("azimuth")  #This is the elevation angle
    
#Georeferencing
swp = vol[0].copy().pipe(wrl.georef.georeference_dataset)

#Plotting
swp.DBZ.plot.pcolormesh(x='x',y='y')
pl.gca().set_aspect('equal')
fig =pl.figure(figsize=(10,10))
swp.DBZ.wradlib.plot_ppi(proj='cg',fig=fig)
 

#This section is to plot over a real map
import cartopy.feature as cfeature
def plot_borders(ax):
    borders = cfeature.NaturalEarthFeature(category='physical',
                                           name='coastline',
                                           "C:/FTP Radar/0087_20211103_042000_08_02.scn",
                                           "C:/FTP Radar/0087_20211103_042000_01_02.scn",
                                           "C:/FTP Radar/0087_20211103_042000_02_02.scn",
                                           "C:/FTP Radar/0087_20211103_042000_03_02.scn",
                                           "C:/FTP Radar/0087_20211103_042000_04_02.scn",
                                           "C:/FTP Radar/0087_20211103_042000_05_02.scn",
                                           "C:/FTP Radar/0087_20211103_042000_06_02.scn",
                                           "C:/FTP Radar/0087_20211103_042000_07_02.scn",
                                           scale='10m',
                                           facecolor='none')
    ax.add_feature(borders, edgecolor='black', lw=2, zorder=4)

map_proj = ccrs.Mercator(central_longitude=swp.longitude.values)
fig = pl.figure(figsize=(10,8))
ax = fig.add_subplot(111, projection=map_proj)

DBZH = swp.DBZH
pm = DBZH.where(DBZH > 0).wradlib.plot_ppi(ax=ax)
plot_borders(ax)
ax.gridlines(draw_labels=True)


#save images to make a gif


#Make the computational filter to separate rain from ashes


