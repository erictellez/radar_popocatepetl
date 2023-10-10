# -*- coding: utf-8 -*-
"""
Created on Sun Sep 12 01:48:15 2021

@author: ERIC TELLEZ
This program is to visualize the cartesian h5 data (normally open with Panoply) 
but in polar coordinates.

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
import h5py
from osgeo import osr
try:
    get_ipython().magic("matplotlib inline")
except:
    pl.ion()
    
#fpath = 'radar_data_examples/Explosiones/20210915_044742/ODIM_H5/0087_20210915_045031.h5' # Remember that we already defined the main path
fpath = 'ODIM_H5/0087_20210912/0087_20210912_154000.h5' # Remember that we already defined the main path
f = wrl.util.get_wradlib_data_file(fpath)
fcontent = wrl.io.read_opera_hdf5(f)

# define your cartesian reference system
# For Mexico City: https://epsg.io/?q=Mexico
proj = osr.SpatialReference()
proj.ImportFromEPSG(6371)

# which keywords can be used to access the content?
#Øprint(fcontent.keys())
# print the entire content including values of data and metadata
# (numpy arrays will not be entirely printed)
#print(fcontent['dataset1/data2/data'])

# Remember that the dataset1/data1/data corresponds to elevation_angle/meteorological_parameter/data.
# dataset1=3.1 and data2=dBz

# dataset#/how contains the elevation angle and the azimuth angle of each measurement and that corresponds to X axis of the reflectivity data with 238 bins
# ['dataset#/how']['startazA'] azimuth angles
# ['dataset#/how']['elangles'] elevation angles (all the entries have the same angle

# dataset#/where/elangle has the elevation angle


type(fcontent['dataset1/how']) #This is a dictionary
type(fcontent['dataset1/how']['startazA']) #This is an array
type(fcontent['dataset1/data2/data']) #This is an array
type(fcontent['where']) #This is a dictionary with (altitude,latitude,longitude)
type(fcontent['where']['lon']) #This is an array

# Coordinates are always the same
# (longitude,latitude,altitude)
#sitio=(-98.65487,19.11921,4007.0)
sitio=(fcontent['where']['lon'], #This form is more general
       fcontent['where']['lat'],
       fcontent['where']['height'])

fig = pl.figure(figsize=(10, 10))
im = wrl.vis.plot_ppi(fcontent['dataset8/data2/data'],
                      az=fcontent['dataset8/how']['startazA'],
                      fig=fig,
                      proj=proj) #Plot


fig = pl.figure(figsize=(10, 8))
cgax, pm=im = wrl.vis.plot_ppi(fcontent['dataset1/data2/data'],
                      az=fcontent['dataset1/how']['startazA'], 
                      elev=fcontent['dataset1/how']['elangles'], 
                      #r=fcontent['dataset1/where']['nbins','nrays'], #this is not right
                      rf=fcontent['dataset1/where']['rstart']+fcontent['dataset1/where']['rscale']*fcontent['dataset1/where']['nbins']*1000, #this numbre is not right
                      site=sitio,
                      fig=fig, 
                      func='pcolormesh',
                      proj=proj) #cg stands for curvilinear grid

fig.savefig('Reflectivity',dpi=100)  #To save the plot as an image
"""
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
"""