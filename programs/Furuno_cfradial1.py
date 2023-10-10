# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 15:06:44 2021

@author: ERIC TELLEZ

#This file is to read and write CFRadial data files using 
#xarray cfradial1 backend.

#Most of the code is taken from wradlib_cfradial_backend.ipynb
#from the wradlib example notebooks.


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
#Be sure to write the proper path of the files
#Remember that the name of the files have the GMT hour, 5 or 6 hours later
#of the hour in Altzomoni
#fpath ='radar_data_examples/CFRadial/0087_20200626/0087_20200626_135500.nc' #Here goes the name of the file

fpath ='radar_data_examples/CFRadial/0087_20201206/0087_20201206_211500.nc' #Here goes the name of the file
f = wrl.util.get_wradlib_data_file(fpath)
vol = wrl.io.open_cfradial1_dataset(f)
#vol = wrl.io.open_cfradial1_mfdataset(f)

# which keywords can be used to access the content?
# print(f.keys())
# print the entire content including values of data and metadata
# (numpy arrays will not be entirely printed)
# print(f['dataset1/data2/data'])

#Fix issues of CFRadial azimuth's
for i, swp in enumerate (vol):
    num_rays =int(360 // swp.azimuth.diff("azimuth").median())
    start_rays = swp.dims["azimuth"] - num_rays
    vol[i] = swp.isel(azimuth=slice(start_rays, start_rays + num_rays )).sortby("azimuth")  #This is the elevation angle
    
#Georeferencing
swp = vol[1].copy().pipe(wrl.georef.georeference_dataset)

#Plotting
swp.DBZ.plot.pcolormesh(x='x',y='y')
pl.gca().set_aspect('auto') #Function set_aspect('auto') is to make the plot equal in both axes

fig =pl.figure(figsize=(10,10))
swp.DBZ.wradlib.plot_ppi(proj='cg',fig=fig)
 

#This section is to plot over a real map
import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
def plot_borders(ax):
    borders = cfeature.NaturalEarthFeature(category='physical',
                                           name='coastline',
                                           scale='10m',
                                           facecolor='none')
    ax.add_feature(borders, edgecolor='black', lw=2, zorder=4)

map_proj = ccrs.AzimuthalEquidistant(central_latitude=swp.latitude.values, 
                                      central_longitude=swp.longitude.values)
pm = swp.DBZ.wradlib.plot_ppi(proj=map_proj)
ax = pl.gca()
ax.gridlines(crs=map_proj)
print(ax)

map_proj = ccrs.Mercator(central_longitude=swp.longitude.values)
fig = pl.figure(figsize=(10,8))
ax = fig.add_subplot(111, projection=map_proj)

DBZ = swp.DBZ
pm = DBZ.where(DBZ > 0).wradlib.plot_ppi(ax=ax)
plot_borders(ax)
ax.gridlines(draw_labels=True)


#save images to make a gif




