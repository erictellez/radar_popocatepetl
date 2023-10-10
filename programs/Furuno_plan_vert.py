# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 02:52:47 2021

@author: Eric Tellez

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
import numpy as np
import datetime as dt
import h5py
from osgeo import osr

# read the data (Furuno data)
filename = wrl.util.get_wradlib_data_file('radar_data_examples/explosiones/20201206_211500/ODIM_H5/0087_20201206_213000.h5')
#filename = wrl.util.get_wradlib_data_file('radar_data_examples/ODIM_H5/0087_20210911/0087_20210911_174500.h5')
raw = wrl.io.read_opera_hdf5(filename)
# this is the radar position tuple (longitude, latitude, altitude)
sitecoords = (raw["where"]["lon"], 
              raw["where"]["lat"],
              raw["where"]["height"])

#r= #This is the range. I have to find the number of elevation angles in the file  

# define your cartesian reference system
# For Mexico City: https://epsg.io/?q=Mexico
proj = osr.SpatialReference()
proj.ImportFromEPSG(6371)
# create Cartesian coordinates corresponding the location of the
# polar volume bins
polxyz  = wradlib.vpr.volcoords_from_polar(sitecoords, elevs,
                                           azims, ranges, proj)

for i in range(8):
    # get the scan metadata for each elevation
    where = raw["dataset%d/where" % (i + 1)]
    what = raw["dataset%d/data2/what" % (i + 1)]
    
    
    x=['dataset%d/how' % (1+d)]['startazA']*cos(['dataset'])
    y=
    z=
    dataxy= 
    datazx=
    datazy=


wrl.vis.plot_plan_and_vert(x, y, z, dataxy,dataxz,datayz 
                               unit="Horizontal Reflectivity {0}".format(unit),
                               levels=range(-32, 60), 
                               title='CAPPI: Radar {0}, {1}T{2}GMT {3}T{4}Altzomoni'.format(sensorname,dateGMT,timeGMT,date,time))