# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 15:14:55 2022

@author: Eric Téllez

This program computes the texture of a variable
http://hydro.ou.edu/files/publications/2007/A%20Fuzzy%20Logic%20Algorithm%20for%20the%20Separation%20of%20Precipitating%20from%20Nonprecipitating%20Echoes%20Using%20Polarimetric%20Radar%20Observations.pdf

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
import matplotlib.pyplot as pl
import os
from osgeo import osr
import glob
import numpy
import warnings
warnings.filterwarnings('ignore')

#To import files automatically
path= 'D:/explosiones/20220909_034300local/H5/0087_20220909/0087_20220909_094500.h5'
#list_of_files=glob.glob(path, recursive=True)
#newest_file = max(list_of_files, key=os.path.getctime)
filename_with_path = wradlib.util.get_wradlib_data_file(path)
raw = wradlib.io.read_opera_hdf5(filename_with_path)

# define your cartesian reference system
# For Mexico City: https://epsg.io/?q=Mexico
proj = osr.SpatialReference()
proj.ImportFromEPSG(6371)

where = raw["dataset1/where"] #to obtain nbins, nrays, rscale, elangle
#nrays is x (rows), nbins is y (columns)
rays=where["nrays"]
bins=where["nbins"]


# this is the radar position tuple (longitude, latitude, altitude)
sitecoords = (raw["where"]["lon"], 
              raw["where"]["lat"],
              raw["where"]["height"])

n=3
m=3 #number of pixels
texture=[]

for a in range(10):

    #DBZH_horizontal_reflectivity=raw["dataset%d/data2/what" % (i + 1)]["offset"] +(raw["dataset%d/data2/what" % (i + 1)]["gain"])*raw["dataset%d/data2/data" % (i + 1)]
    #VRAD_radial_velocity=raw["dataset%d/data3/what" % (i + 1)]["offset"] +(raw["dataset%d/data3/what" % (i + 1)]["gain"])*raw["dataset%d/data3/data"% (i + 1)]
    ZDR_reflection_factor_difference=raw["dataset%d/data4/what" % (a + 1)]["offset"] +(raw["dataset%d/data4/what" % (a + 1)]["gain"])*raw["dataset%d/data4/data" % (a + 1)]
    #KDP_propagation_phase_difference_rate_of_change=raw["dataset%d/data5/what" % (i + 1)]["offset"] +(raw["dataset%d/data5/what" % (i + 1)]["gain"])*raw["dataset%d/data5/data" % (i + 1)]
    PHIDP_differential_propagation_phase=raw["dataset%d/data6/what" % (a + 1)]["offset"] +(raw["dataset%d/data6/what" % (a + 1)]["gain"])*raw["dataset%d/data6/data" % (a + 1)]
    RHOHV_copolar_correlation_coefficient=raw["dataset%d/data7/what" % (a + 1)]["offset"] +(raw["dataset%d/data7/what" % (a + 1)]["gain"])*raw["dataset%d/data7/data" % (a + 1)]
    #WRAD_doppler_velocity_spectrum_width=raw["dataset%d/data8/what" % (i + 1)]["offset"] +(raw["dataset%d/data8/what" % (i + 1)]["gain"])*raw["dataset%d/data8/data" % (i + 1)]

    #elevation angle (very important)
    elangle = raw['dataset%d/where' % (a + 1)]['elangle'] #to obtain the elevation angle
    azimuth = raw['dataset%d/how' % (a + 1)]['startazA'] #to obtain all the azimuth angles
    rscale= raw['dataset%d/where' % (a + 1)]['rscale'] #to obtain the conversion factor of the distance

    for r in range(rays):
        for b in range(bins):
            for i in range(int(-(m-1)/2),1,int((m-1)/2)):
                for j in range(int(-(n-1)/2),1,int((n-1)/2)):
                    point=numpy.sqrt(((ZDR_reflection_factor_difference[r,b]-ZDR_reflection_factor_difference[r+i,b+j])**2)/(n*m))
                    texture = numpy.append(texture,point)

print(texture)                    
#plot the horizontal reflectivity
fig= pl.figure(figsize=(10, 10))
#ax, im = wradlib.vis.plot_ppi(texture[:,0:200], #The first coordinate is angle and the second is radius
ax, im = wradlib.vis.plot_ppi(texture,
                              #reflectivity,
                              rf= 1/rscale,
                              az= azimuth,
                              elev= elangle,
                              fig= fig,
                              site= sitecoords,
                              #proj='cg', #Another type of projection
                              proj= proj, #Plot
                              ax=111,
                              func='pcolormesh')