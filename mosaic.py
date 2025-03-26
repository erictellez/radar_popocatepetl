# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 18:02:37 2022

@author: Eric Téllez

This software is to plot all the variables at a single constant elevation angle.
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
path= 'D:/ODIM_H5/**/*.h5'
list_of_files=glob.glob(path, recursive=True)
newest_file = max(list_of_files, key=os.path.getctime)
filename_with_path = wradlib.util.get_wradlib_data_file(newest_file)
raw = wradlib.io.read_opera_hdf5(filename_with_path)

#To get the name of the file and paste it into the name of the plots
filename = os.path.basename(filename_with_path) #Filename with extension
file = os.path.splitext(filename)  #Tuple of string with filename and extension


for i in range(10):  #This number has to change if the number of elevation angle changes
   
    RATE_rainfall_intensity=raw["dataset%d/data1/what" % (i + 1)]["offset"] +(raw["dataset%d/data1/what" % (i + 1)]["gain"])*raw["dataset%d/data1/data" % (i + 1)] #This dataset is not that important
    DBZH_horizontal_reflectivity=raw["dataset%d/data2/what" % (i + 1)]["offset"] +(raw["dataset%d/data2/what" % (i + 1)]["gain"])*raw["dataset%d/data2/data" % (i + 1)]
    VRAD_radial_velocity=raw["dataset%d/data3/what" % (i + 1)]["offset"] +(raw["dataset%d/data3/what" % (i + 1)]["gain"])*raw["dataset%d/data3/data"% (i + 1)]
    ZDR_reflection_factor_difference=raw["dataset%d/data4/what" % (i + 1)]["offset"] +(raw["dataset%d/data4/what" % (i + 1)]["gain"])*raw["dataset%d/data4/data" % (i + 1)]
    KDP_propagation_phase_difference_rate_of_change=raw["dataset%d/data5/what" % (i + 1)]["offset"] +(raw["dataset%d/data5/what" % (i + 1)]["gain"])*raw["dataset%d/data5/data" % (i + 1)]
    PHIDP_differential_propagation_phase=raw["dataset%d/data6/what" % (i + 1)]["offset"] +(raw["dataset%d/data6/what" % (i + 1)]["gain"])*raw["dataset%d/data6/data" % (i + 1)]
    RHOHV_copolar_correlation_coefficient=raw["dataset%d/data7/what" % (i + 1)]["offset"] +(raw["dataset%d/data7/what" % (i + 1)]["gain"])*raw["dataset%d/data7/data" % (i + 1)]
    WRAD_doppler_velocity_spectrum_width=raw["dataset%d/data8/what" % (i + 1)]["offset"] +(raw["dataset%d/data8/what" % (i + 1)]["gain"])*raw["dataset%d/data8/data" % (i + 1)]
    #raw['dataset4/data9/data'] #I dont know what this dataset means
    
    #elevation angle (very important)
    elangle = raw['dataset%d/where' % (i + 1)]['elangle'] #to obtain the elevation angle
    azimuth = raw['dataset%d/how' % (i + 1)]['startazA'] #to obtain all the azimuth angles
    rscale= raw['dataset%d/where' % (i + 1)]['rscale'] #to obtain the conversion factor of the distance
    
    #date and time is almost the same as the name of the archive
    dateGMT = raw['what']['startdate'].decode('UTF-8') #Change byte type to integer
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
    
    #plot all the images in one figure
    fig= pl.figure(figsize=(20, 10 ))
    #fig, ax = pl.subplots(nrows=2, ncols=4, sharex=True, sharey=True, figsize=(20, 10))
    fig.suptitle('{} {} Local, {} {} GMT \n Ángulo de elevación {}°'.format(date,time,dateGMT,timeGMT,elangle), fontsize=10)
    fig.supxlabel('distancia [m]', fontsize=10)
    fig.supylabel('distancia [m]', fontsize=10)
    pl.tight_layout()
    
    #plot the possible amount of rain
    #ax, im = wradlib.vis.plot_ppi(RATE_rainfall_intensity[:,0:200], #The first coordinate is angle and the second is radius
    #The line above is to cut the image right after the distance of Popocatepetl volcano corresponding
    #to the data 200
    ax = fig.add_subplot(241, frameon=False)
    #pl.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=True, right=False)
    
    ax, im = wradlib.vis.plot_ppi(RATE_rainfall_intensity,
                                  #reflectivity,
                                  rf= 1/rscale,
                                  az= azimuth,
                                  elev= elangle,
                                  fig= fig,
                                  site= sitecoords,
                                  #proj='cg', #Another type of projection
                                  proj= proj, #Plot
                                  ax=ax,
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
    
    title = ax.set_title('Intensidad de lluvia [mm/h]', fontsize=10)
    cb = pl.colorbar(im, ax=ax)
    cb.ax.tick_params(labelsize=6)
    pl.rc('xtick', labelsize=6) 
    pl.rc('ytick', labelsize=6)
    
    #plot the horizontal reflectivity
    #ax, im = wradlib.vis.plot_ppi(DBZH_horizontal_reflectivity[:,0:200], #The first coordinate is angle and the second is radius
    ax = fig.add_subplot(242, frameon=False)
    pl.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
    ax, im = wradlib.vis.plot_ppi(DBZH_horizontal_reflectivity,
                                  #reflectivity,
                                  rf= 1/rscale,
                                  az= azimuth,
                                  elev= elangle,
                                  fig= fig,
                                  site= sitecoords,
                                  #proj='cg', #Another type of projection
                                  proj= proj, #Plot
                                  ax=ax,
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
    
    title = ax.set_title('Reflectividad [dBz]', fontsize=10)
    cb = pl.colorbar(im, ax=ax)
    cb.ax.tick_params(labelsize=6)  #size font of the colorbar
    pl.rc('xtick', labelsize=6)    #size font of the x-axes
    pl.rc('ytick', labelsize=6)    #size font of the y-axes
    
    #plot the radial velocity of the wind
    ax = fig.add_subplot(244, frameon=False)
    pl.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
    #ax, im = wradlib.vis.plot_ppi(VRAD_radial_velocity[:,0:200], #The first coordinate is angle and the second is radius
    ax, im = wradlib.vis.plot_ppi(VRAD_radial_velocity,
                                  #reflectivity,
                                  rf= 1/rscale,
                                  az= azimuth,
                                  elev= elangle,
                                  fig= fig,
                                  site= sitecoords,
                                  #proj='cg', #Another type of projection
                                  proj= proj, #Plot
                                  ax=ax,
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
    
    title = ax.set_title('VRAD [m/s]', fontsize=10)
    cb = pl.colorbar(im, ax=ax)
    cb.ax.tick_params(labelsize=6)
    pl.rc('xtick', labelsize=6) 
    pl.rc('ytick', labelsize=6)
    
    #plot
    ax = fig.add_subplot(243, frameon=False)
    pl.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
    #ax, im = wradlib.vis.plot_ppi(ZDR_reflection_factor_difference[:,0:200], #The first coordinate is angle and the second is radius
    ax, im = wradlib.vis.plot_ppi(ZDR_reflection_factor_difference,                                  
                                  #reflectivity,
                                  rf= 1/rscale,
                                  az= azimuth,
                                  elev= elangle,
                                  fig= fig,
                                  site= sitecoords,
                                  #proj='cg', #Another type of projection
                                  proj= proj, #Plot
                                  ax=ax,
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
    
    title = ax.set_title('ZDR [dB]', fontsize=10)
    cb = pl.colorbar(im, ax=ax)
    cb.ax.tick_params(labelsize=6)
    pl.rc('xtick', labelsize=6) 
    pl.rc('ytick', labelsize=6)
    
    #Plot
    ax = fig.add_subplot(245, frameon=False)
    #pl.tick_params(labelcolor='none', which='both', top=False, bottom=True, left=True, right=False)
    #ax, im = wradlib.vis.plot_ppi(KDP_propagation_phase_difference_rate_of_change[:,0:200], #The first coordinate is angle and the second is radius
    ax, im = wradlib.vis.plot_ppi(KDP_propagation_phase_difference_rate_of_change,
                                  #reflectivity,
                                  rf= 1/rscale,
                                  az= azimuth,
                                  elev= elangle,
                                  fig= fig,
                                  site= sitecoords,
                                  #proj='cg', #Another type of projection
                                  proj= proj, #Plot
                                  ax=ax,
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
    
    title = ax.set_title('KDP [deg/km]', fontsize=10)
    cb = pl.colorbar(im, ax=ax)
    cb.ax.tick_params(labelsize=6)
    pl.rc('xtick', labelsize=6) 
    pl.rc('ytick', labelsize=6)
    
    #plot the differential propagation phase
    ax = fig.add_subplot(246, frameon=False)
    pl.tick_params(labelcolor='none', which='both', top=False, bottom=True, left=False, right=False)
    #ax, im = wradlib.vis.plot_ppi(PHIDP_differential_propagation_phase[:,0:200], #The first coordinate is angle and the second is radius
    ax, im = wradlib.vis.plot_ppi(PHIDP_differential_propagation_phase,
                                  #reflectivity,
                                  rf= 1/rscale,
                                  az= azimuth,
                                  elev= elangle,
                                  fig= fig,
                                  site= sitecoords,
                                  #proj='cg', #Another type of projection
                                  proj= proj, #Plot
                                  ax=ax,
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
    
    title = ax.set_title('PHIDP [deg]', fontsize=10)
    cb = pl.colorbar(im, ax=ax)
    cb.ax.tick_params(labelsize=6)
    pl.rc('xtick', labelsize=6) 
    pl.rc('ytick', labelsize=6)
    
    #Plot the copolar correlation coefficient
    ax = fig.add_subplot(247, frameon=False)
    pl.tick_params(labelcolor='none', which='both', top=False, bottom=True, left=False, right=False)
    #ax, im = wradlib.vis.plot_ppi(RHOHV_copolar_correlation_coefficient[:,0:200], #The first coordinate is angle and the second is radius
    ax, im = wradlib.vis.plot_ppi(RHOHV_copolar_correlation_coefficient,
                                  #reflectivity,
                                  rf= 1/rscale,
                                  az= azimuth,
                                  elev= elangle,
                                  fig= fig,
                                  site= sitecoords,
                                  #proj='cg', #Another type of projection
                                  proj= proj, #Plot
                                  ax=ax,
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
    
    title = ax.set_title('RHOHV', fontsize=10)
    cb = pl.colorbar(im, ax=ax)
    cb.ax.tick_params(labelsize=6)
    pl.rc('xtick', labelsize=6) 
    pl.rc('ytick', labelsize=6)
    
    #Plot the standard deviation of the wind velocity
    ax = fig.add_subplot(248, frameon=False)
    pl.tick_params(labelcolor='none', which='both', top=False, bottom=True, left=False, right=False)
    #ax, im = wradlib.vis.plot_ppi(WRAD_doppler_velocity_spectrum_width[:,0:200], #The first coordinate is angle and the second is radius
    ax, im = wradlib.vis.plot_ppi(WRAD_doppler_velocity_spectrum_width,
                                  #reflectivity,
                                  rf= 1/rscale,
                                  az= azimuth,
                                  elev= elangle,
                                  fig= fig,
                                  site= sitecoords,
                                  #proj='cg', #Another type of projection
                                  proj= proj, #Plot
                                  ax=ax,
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
    
    title = ax.set_title('WRAD [m/s]', fontsize=10)
    cb = pl.colorbar(im, ax=ax)
    cb.ax.tick_params(labelsize=6)
    pl.rc('xtick', labelsize=6) 
    pl.rc('ytick', labelsize=6)
    
    folder_mosaic='D:/Carpeta_Imag/mosaic/'
    fig.savefig(folder_mosaic + file[0] + '_mosaic%d' % (i),dpi=100)  #To save the plot as an image