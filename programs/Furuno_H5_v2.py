# -*- coding: utf-8 -*-
"""
Created on Sun Sep 12 01:48:15 2021

@author: ERIC TELLEZ
This program is for visualizing the converted cartesian data in polar form
"""


import wradlib as wrl
import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as pl
import numpy as np
try:
    get_ipython().magic("matplotlib inline")
except:
    pl.ion()
    
fpath = 'ODIM_H5/0087_20210912/0087_20210912_154000.h5' # Remember that we already defined the main path
f = wrl.util.get_wradlib_data_file(fpath)
fcontent = wrl.io.read_opera_hdf5(f)

# which keywords can be used to access the content?
#print(fcontent.keys())
# print the entire content including values of data and metadata
# (numpy arrays will not be entirely printed)
#print(fcontent['dataset1/data2/data'])

# Remember that the dataset1/data1/data corresponds to elevation_angle/meteorological_parameter/data.
# dataset1=3.1 and data2=dBz

# dataset#/how contains the elevation angle and the azimuth angle of each measurement and that corresponds to X axis of the reflectivity data with 238 bins

type(fcontent['dataset1/how']) #This is a dictionary
type(fcontent['dataset1/how']['startazA']) #This is an array
type(fcontent['dataset1/data2/data']) #This is an array
type(fcontent['where']) #This is a dictionary

# Coordinates are always the same
# (longitude,latitude,altitude)
sitio=(-98.65487,19.11921,4007.0)

fig = pl.figure(figsize=(10, 10))
im = wrl.vis.plot_ppi(fcontent['dataset1/data2/data'],
                      az=fcontent['dataset1/how']['startazA'],
                      fig=fig,
                      proj='cg') #Plot


fig = pl.figure(figsize=(10, 8))
cgax, pm=im = wrl.vis.plot_ppi(fcontent['dataset1/data2/data'],
                      az=fcontent['dataset1/how']['startazA'], 
                      elev=fcontent['dataset1/how']['elangles'], 
                      site=sitio,
                      fig=fig, 
                      func='pcolormesh',
                      proj='cg') #cg stands for curvilinear grid

caax = cgax.parasites[0]
paax = cgax.parasites[1]

## To create the 
#pl.title('HERE SHOULD BE THE NAME OF THE FILE', y=1.05)
cbar = pl.colorbar(pm, pad=0.075, ax=paax)
caax.set_xlabel('x_range [km]')
caax.set_ylabel('y_range [km]')
pl.text(1.0, 1.05, 'azimuth', transform=caax.transAxes, va='bottom',
        ha='right')
cbar.set_label('reflectivity [dBZ]') #reflectivity only if we plot data2    
