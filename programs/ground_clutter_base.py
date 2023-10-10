# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 17:10:22 2022

@author: Eric Téllez

Ground clutter base

This program is to generate the Ground Clutter from data of clear sky days.
This is the first step to take out the ground from the reflectivity profile.

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
import glob
import numpy
from osgeo import osr
import warnings
warnings.filterwarnings('ignore')


# define your cartesian reference system
# For Mexico City: https://epsg.io/?q=Mexico
proj = osr.SpatialReference()
proj.ImportFromEPSG(6371)

#To import several files automatically
path= 'D:/Ground_Clutter/H5/**/*.h5'
list_of_files=glob.glob(path, recursive=True)  #This is a list
all_files=len(list_of_files) #Total number of files
#print(all_files)

#dataset%d is the angle
#dataset/data%d/ is the physical variable
Clutter_DBZH=numpy.array([]).reshape(-1,1,1)
#Clutter_RATE=numpy.array([]).reshape(-1,1,1)
#Clutter_VRAD=numpy.array([]).reshape(-1,1,1)
#Clutter_ZDR=numpy.array([]).reshape(-1,1,1)
#Clutter_KDP=numpy.array([]).reshape(-1,1,1)
#Clutter_PHIDP=numpy.array([]).reshape(-1,1,1)
#Clutter_RHOHV=numpy.array([]).reshape(-1,1,1)
#Clutter_WRAD=numpy.array([]).reshape(-1,1,1)

for a in range(8):  #number of elevation angles

    DBZH=numpy.array([]).reshape(-1,1,1)
    #RATE=numpy.array([]).reshape(-1,1,1)
    #VRAD=numpy.array([]).reshape(-1,1,1)
    #ZDR=numpy.array([]).reshape(-1,1,1)
    #KDP=numpy.array([]).reshape(-1,1,1)
    #PHIDP=numpy.array([]).reshape(-1,1,1)
    #RHOHV=numpy.array([]).reshape(-1,1,1)
    #WRAD=numpy.array([]).reshape(-1,1,1)

    
    for i in range(all_files): #number of files to make the average
        current_file = list_of_files[i]
        filename_path = wradlib.util.get_wradlib_data_file(current_file)
        raw = wradlib.io.read_opera_hdf5(filename_path)
        
        rscale = raw['dataset%d/where' %(a+1)]['rscale'] #to obtain the conversion factor of the distance. It is the same for all the angles
    
        #nrays is x (rows), nbins is y (columns)
        rays = raw["dataset%d/where" % (a + 1)]["nrays"] #to obtain nbins, nrays, rscale, elangle
        bins = raw["dataset%d/where" % (a + 1)]["nbins"]   
        
        what = raw["dataset%d/data2/what" % (a + 1)] # to obtain the gain and the offset
        
        #Coordinates
        sitecoords = (raw["where"]["lon"], 
                      raw["where"]["lat"],
                      raw["where"]["height"])
    
        elangle = raw['dataset%d/where' %(a+1)]['elangle'] #to obtain the elevation angle
        azimuth = raw['dataset%d/how' %(a+1)]['startazA'] #to obtain all the azimuth angles


        if rays==317 and bins==401:
            #RATE_angle=raw["dataset%d/data1/what"%(a+1)]["offset"] +(raw["dataset%d/data1/what"%(a+1)]["gain"])*raw["dataset%d/data1/data"%(a+1)] #This dataset is not that important
            DBZH_angle=raw["dataset%d/data2/what"%(a+1)]["offset"] +(raw["dataset%d/data2/what"%(a+1)]["gain"])*raw["dataset%d/data2/data"%(a+1)]
            #VRAD_angle=raw["dataset%d/data3/what"%(a+1)]["offset"] +(raw["dataset%d/data3/what"%(a+1)]["gain"])*raw["dataset%d/data3/data"%(a+1)]
            #ZDR_angle=raw["dataset%d/data4/what"%(a+1)]["offset"] +(raw["dataset%d/data4/what"%(a+1)]["gain"])*raw["dataset%d/data4/data"%(a+1)]
            #KDP_angle=raw["dataset%d/data5/what"%(a+1)]["offset"] +(raw["dataset%d/data5/what"%(a+1)]["gain"])*raw["dataset%d/data5/data"%(a+1)]
            #PHIDP_angle=raw["dataset%d/data6/what"%(a+1)]["offset"] +(raw["dataset%d/data6/what"%(a+1)]["gain"])*raw["dataset%d/data6/data"%(a+1)]
            #RHOHV_angle=raw["dataset%d/data7/what"%(a+1)]["offset"] +(raw["dataset%d/data7/what"%(a+1)]["gain"])*raw["dataset%d/data7/data"%(a+1)]
            #WRAD_angle=raw["dataset%d/data8/what"%(a+1)]["offset"] +(raw["dataset%d/data8/what"%(a+1)]["gain"])*raw["dataset%d/data8/data"%(a+1)]
            #print(angle)
            #print(angle.shape)
            
            DBZH=numpy.append(DBZH,DBZH_angle).reshape(i+1,rays,bins)
            #RATE=numpy.append(RATE,RATE_angle).reshape(i+1,rays,bins)
            #VRAD=numpy.append(VRAD,VRAD_angle).reshape(i+1,rays,bins)
            #ZDR=numpy.append(ZDR,ZDR_angle).reshape(i+1,rays,bins)
            #KDP=numpy.append(KDP,KDP_angle).reshape(i+1,rays,bins)
            #PHIDP=numpy.append(PHIDP,PHIDP_angle).reshape(i+1,rays,bins)
            #RHOHV=numpy.append(RHOHV,RHOHV_angle).reshape(i+1,rays,bins)
            #WRAD=numpy.append(WRAD,WRAD_angle).reshape(i+1,rays,bins)
    
    #print(DBZH.shape)            
    #DBZH=numpy.reshape(all_files,rays,bins)   
    DBZH_av= numpy.average(DBZH, axis=0)
    #RATE_av= numpy.average(RATE, axis=0)
    #VRAD_av= numpy.average(VRAD, axis=0)
    #ZDR_av= numpy.average(ZDR, axis=0)
    #KDP_av= numpy.average(KDP, axis=0)
    #PHIDP_av= numpy.average(PHIDP, axis=0)
    #RHOHV_av= numpy.average(RHOHV, axis=0)
    #WRAD_av= numpy.average(WRAD, axis=0)
    #print(DBZH_clutter.shape)
    #print(DBZH)#[:,0,0:1])
    #print(DBZH_clutter)
    Clutter_DBZH=numpy.append(Clutter_DBZH,DBZH_av).reshape(a+1,rays,bins)
    #Clutter_RATE=numpy.append(Clutter_RATE,RATE_av).reshape(a+1,rays,bins)
    #Clutter_VRAD=numpy.append(Clutter_VRAD,VRAD_av).reshape(a+1,rays,bins)
    #Clutter_ZDR=numpy.append(Clutter_ZDR,ZDR_av).reshape(a+1,rays,bins)
    #Clutter_KDP=numpy.append(Clutter_KDP,KDP_av).reshape(a+1,rays,bins)
    #Clutter_PHIDP=numpy.append(Clutter_PHIDP,PHIDP_av).reshape(a+1,rays,bins)
    #Clutter_RHOHV=numpy.append(Clutter_RHOHV,RHOHV_av).reshape(a+1,rays,bins)
    #Clutter_WRAD=numpy.append(Clutter_WRAD,WRAD_av).reshape(a+1,rays,bins)
    
    """
    fig = pl.figure(figsize=(20,10))
    ax = fig.add_subplot(241)
    ax, pm = wradlib.vis.plot_ppi(DBZH_clutter,#[:,0:200], 
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
        
    xlabel = ax.set_xlabel('distancia [m]')
    ylabel = ax.set_ylabel('distancia [m]')
    title = ax.set_title('Reflectivity DBZH [dBz]')
    cb = pl.colorbar(pm, ax=ax)
    """

#Save the data to a file
with open("D:/Ground_clutter/Clutter_base/Clutter_30km_dbzh.txt", "w") as file:
    data = " ".join(Clutter_DBZH)
    file.write(data)
"""
#with open("D:/Ground_clutter/Clutter_base/Clutter_30km_rate.txt", "w") as file:
#    data2 = " ".join(Clutter_RATE)
#    file.write(data2)
#with open("D:/Ground_clutter/Clutter_base/Clutter_30km_vrad.txt", "w") as file:
#    data3 = " ".join(Clutter_VRAD)
#    file.write(data3)
#with open("D:/Ground_clutter/Clutter_base/Clutter_30km_zdr.txt", "w") as file:
#    data4 = " ".join(Clutter_ZDR)
#    file.write(data4)
#with open("D:/Ground_clutter/Clutter_base/Clutter_30km_kdp.txt", "w") as file:
#    data5 = " ".join(Clutter_KDP)
#    file.write(data5)
#with open("D:/Ground_clutter/Clutter_base/Clutter_30km_phidp.txt", "w") as file:
#    data6 = " ".join(Clutter_PHIDP)
#    file.write(data6)
#with open("D:/Ground_clutter/Clutter_base/Clutter_30km_rhohv.txt", "w") as file:
#    data7 = " ".join(Clutter_RHOHV)
#    file.write(data7)
#with open("D:/Ground_clutter/Clutter_base/Clutter_30km_wrad.txt", "w") as file:
#    data8 = " ".join(Clutter_WRAD)
#    file.write(data8)      
    
    clmap = wradlib.clutter.filter_gabella(angle,
                                           wsize=5,
                                           thrsnorain=0.,
                                           tr1=6.,
                                           n_p=8,
                                           tr2=1.3,
                                           radial=False,
                                           cartesian=False)
    
    ax = fig.add_subplot(122)
    ax, pm = wradlib.vis.plot_ppi(clmap[:,0:200], 
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

    xlabel = ax.set_xlabel('distancia [m]')
    ylabel = ax.set_ylabel('distancia [m]')
    title = ax.set_title('Cluttermap DBZH [dBz]')
    cb = pl.colorbar(pm, ax=ax)
    """
    