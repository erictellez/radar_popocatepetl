# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 22:20:33 2021

@author: Eric Tellez
    
Vertical Profile of Reflectivity (VPR) from wradlib
suited for Furuno WR-2100


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

import wradlib
import numpy as np
from osgeo import osr
import matplotlib.pyplot as pl
pl.interactive(True)

# read the data (Furuno data)
filename = wradlib.util.get_wradlib_data_file('radar_data_examples/explosiones/20201206_211500/ODIM_H5/0087_20201206_213000.h5')
#filename = wrl.util.get_wradlib_data_file('radar_data_examples/ODIM_H5/0087_20210911/0087_20210911_174500.h5')
raw = wradlib.io.read_opera_hdf5(filename)
# this is the radar position tuple (longitude, latitude, altitude)
sitecoords = (raw["where"]["lon"], 
              raw["where"]["lat"],
              raw["where"]["height"])


# define elevation and azimuth angles, ranges, radar site coordinates,
# projection
elevs  = np.array([3.1,4.5,6.0,8.2,11.,14.,18.,28.])
azims  = np.arange(0., 360., 1.)
ranges = np.arange(0., 15000., 100.)

# define your cartesian reference system
# For Mexico City: https://epsg.io/?q=Mexico
proj = osr.SpatialReference()
proj.ImportFromEPSG(6371)

# create Cartesian coordinates corresponding the location of the
# polar volume bins
polxyz  = wradlib.vpr.volcoords_from_polar(sitecoords, 
                                           elevs,
                                           azims, 
                                           ranges, 
                                           proj)  # noqa

#This synthetic polar volume is a 3D data
poldata = wradlib.vpr.synthetic_polar_volume(polxyz)
#actual data must be constructed stacking all the angles
#poldata = raw["dataset1/data2/data"]

# this is the shape of our polar volume
polshape = (len(elevs),len(azims),len(ranges))

# now we define the coordinates for the 3-D grid (the CAPPI layers)
x = np.linspace(polxyz[:,0].min(), polxyz[:,0].max(), 120)
y = np.linspace(polxyz[:,1].min(), polxyz[:,1].max(), 120)
z = np.arange(500.,10500.,500.)
xyz = wradlib.util.gridaspoints(z, y, x)
gridshape = (len(z), len(y), len(x))

# create an instance of the CAPPI class and
# use it to create a series of CAPPIs
gridder = wradlib.vpr.CAPPI(polxyz, 
                            xyz, 
                            maxrange=15000,  # noqa
                            minelev=elevs.min(), 
                            maxelev=elevs.max(),
                            ipclass=wradlib.ipol.Idw)

gridded = np.ma.masked_invalid( gridder(poldata) ).reshape(gridshape)

# plot results
levels = np.linspace(0,100,25)
wradlib.vis.plot_max_plan_and_vert(x, 
                                   y, 
                                   z, 
                                   gridded, 
                                   levels=levels,
                                   cmap=pl.cm.viridis)
pl.show()