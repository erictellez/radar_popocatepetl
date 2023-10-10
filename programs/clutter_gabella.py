# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 20:38:53 2022

@author: Eric Tellez
This software is to plot all the variables at all the elevation angles.
The plot draws the horizontal plane of an explosion seen from above. 


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
import numpy
from osgeo import osr
import glob
import os.path
import warnings
warnings.filterwarnings('ignore')

# define your cartesian reference system
# For Mexico City: https://epsg.io/?q=Mexico
proj = osr.SpatialReference()
proj.ImportFromEPSG(6371)

#To import files automatically
path= 'D:/explosion/H5/**/*.h5'
list_of_files=glob.glob(path, recursive=True)
all_files=len(list_of_files)

path_clutter='D:/Ground_Clutter/Clutter_base/Clutter_popo_30km.npy'
Clutter = numpy.load(path_clutter)

#dataset%d is the angle
#dataset/data%d/ is the physical variable

for i in range(all_files): #number of files
    current_file = list_of_files[2]
    filename_path = wradlib.util.get_wradlib_data_file(current_file)
    raw = wradlib.io.read_opera_hdf5(filename_path)
   
    #To get the name of the file and paste it into the name of the plots
    filename = os.path.basename(filename_path) #Filename with extension
    file = os.path.splitext(filename)  #Tuple of string with filename and extension
    
    DBZH_horizontal_reflectivity=raw["dataset8/data2/what"]["offset"] +(raw["dataset8/data2/what"]["gain"])*raw["dataset8/data2/data"]
    #VRAD_radial_velocity=raw["dataset%d/data3/what" % (i + 1)]["offset"] +(raw["dataset%d/data3/what" % (i + 1)]["gain"])*raw["dataset%d/data3/data"% (i + 1)]
    #ZDR_reflection_factor_difference=raw["dataset%d/data4/what" % (i + 1)]["offset"] +(raw["dataset%d/data4/what" % (i + 1)]["gain"])*raw["dataset%d/data4/data" % (i + 1)]
    #KDP_propagation_phase_difference_rate_of_change=raw["dataset%d/data5/what" % (i + 1)]["offset"] +(raw["dataset%d/data5/what" % (i + 1)]["gain"])*raw["dataset%d/data5/data" % (i + 1)]
    #PHIDP_differential_propagation_phase=raw["dataset%d/data6/what" % (i + 1)]["offset"] +(raw["dataset%d/data6/what" % (i + 1)]["gain"])*raw["dataset%d/data6/data" % (i + 1)]
    #RHOHV_copolar_correlation_coefficient=raw["dataset%d/data7/what" % (i + 1)]["offset"] +(raw["dataset%d/data7/what" % (i + 1)]["gain"])*raw["dataset%d/data7/data" % (i + 1)]
    #WRAD_doppler_velocity_spectrum_width=raw["dataset%d/data8/what" % (i + 1)]["offset"] +(raw["dataset%d/data8/what" % (i + 1)]["gain"])*raw["dataset%d/data8/data" % (i + 1)]
    
    #elevation angle (very important)
    elangle = raw['dataset8/where']['elangle'] #to obtain the elevation angle
    azimuth = raw['dataset8/how']['startazA'] #to obtain all the azimuth angles
    rscale= raw['dataset8/where']['rscale'] #to obtain the conversion factor of the distance

    #date and time is almost the same as the name of the archive
    #This data has the format byte and UTF-8 is to convert to string
    dateGMT = raw['what']['startdate'].decode('UTF-8')
    dateGMT = dateGMT[:4]+"-"+ dateGMT[4:]
    dateGMT = dateGMT[:7]+"-"+ dateGMT[7:]
    timeGMT = raw['what']['starttime'].decode('UTF-8')
    timeGMT = timeGMT[:2]+":"+ timeGMT[2:]
    timeGMT = timeGMT[:5]+":"+ timeGMT[5:]

    #Coordinates
    sitecoords = (raw["where"]["lon"], 
                  raw["where"]["lat"],
                  raw["where"]["height"])
    
    DBZH_wo_clutter=DBZH_horizontal_reflectivity[:,0:401]-Clutter[6,:,:]
    
    #plot the horizontal reflectivity
    fig= pl.figure(figsize=(20,8))
        
    clmap = wradlib.clutter.filter_gabella(DBZH_wo_clutter[:,0:401],
                                           wsize=5,
                                           thrsnorain=0.,
                                           tr1=6.,
                                           n_p=8,
                                           tr2=1.3,
                                           radial=False,
                                           cartesian=False)
        
    data_no_clutter = wradlib.ipol.interpolate_polar(DBZH_wo_clutter[:,0:401], clmap)
        
    ax, pm = wradlib.vis.plot_ppi(data_no_clutter[:,0:401], 
                                  #data_no_clutter,
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
        
    xlabel = ax.set_xlabel('distancia [m]')
    ylabel = ax.set_ylabel('distancia [m]')
    title = ax.set_title('Data no clutter DBZH [dBz]')
    cb = pl.colorbar(pm, ax=ax)
        
    #To plot the exact point over the crater with a dotted white line
    ax, pm = wradlib.vis.plot_ppi_crosshair(site=sitecoords, 
                                            ranges=[12000],
                                            angles=[165],
                                            proj=None,
                                            elev=elangle,
                                            line=dict(color='white'),
                                            circle={'edgecolor': 'white'},
                                            )