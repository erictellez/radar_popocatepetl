# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 23:58:56 2021

@author: Eric Tellez

This program is only to plot the data in 3D

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

import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import wradlib as wrl
import numpy as np
import datetime as dt
import h5py
from osgeo import osr

#filename = wrl.util.get_wradlib_data_file('radar_data_examples/ODIM_H5/0087_20210911/0087_20210911_174500.h5')
filename = wrl.util.get_wradlib_data_file('radar_data_examples/Explosiones/20201206_211500/ODIM_H5/0087_20201206_213000.h5')
raw = wrl.io.read_opera_hdf5(filename)
# this is the radar position tuple (longitude, latitude, altitude)
sitecoords = (raw["where"]["lon"], 
              raw["where"]["lat"],
              raw["where"]["height"])


# define your cartesian reference system
# For Mexico City: https://epsg.io/?q=Mexico
proj = osr.SpatialReference()
proj.ImportFromEPSG(6371)

# containers to hold Cartesian bin coordinates and data
xyz, data = np.array([]).reshape((-1, 3)), np.array([])

# iterate over 8 elevation angles
for i in range(8):
    # get the scan metadata for each elevation
    where = raw["dataset%d/where" % (i + 1)] #to obtain nbins, nrays, rscale, rscale, elangle
    what = raw["dataset%d/data2/what" % (i + 1)] # to obtain the gain and the offset
    
       
    # define arrays of polar coordinate arrays (azimuth and range)
    #az = np.arange(how[0], round(how[maxaz-1]), (sector)/where["nrays"])
    #print(azo.shape)
    #print(where["nrays"])
    az = np.arange(0., 360., 360/where["nrays"])
    
    #Generate an zeros array to extend the circular scanned sector to a complete circle
    #azizero = np.zeros((int(where['nrays']*360/sector)-maxaz,where['nbins']))*255
    #azimuth = np.append(az, azizero) #extending the array to a full circle 
    
    # rstart is given in km, so multiply by 1000.
    rstart = where["rstart"] * 1000.
    r = np.arange(rstart,
                  rstart + where["nbins"] * where["rscale"],
                  where["rscale"])
    
    # derive 3-D Cartesian coordinate tuples
    xyz_ = wrl.vpr.volcoords_from_polar(sitecoords, 
                                        where["elangle"],
                                        az, 
                                        r, 
                                        proj)

    # get the scan data for this elevation
    #   here, you can do all the processing on the 2-D polar level
    #   e.g. clutter elimination, attenuation correction, ...
    #data_ = what["offset"] + (what["gain"])* raw[
    #    "dataset%d/data2/data" % (i + 1)] 
    
    data_ =  what["offset"] +(what["gain"])*raw[
        "dataset%d/data2/data" % (i + 1)] 
    
    """
    data_ = (what["offset"] +(what["gain"])*raw[
        "dataset%d/data2/data" % (i + 1)] -rawclutter[
            "dataset%d/data2/data" % (i + 1)])       # Here I can substract the ground, that means the clutter elimination
    
    
    The next function is written based on 
    Gianfranco Vulpiani, Mario Montopoli, Luca Delli Passeri, Antonio G. Gioia, Pietro Giordano, and Frank S. Marzano. 
    On the use of dual-polarized c-band radar for operational rainfall retrieval in mountainous areas. 
    Journal of Applied Meteorology and Climatology, 51(2):405–425, Feb 2012. 
    doi:10.1175/JAMC-D-10-05024.1.         
    
    wradlib.clutter.classify_echo_fuzzy(dat, weights=None, trpz=None, thresh=0.5)
    """    
    
    # transfer to containers
    xyz, data = np.vstack((xyz, xyz_)), np.append(data, data_.ravel())

mpl.rcParams['legend.fontsize'] = 10

fig = plt.figure()
ax = fig.gca(projection='3d')
 
ax.plot(data[:,1],)
