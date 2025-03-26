# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 19:32:32 2022

@author: ERIC TELLEZ
Reading and visualizing an ODIM_H5 polar volume
The code is suited from the wradlib original to read the Furuno netCDF data

Specifically the reflectivity in the data dBz


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
from osgeo import osr
import glob
import os
import warnings
warnings.filterwarnings('ignore')
import matplotlib as pl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as colors
#import xarray as xr
#from shapely.errors import ShapelyDeprecationWarning
#from xmovie import Movie

tstart = dt.datetime.now()

#To import files automatically
#path= 'D:/explosion/H5/**/*.h5'
path='C:/Users/ERICK/Ground_Clutter/explosion/0087_20220907/*.h5'
list_of_files=glob.glob(path, recursive=True)
all_files=len(list_of_files)

#path_static_clutter='C:/Users/ERICK/Ground_Clutter/Clutter_base/Clutter_30km_ZDR_test.npy'
#Clutter = np.load(path_static_clutter)

#path_quality_matrix='C:/Users/ERICK/Ground_Clutter/Clutter_base/Q.npy'
#Q=np.load(path_quality_matrix)

"""
#Here I have to import the data to make the movie
# Load test dataset
ds = xr.tutorial.open_dataset('air_temperature').isel(time=slice(0, 150))
# Create movie object
mov = Movie(ds.air)
"""
    
# define your cartesian reference system
# For Mexico City: https://epsg.io/?q=Mexico
proj = osr.SpatialReference()
#proj.ImportFromEPSG(6371)
proj.ImportFromEPSG(32614)  #Review this, it seems that this is the good one to the zone 14Q

for a in range(all_files): #number of files

    current_file = list_of_files[a]
    filename_path = wrl.util.get_wradlib_data_file(current_file)
    raw = wrl.io.read_opera_hdf5(filename_path)
    
    #To get the name of the file and paste it into the name of the plots
    filename = os.path.basename(filename_path) #Filename with extension
    file = os.path.splitext(filename)  #Tuple of string with filename and extension   

    # this is the radar position tuple (longitude, latitude, altitude)
    sitecoords = (raw["where"]["lon"], 
                  raw["where"]["lat"],
                  raw["where"]["height"])

    # containers to hold Cartesian bin coordinates and data
    xyz, data = np.array([]).reshape((-1, 3)), np.array([])


    #date and time is almost the same as the name of the archive
    dateGMT = raw['what']['startdate']
    timeGMT = raw['what']['starttime']
    
    
    #CMAP Parameters
    Weight_cmap=0.5  #0.5 Vulpiani and Crisologo
    x1_cmap=10
    x2_cmap=30
    x3_cmap=70
    x4_cmap=95 #Paper says infinity
    
    #radial velocity Parameters
    Weight_Vrad=0.1  #0.3 Vulpiani, 0.1 Crisologo
    x1_Vrad=-0.2
    x2_Vrad=-0.1
    x3_Vrad=0.1
    x4_Vrad=0.2
    
    #Texture of Zdr Parameters
    Weight_TxZdr=0.4 #0.4 Vulpiani Crisologo
    x1_TxZdr=0.7
    x2_TxZdr=1.0
    x3_TxZdr=20.0 #Paper says infinity
    x4_TxZdr=20.0 #Paper says infinity
    
    #Texture of Rho Parameters
    Weight_TxRho=0.4  #0.4 Vulpiani Crisologo
    x1_TxRho=0.1
    x2_TxRho=0.15
    x3_TxRho=1000 #Paper says infinity
    x4_TxRho=1000 #Paper says infinity
    
    #Texture of Phi Parameters
    Weight_TxPhi=0.1   #0.4 Vulpiani, 0.1 Crisologo
    x1_TxPhi=15
    x2_TxPhi=20
    x3_TxPhi=1000 #Paper says infinity
    x4_TxPhi=1000 #Paper says infinity
        
    #Rho Parameters from Crisologo 
    Weight_Rho=0.4  #0.4 Crisologo
    x1_Rho=-1000  #Paper says minus infinity
    x2_Rho=-1000  #Paper says minus infinity
    x3_Rho=0.9 
    x4_Rho=0.95 
    """
    #So far is doing nothing
    #kdp Parameters from Tellez
    Weight_kdp=0.4
    x1_kdp=-2  #Paper says minus infinity
    x2_kdp=1  #Paper says minus infinity
    x3_kdp=3 
    x4_kdp=7 
    
    #kdp texture Parameters from Tellez
    Weight_Txkdp=0.4
    x1_Txkdp=-1000  #
    x2_Txkdp=-1000  #
    x3_Txkdp=0.9 
    x4_Txkdp=0.95 
    """
    
    #open the clutter map of DBZH generated with static_clutter_map.py 
    #This is .npy file of DBZH
    CMAP_DBZH=np.load('C:/Users/ERICK/Ground_Clutter/Clutter_base/Clutter_30km_dbzh_test.npy')

    #Q=np.zeros(CMAP_DBZH.shape)    
    
    Vrad=np.array([]).reshape(-1,1,1)
    TxZdr=np.array([]).reshape(-1,1,1)
    TxRho=np.array([]).reshape(-1,1,1)
    TxPhi=np.array([]).reshape(-1,1,1)
    Rho=np.array([]).reshape(-1,1,1)  #Crisologo
    Txkdp=np.array([]).reshape(-1,1,1) #Tellez
    
    Q=np.array([]).reshape(-1,1,1)
    #This equations are form the ground 
    #This for cycle is to calculate for each pixel in the 3D matrix of data
    for i in range(CMAP_DBZH.shape[0]):   
        
        #elevation angle (very important)
        elangle = raw['dataset%d/where' % (i + 1)]['elangle'] #to obtain the elevation angle
        azimuth = raw['dataset%d/how' % (i + 1)]['startazA'] #to obtain all the azimuth angles
        rscale= raw['dataset%d/where' % (i + 1)]['rscale'] #to obtain the conversion factor of the distance
        
        #nrays is x (rows), nbins is y (columns)
        rays = raw["dataset%d/where" % (i + 1)]["nrays"] #to obtain nbins, nrays, rscale, elangle
        bins = raw["dataset%d/where" % (i + 1)]["nbins"] 
        #print(rays)
        
        #radial_velocity
        Vrad_angle=raw["dataset%d/data3/what" % (i + 1)]["offset"] +(raw["dataset%d/data3/what" % (i + 1)]["gain"])*raw["dataset%d/data3/data"% (i + 1)]
        
        #texture of Zdr
        Zdr=raw["dataset%d/data4/what" % (i + 1)]["offset"] +(raw["dataset%d/data4/what" % (i + 1)]["gain"])*raw["dataset%d/data4/data" % (i + 1)]
        TxZdr_angle= wrl.dp.texture(Zdr)
        
        #Texture of rhohv
        rhohv=raw["dataset%d/data7/what" % (i + 1)]["offset"] +(raw["dataset%d/data7/what" % (i + 1)]["gain"])*raw["dataset%d/data7/data" % (i + 1)]
        TxRho_angle= wrl.dp.texture(rhohv)
        
        #Texture of phidp
        phidp=raw["dataset%d/data6/what" % (i + 1)]["offset"] +(raw["dataset%d/data6/what" % (i + 1)]["gain"])*raw["dataset%d/data6/data" % (i + 1)]
        TxPhi_angle= wrl.dp.texture(phidp)  
        
        #Texture of kdp, proposed by Tellez
        kdp=raw["dataset%d/data5/what"%(i + 1)]["offset"] +(raw["dataset%d/data5/what"%(i + 1)]["gain"])*raw["dataset%d/data5/data"%(i + 1)]
        Txkdp_angle = wrl.dp.texture(kdp)
        
        Vrad=np.append(Vrad,Vrad_angle).reshape(i+1,rays,bins)
        TxZdr=np.append(TxZdr,TxZdr_angle).reshape(i+1,rays,bins)
        TxPhi=np.append(TxPhi,TxPhi_angle).reshape(i+1,rays,bins)
        TxRho=np.append(TxRho,TxRho_angle).reshape(i+1,rays,bins)
        Txkdp=np.append(Txkdp,Txkdp_angle).reshape(i+1,rays,bins) #Tellez
        
        #Instruction to vectorize the if clause
        #condition1=CMAP_DBZH<x1_cmap or CMAP_DBZH>x4_cmap
        #dmap=np.where(condition1,CMAP_DBZH=0)
        
        for j in range(CMAP_DBZH.shape[1]):
            for k in range(CMAP_DBZH.shape[2]):       

                if CMAP_DBZH[i,j,k]<x1_cmap or CMAP_DBZH[i,j,k]>x4_cmap:
                    CMAP_DBZH[i,j,k]=0  #The original algorithm marks this as zero, I'm trying NaN to save time
                elif x1_cmap < CMAP_DBZH[i,j,k] < x2_cmap:
                    CMAP_DBZH[i,j,k]=(CMAP_DBZH[i,j,k] - x1_cmap)/(x2_cmap - x1_cmap)
                elif x3_cmap < CMAP_DBZH[i,j,k] < x4_cmap:
                    CMAP_DBZH[i,j,k]=(x4_cmap - CMAP_DBZH[i,j,k])/(x4_cmap - x3_cmap)        
                elif x2_cmap < CMAP_DBZH[i,j,k] < x3_cmap:
                    CMAP_DBZH[i,j,k]=1
            
                if Vrad[i,j,k]<x1_Vrad or Vrad[i,j,k]>x4_Vrad:
                    Vrad[i,j,k]=0
                elif x1_Vrad < Vrad[i,j,k] < x2_Vrad:
                    Vrad[i,j,k]=(Vrad[i,j,k] - x1_Vrad)/(x2_Vrad - x1_Vrad)
                elif x3_Vrad < Vrad[i,j,k] < x4_Vrad:
                    Vrad[i,j,k]=(x4_Vrad - Vrad[i,j,k])/(x4_Vrad - x3_Vrad)       
                elif x2_Vrad < Vrad[i,j,k] < x3_Vrad:
                    Vrad[i,j,k]=1

                if TxZdr[i,j,k]<x1_TxZdr or TxZdr[i,j,k]>x4_TxZdr:
                    TxZdr[i,j,k]=0
                elif x1_TxZdr < TxZdr[i,j,k] < x2_TxZdr:
                    TxZdr[i,j,k]=(TxZdr[i,j,k] - x1_cmap)/(x2_TxZdr - x1_TxZdr)
                elif x3_TxZdr < TxZdr[i,j,k] < x4_TxZdr:
                    TxZdr[i,j,k]=(x4_cmap - TxZdr[i,j,k])/(x4_TxZdr - x3_TxZdr)        
                elif x2_TxZdr < TxZdr[i,j,k] < x3_TxZdr:
                    TxZdr[i,j,k]=1

                if TxRho[i,j,k]<x1_TxRho or TxRho[i,j,k]>x4_TxRho:
                    TxRho[i,j,k]=0
                elif x1_TxRho < TxRho[i,j,k] < x2_TxRho:
                    TxRho[i,j,k]=(TxRho[i,j,k] - x1_TxRho)/(x2_TxRho - x1_TxRho)
                elif x3_TxRho < TxRho[i,j,k] < x4_TxRho:
                    TxRho[i,j,k]=(x4_TxRho - TxRho[i,j,k])/(x4_TxRho - x3_TxRho)        
                elif x2_TxRho < TxRho[i,j,k] < x3_TxRho:
                    TxRho[i,j,k]=1
        
                if TxPhi[i,j,k]<x1_TxPhi or TxPhi[i,j,k]>x4_TxPhi:
                    TxPhi[i,j,k]=0
                elif x1_TxPhi < TxPhi[i,j,k] < x2_TxPhi:
                    TxPhi[i,j,k]=(TxPhi[i,j,k] - x1_cmap)/(x2_TxPhi - x1_TxPhi)
                elif x3_TxPhi < TxPhi[i,j,k] < x4_TxPhi:
                    TxPhi[i,j,k]=(x4_TxPhi - TxPhi[i,j,k])/(x4_TxPhi - x3_TxPhi)        
                elif x2_TxPhi < TxPhi[i,j,k] < x3_TxPhi:
                    TxPhi[i,j,k]=1
                   
                #This section is because the paper of Crisologo
                if rhohv[j,k]<x1_Rho or rhohv[j,k]>x4_Rho:
                    rhohv[j,k]=0
                elif x1_Rho < rhohv[j,k] < x2_Rho:
                    rhohv[j,k]=(rhohv[j,k] - x1_Rho)/(x2_Rho - x1_Rho)
                elif x3_Rho < rhohv[j,k] < x4_Rho:
                    rhohv[j,k]=(x4_Rho - rhohv[j,k])/(x4_Rho - x3_Rho)        
                elif x2_Rho < rhohv[j,k] < x3_Rho:
                    rhohv[j,k]=1
                    
                """
                #This section is because I want
                if kdp[j,k]<x1_kdp or kdp[j,k]>x4_kdp:
                    kdp[j,k]=0
                elif x1_kdp < kdp[j,k] < x2_kdp:
                    kdp[j,k]=(kdp[j,k] - x1_kdp)/(x2_kdp - x1_kdp)
                elif x3_kdp < kdp[j,k] < x4_kdp:
                    kdp[j,k]=(x4_kdp - kdp[j,k])/(x4_kdp - x3_kdp)        
                elif x2_kdp < kdp[j,k] < x3_kdp:
                    kdp[j,k]=1
        
                
                #This section is because I want
                if Txkdp[i,j,k]<x1_Txkdp or Txkdp[i,j,k]>x4_Txkdp:
                    Txkdp[i,j,k]=0
                elif x1_Txkdp < Txkdp[i,j,k] < x2_Txkdp:
                    Txkdp[i,j,k]=(Txkdp[i,j,k] - x1_Txkdp)/(x2_Txkdp - x1_Txkdp)
                elif x3_Txkdp < Txkdp[i,j,k] < x4_Txkdp:
                    Txkdp[i,j,k]=(x4_Txkdp - Txkdp[i,j,k])/(x4_Txkdp - x3_Txkdp)        
                elif x2_Txkdp < Txkdp[i,j,k] < x3_Txkdp:
                    Txkdp[i,j,k]=1
                """

        q_cmap = 1-CMAP_DBZH[i]
        q_Vrad = 1-Vrad[i]
        q_TxZdr = 1-TxZdr[i]
        q_TxRho = 1-TxRho[i]
        q_TxPhi = 1-TxPhi[i]
        q_Rho = 1- rhohv #Crisologo
        q_Txkdp=1    #Tellez
        q_kdp=1-kdp  #Tellez
        
        q_Vrad = q_Vrad[:CMAP_DBZH.shape[1],:CMAP_DBZH.shape[2]]
        q_TxZdr = q_TxZdr[:CMAP_DBZH.shape[1],:CMAP_DBZH.shape[2]]
        q_TxRho = q_TxRho[:CMAP_DBZH.shape[1],:CMAP_DBZH.shape[2]]
        q_TxPhi = q_TxPhi[:CMAP_DBZH.shape[1],:CMAP_DBZH.shape[2]]
        q_Rho = q_Rho[:CMAP_DBZH.shape[1],:CMAP_DBZH.shape[2]]  #Crisologo
        q_kdp = q_Rho[:CMAP_DBZH.shape[1],:CMAP_DBZH.shape[2]] #Tellez
        q_Txkdp = q_Rho[:CMAP_DBZH.shape[1],:CMAP_DBZH.shape[2]] #Tellez
        
        """
        #Vulpiani 2012
        Q=(Weight_cmap*q_cmap
           + Weight_Vrad*q_Vrad 
           + Weight_TxZdr*q_TxZdr 
           + Weight_TxRho*q_TxRho 
           + Weight_TxPhi*q_TxPhi)/(Weight_cmap 
                                    + Weight_Vrad 
                                    + Weight_TxZdr 
                                    + Weight_TxRho 
                                    + Weight_TxPhi) 
        
        """                           
        #Crisologo function 2014
        Q=(Weight_cmap*q_cmap
        + Weight_Vrad*q_Vrad 
        + Weight_TxZdr*q_TxZdr 
        + Weight_TxRho*q_TxRho 
        + Weight_TxPhi*q_TxPhi
        + Weight_Rho*q_Rho)/(Weight_cmap 
                             + Weight_Vrad 
                             + Weight_TxZdr 
                             + Weight_TxRho 
                             + Weight_TxPhi
                             + Weight_Rho) #Crisologo 2014

        """
        #Tellez function
        Q=(Weight_cmap*q_cmap
        + Weight_Vrad*q_Vrad 
        + Weight_TxZdr*q_TxZdr 
        + Weight_TxRho*q_TxRho 
        + Weight_TxPhi*q_TxPhi
        + Weight_Rho*q_Rho
        + Weight_Txkdp*q_Txkdp
        + Weight_kdp*q_kdp)/(Weight_cmap 
                             + Weight_Vrad 
                             + Weight_TxZdr 
                             + Weight_TxRho 
                             + Weight_TxPhi
                             + Weight_Rho     
                             + Weight_Txkdp
                             + Weight_kdp)
        
       
    #nrays is x (rows), nbins is y (columns)
    dataset# is the angle
    dataset#/data# is the physical variable   
    data2 raw['dataset2/data2/what']['quantity']  is the horizontal reflectivity dBzH
    """    

    how = raw['dataset1/how']['startazA'] #to obtain all the azimuth angles
    maxaz = len(how) #It gives the lenght of the array
    sector = abs(int(how[maxaz-1]-how[0]))+1  #Angle size of the scanned sector
    #how[0] is the first angle of the measurement

    #This for is to change of elevation angle without touching the code, but is not finished yet.
    #for angle in range(10):
    #    where = raw["dataset%d/where" % (angle+1)] #to obtain nbins, nrays, rscale, elangle 
    
    # iterate over the elevation angles 
    for i in range(2,10):
        # get the scan metadata for each elevation 
        where = raw["dataset%d/where" % (i+1)] #to obtain nbins, nrays, rscale, elangle
        what = raw["dataset%d/data2/what" % (i+1)] # to obtain the gain and the offset
      
        #nrays is x (rows), nbins is y (columns)
        rays=where["nrays"]
        bins=401#where["nbins"] #This number has to be the maximum of the Q matrix
        
        if sector==359: #this line is to 360 sectors. Sector starts in 0 and ends in 359
            az = np.arange(0., 359., 360/where["nrays"]) #this line is to 360 sectors
        elif sector<359:
            az = np.arange(0., 360., sector/where["nrays"]) #This line is to sectors smaller than 360, ie the ones that are produced by sppi scans
            
        # rstart is given in km, so multiply by 1000.
        rstart = where["rstart"] * 1000.
        r = np.arange(rstart,
                      rstart + bins * where["rscale"],
                      where["rscale"])
        
        # derive 3-D Cartesian coordinate tuples
        xyz_ = wrl.vpr.volcoords_from_polar(sitecoords, 
                                            where["elangle"],
                                            az, 
                                            r, 
                                            proj)
            
        #Creating an array of invalid data (values=255) or zeros to complete the circular sector
        #Value of 255 rise a problem in the edges of the circular sector.
        #nodata=np.ones(int(rays*((360/sector)-1))*bins)*255
        nodata=np.zeros(int(rays*((360/sector)-1))*bins)
        nodata=np.reshape(nodata, (int(rays*((360/(sector)-1))),bins))
            
        # get the scan data for this elevation
        #   here, you can do all the processing on the 2-D polar level
        #   e.g. clutter elimination, attenuation correction, ...
        #data_ = what["offset"] + (what["gain"])* raw[
        #    "dataset%d/data2/data" % (i + 1)] 
            
        """
        data_ =  what["offset"] +(what["gain"])*raw[
            "dataset%d/data2/data" % (i + 1)] 
            data_=np.append(data_,nodata).reshape((int(rays*(360/sector)),bins))
            """
            
            #Sometimes the data has different number of rows or columns. This statement is to correct that.
            #if raw["dataset%d/data2/data"%(i+1)] == rawclutter["dataset%d/data2/data"%(i+1)]
            #diffrows = raw["dataset%d/data2/data"%(i+1)][:2] - rawclutter["dataset%d/data2/data"%(i+1)]
            #diffcolumns = raw["dataset%d/data2/data"%(i+1)] - rawclutter["dataset%d/data2/data"%(i+1)]
            #columnsextra = np.zeros() 
       
        
        #This is the conversion between 8 bits data (0-254) and reflectivity (0-100)
        data_ = what["offset"] +(what["gain"])*(raw[
                "dataset%d/data2/data" % (i + 1)])
       
        #This code is to add the zero columns missing because the vol-cappi only plots 360 and in this case we have a 30º sector
        data_=np.append(data_[:CMAP_DBZH.shape[1],:CMAP_DBZH.shape[2]],nodata).reshape((int(rays*(360/sector)),bins))
       
        data_[data_ == -32]=np.nan
        data_[data_ == 95.5]=np.nan
        data_[Q < 0.55] = np.nan  #In the paper of Vulpiani they chose 0.5, I chose 0.65 in the first approach. 0.55 functions better for Crisologo
                

        """
            The next function is written based on 
            Gianfranco Vulpiani, Mario Montopoli, Luca Delli Passeri, Antonio G. Gioia, Pietro Giordano, and Frank S. Marzano. 
            On the use of dual-polarized c-band radar for operational rainfall retrieval in mountainous areas. 
            Journal of Applied Meteorology and Climatology, 51(2):405–425, Feb 2012. 
            doi:10.1175/JAMC-D-10-05024.1.         
                        
            wradlib.clutter.classify_echo_fuzzy(dat, weights=None, trpz=None, thresh=0.5)
            """    
                        
        # make sure the data is aligned to zero azimuth == due north
        # get azimuth of first ray
        zero_az = int(rays*how[0]/sector)
        # realign azimuth array to have 0 deg as first ray
        data_ = np.roll(data_, zero_az, axis=0)
            
        # transfer to containers
        xyz, data = np.vstack((xyz, xyz_)), np.append(data, data_.ravel())
            

    # generate 3-D Cartesian target grid coordinates
    maxrange = rstart + bins * where["rscale"] #This range is diameter. For Popo=35000 Furuno max range is 70000 in radius
    minelev = 3.1     #minimum elevation angle set up by scan strategy
    maxelev = 28.     #maximum elevation angle set up by scan strategy
    minalt = 4000.    #minimum altitude maxrange*sin(minelev)
    maxalt = 10000.   #altitude (Good number = 10000)
    horiz_res = 150. #This resolution is in meters (Good number = 100)
    vert_res = 100.   #This resolution is in meters (Good number = 50)
    
    #trgxyz are the coordinates
    #trgshape is the size of the 3D matrix
    trgxyz, trgshape = wrl.vpr.make_3d_grid(sitecoords, 
                                            proj, 
                                            maxrange,
                                            maxalt, 
                                            horiz_res, 
                                            vert_res, 
                                            minalt) #Here you can set up the altitude of the radar or the border of the crater
    
    # interpolate to Cartesian 3-D volume grid
    gridder = wrl.vpr.CAPPI(xyz, 
                            trgxyz, 
                            trgshape, 
                            maxrange, 
                            minelev,
                            maxelev,
                            ipclass=wrl.ipol.Idw) #For interpolation
    
    data3d=gridder(data).reshape(trgshape)     
    vol = np.ma.masked_invalid(gridder(data).reshape(trgshape))
    # Save the array to a text file in format .npy
    np.save('C:/Users/ERICK/Ground_Clutter/data_explosion/data_woc_{0}.npy'.format(file[0]), data3d) 
    #wrl.vpr.norm_vpr_stats(vol,)   #To visualize some statistics
    
    
    unit = raw['dataset2/data2/what']['quantity'].decode('UTF-8') #the units of the plot
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
    sensorname = raw['what']['source'].decode('UTF-8')
    
    # diagnostic plot
    trgx = trgxyz[:, 0].reshape(trgshape)[0, 0, :]
    trgy = trgxyz[:, 1].reshape(trgshape)[0, :, 0]
    trgz = trgxyz[:, 2].reshape(trgshape)[:, 0, 0]
    
    """
    wrl.vis.plot_max_plan_and_vert(trgx, 
                                   trgy, 
                                   trgz, 
                                   vol, 
                                   unit="Horizontal Reflectivity {0}".format(unit),
                                   levels=range(0, 95), #This is the reflectivity scale
                                   #levels=range(0, 100),
                                   title='{0} {1} local, {2} {3} GMT'.format(date,time,dateGMT,timeGMT), #title in the graph
                                   #saveto='D:/Carpeta_Imag/VCAPPI/VCAPPI_{0}'.format(file[0])) #name of the file
                                   )
    """ 
    
    #This function is to plot not just the maximum reflectivity but in a sagital section
    wrl.vis.plot_plan_and_vert(trgx, 
                               trgy, 
                               trgz, 
                               #np.max(vol, axis=-3),
                               #np.max(vol, axis=-2),
                               #np.max(vol, axis=-1),
                               vol[10,:,:],    #(min ) (best ) (max )
                               vol[:,113,:],  #(min 105) (best 113) (max 122) #The projection in y with the sagital section over the crater of the volcano
                               vol[:,:,214],  #The explosion appears first in 204 and 205 five minutos before the big signal #(min 204) (best 214) (max 224) #The projection in x with the sagital section over the crater of the volcano
                               unit="Horizontal Reflectivity {0}".format(unit),
                               levels=range(0, 95), #This is the reflectivity scale
                               #levels=range(0, 95), #Maximum 95
                               title='{0} {1} local, {2} {3} GMT'.format(date,time,dateGMT,timeGMT)) #title in the graph
                               #saveto='C:/Users/radar1/Desktop/20220909_070000/plots/VCAPPI_{0}'.format(file[0])) #name of the file
        

    print("3-D interpolation took:", dt.datetime.now() - tstart)

#np.savez is to save several arrays in one file.