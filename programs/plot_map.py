# -*- coding: utf-8 -*-
"""
Created on Fri May 19 18:14:00 2023

@author: Eric Téllez

This software is to plot the radar data over a map

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
#path= 'D:/ODIM_H5/**/*.h5'
path= 'D:/ODIM_H5/0087_20221006/0087_20221006_030000.h5'
list_of_files=glob.glob(path, recursive=True)
newest_file = max(list_of_files, key=os.path.getctime)
filename_with_path = wradlib.util.get_wradlib_data_file(newest_file)
raw = wradlib.io.read_opera_hdf5(filename_with_path)

#To get the name of the file and paste it into the name of the plots
filename = os.path.basename(filename_with_path) #Filename with extension
file = os.path.splitext(filename)  #Tuple of string with filename and extension

#dataset%d is the angle
#dataset/data%d/ is the physical variable


for i in range(10):  #This number has to change if the number of elevation angle changes
   
    #RATE_rainfall_intensity=raw["dataset%d/data1/what" % (i + 1)]["offset"] +(raw["dataset%d/data1/what" % (i + 1)]["gain"])*raw["dataset%d/data1/data" % (i + 1)] #This dataset is not that important
    DBZH_horizontal_reflectivity=raw["dataset%d/data2/what" % (i + 1)]["offset"] +(raw["dataset%d/data2/what" % (i + 1)]["gain"])*raw["dataset%d/data2/data" % (i + 1)]
    #VRAD_radial_velocity=raw["dataset%d/data3/what" % (i + 1)]["offset"] +(raw["dataset%d/data3/what" % (i + 1)]["gain"])*raw["dataset%d/data3/data"% (i + 1)]
    #ZDR_reflection_factor_difference=raw["dataset%d/data4/what" % (i + 1)]["offset"] +(raw["dataset%d/data4/what" % (i + 1)]["gain"])*raw["dataset%d/data4/data" % (i + 1)]
    #KDP_propagation_phase_difference_rate_of_change=raw["dataset%d/data5/what" % (i + 1)]["offset"] +(raw["dataset%d/data5/what" % (i + 1)]["gain"])*raw["dataset%d/data5/data" % (i + 1)]
    #PHIDP_differential_propagation_phase=raw["dataset%d/data6/what" % (i + 1)]["offset"] +(raw["dataset%d/data6/what" % (i + 1)]["gain"])*raw["dataset%d/data6/data" % (i + 1)]
    #RHOHV_copolar_correlation_coefficient=raw["dataset%d/data7/what" % (i + 1)]["offset"] +(raw["dataset%d/data7/what" % (i + 1)]["gain"])*raw["dataset%d/data7/data" % (i + 1)]
    #WRAD_doppler_velocity_spectrum_width=raw["dataset%d/data8/what" % (i + 1)]["offset"] +(raw["dataset%d/data8/what" % (i + 1)]["gain"])*raw["dataset%d/data8/data" % (i + 1)]
    #raw['dataset4/data9/data'] #I dont know what this dataset means
    
    #elevation angle (very important)
    elangle = raw['dataset%d/where' % (i + 1)]['elangle'] #to obtain the elevation angle
    azimuth = raw['dataset%d/how' % (i + 1)]['startazA'][132:157] #to obtain all the azimuth angles
    rscale= raw['dataset%d/where' % (i + 1)]['rscale'] #to obtain the conversion factor of the distance
    
    #date and time is almost the same as the name of the archive
    #This data has the format byte and UTF-8 is to convert to string
    dateGMT = raw['what']['startdate'].decode('UTF-8')
    dateGMT = dateGMT[:4]+"-"+ dateGMT[4:]
    dateGMT = dateGMT[:7]+"-"+ dateGMT[7:]
    timeGMT = raw['what']['starttime'].decode('UTF-8')
    timeGMT = timeGMT[:2]+":"+ timeGMT[2:]
    timeGMT = timeGMT[:5]+":"+ timeGMT[5:]
    
    date = raw['what']['Local_date'].decode('UTF-8')
    date = date[:4]+"-"+ date[4:]
    date = date[:7]+"-"+ date[7:]
    time = raw['what']['Local_time'].decode('UTF-8')
    time = time[:2]+":"+ time[2:]
    time = time[:5]+":"+ time[5:]
    
    
    #Coordinates
    sitecoords = (raw["where"]["lon"], 
                  raw["where"]["lat"],
                  raw["where"]["height"])
    
    
    #plot the horizontal reflectivity
    #fig2= pl.figure(figsize=(100, 100))
    
    #Plot the map under the data
    pl.rcParams["figure.figsize"] = [7.00, 3.50]
    pl.rcParams["figure.autolayout"] = True
    im = pl.imread("mapa-iztapopo.png")
    fig2, ax = pl.subplots()
    
    #im = ax.imshow(im, extent=[0, 300, 0, 300])
    #x = numpy.array(range(300))    
    #ax.plot(x, x, ls='dotted', linewidth=2, color='red')
    
        
    #ax, im = wradlib.vis.plot_ppi(DBZH_horizontal_reflectivity[:,0:200], #The first coordinate is angle and the second is radius
    ax, im = wradlib.vis.plot_ppi(DBZH_horizontal_reflectivity[132:157,0:200],
                                  #reflectivity,
                                  rf= 1/rscale,
                                  az= azimuth,
                                  elev= elangle,
                                  fig= fig2,
                                  site= sitecoords,
                                  #proj='cg', #Another type of projection
                                  proj= proj, #Plot
                                  ax=111,
                                  func='pcolormesh')
    
    #To plot the exact point over the crater with a dotted white line
    axe = wradlib.vis.plot_ppi_crosshair(site=sitecoords, 
                                         ranges=[11200],
                                         angles=[165],
                                         proj=None,
                                         elev=elangle,
                                         line=dict(color='white'),
                                         circle={'edgecolor': 'white'},
                                         )
    
    ax.plot(ax, im)
    
    xlabel = ax.set_xlabel('distancia [m]')
    ylabel = ax.set_ylabel('distancia [m]')
    title = ax.set_title('{} {} local, {} {} GMT \n Reflectividad [dBz],  Ángulo de elevación {}°'.format(date,time,dateGMT,timeGMT,elangle))
    cb = pl.colorbar(im, ax=ax)
    
    pl.show()
    #folder_DBZH='C:/Users/radar1/Desktop/Explosion_radar_alta_calidad/'
    #fig2.savefig(folder_DBZH + file[0] + '_DBZH%d' % (i), dpi=100) #To save the plot as an image
