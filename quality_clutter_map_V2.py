# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 17:10:22 2022

@author: Eric Téllez

Quality clutter map version 2

This program is to generate a quality clutter map from data of clear sky days.

Most of this software is generated upon the Vulpiani et al 2012 paper named 
On the use of Dual-Polarized C-Band Radar por operational Rainfall retrieval in Mountainous Areas

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
import numpy
import matplotlib as pl
import warnings
warnings.filterwarnings('ignore')

#To import the file that has the emission that want to be analised
path= 'C:/Users/ERICK/Ground_Clutter/explosion/0087_20210914/0087_20210914_230000.h5'
filename = wradlib.util.get_wradlib_data_file(path)
raw = wradlib.io.read_opera_hdf5(filename)

#date and time is almost the same as the name of the archive
dateGMT = raw['what']['startdate']
timeGMT = raw['what']['starttime']

#Coordinates
sitecoords = (raw["where"]["lon"], 
              raw["where"]["lat"],
              raw["where"]["height"])

#CMAP Parameters
Weight_cmap=0.5
x1_cmap=10
x2_cmap=30
x3_cmap=70
x4_cmap=95 #Paper says infinity

#radial velocity Parameters
Weight_Vrad=0.3
x1_Vrad=-0.2
x2_Vrad=-0.1
x3_Vrad=0.1
x4_Vrad=0.2

#Texture of Zdr Parameters
Weight_TxZdr=0.4
x1_TxZdr=0.7
x2_TxZdr=1.0
x3_TxZdr=20.0 #Paper says infinity
x4_TxZdr=20.0 #Paper says infinity

#Texture of Rho Parameters
Weight_TxRho=0.4
x1_TxRho=0.1
x2_TxRho=0.15
x3_TxRho=1000 #Paper says infinity
x4_TxRho=1000 #Paper says infinity

#Texture of Phi Parameters
Weight_TxPhi=0.4
x1_TxPhi=15
x2_TxPhi=20
x3_TxPhi=1000 #Paper says infinity
x4_TxPhi=1000 #Paper says infinity

#open the clutter map of DBZH generated with static_clutter_map.py 
#This is .npy file of DBZH
CMAP_DBZH=numpy.load('C:/Users/ERICK/Ground_Clutter/Clutter_base/Clutter_30km_dbzh_test.npy')

Vrad=numpy.array([]).reshape(-1,1,1)
TxZdr=numpy.array([]).reshape(-1,1,1)
TxRho=numpy.array([]).reshape(-1,1,1)
TxPhi=numpy.array([]).reshape(-1,1,1)

Q2=numpy.array([]).reshape(-1,1,1)

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
    
    #radial_velocity
    Vrad_angle=raw["dataset%d/data3/what" % (i + 1)]["offset"] +(raw["dataset%d/data3/what" % (i + 1)]["gain"])*raw["dataset%d/data3/data"% (i + 1)]
    
    #texture of Zdr
    Zdr=raw["dataset%d/data4/what" % (i + 1)]["offset"] +(raw["dataset%d/data4/what" % (i + 1)]["gain"])*raw["dataset%d/data4/data" % (i + 1)]
    TxZdr_angle= wradlib.dp.texture(Zdr)
    
    #Texture of rhohv
    rhohv=raw["dataset%d/data7/what" % (i + 1)]["offset"] +(raw["dataset%d/data7/what" % (i + 1)]["gain"])*raw["dataset%d/data7/data" % (i + 1)]
    TxRho_angle= wradlib.dp.texture(rhohv)
    
    #Texture of phidp
    phidp=raw["dataset%d/data6/what" % (i + 1)]["offset"] +(raw["dataset%d/data6/what" % (i + 1)]["gain"])*raw["dataset%d/data6/data" % (i + 1)]
    TxPhi_angle= wradlib.dp.texture(phidp)  
    
    Vrad=numpy.append(Vrad,Vrad_angle).reshape(i+1,rays,bins)
    TxZdr=numpy.append(TxZdr,TxZdr_angle).reshape(i+1,rays,bins)
    TxPhi=numpy.append(TxPhi,TxPhi_angle).reshape(i+1,rays,bins)
    TxRho=numpy.append(TxRho,TxRho_angle).reshape(i+1,rays,bins)

    
    for j in range(CMAP_DBZH.shape[1]):
        for k in range(CMAP_DBZH.shape[2]):       

            if CMAP_DBZH[i,j,k]<x1_cmap or CMAP_DBZH[i,j,k]>x4_cmap:
                d_cmap=0
            elif x1_cmap < CMAP_DBZH[i,j,k] < x2_cmap:
                d_cmap=(CMAP_DBZH[i,j,k] - x1_cmap)/(x2_cmap - x1_cmap)
            elif x3_cmap < CMAP_DBZH[i,j,k] < x4_cmap:
                d_cmap=(x4_cmap - CMAP_DBZH[i,j,k])/(x4_cmap - x3_cmap)        
            elif x2_cmap < CMAP_DBZH[i,j,k] < x3_cmap:
                d_cmap=1
            
            if Vrad[i,j,k]<x1_Vrad or Vrad[i,j,k]>x4_Vrad:
                d_Vrad=0
            elif x1_Vrad < Vrad[i,j,k] < x2_Vrad:
                d_Vrad=(Vrad[i,j,k] - x1_Vrad)/(x2_Vrad - x1_Vrad)
            elif x3_Vrad < Vrad[i,j,k] < x4_Vrad:
                d_Vrad=(x4_Vrad - Vrad[i,j,k])/(x4_Vrad - x3_Vrad)        
            elif x2_Vrad < Vrad[i,j,k] < x3_Vrad:
                d_Vrad=1

            if TxZdr[i,j,k]<x1_TxZdr or TxZdr[i,j,k]>x4_TxZdr:
                d_TxZdr=0
            elif x1_TxZdr < TxZdr[i,j,k] < x2_TxZdr:
                d_TxZdr=(TxZdr[i,j,k] - x1_cmap)/(x2_TxZdr - x1_TxZdr)
            elif x3_TxZdr < TxZdr[i,j,k] < x4_TxZdr:
                d_TxZdr=(x4_cmap - TxZdr[i,j,k])/(x4_TxZdr - x3_TxZdr)        
            elif x2_TxZdr < TxZdr[i,j,k] < x3_TxZdr:
                d_TxZdr=1

            if TxRho[i,j,k]<x1_TxRho or TxRho[i,j,k]>x4_TxRho:
                d_TxRho=0
            elif x1_TxRho < TxRho[i,j,k] < x2_TxRho:
                d_TxRho=(TxRho[i,j,k] - x1_TxRho)/(x2_TxRho - x1_TxRho)
            elif x3_TxRho < TxRho[i,j,k] < x4_TxRho:
                d_TxRho=(x4_TxRho - TxRho[i,j,k])/(x4_TxRho - x3_TxRho)        
            elif x2_TxRho < TxRho[i,j,k] < x3_TxRho:
                d_TxRho=1
        
            if TxPhi[i,j,k]<x1_TxPhi or TxPhi[i,j,k]>x4_TxPhi:
                d_TxPhi=0
            elif x1_TxPhi < TxPhi[i,j,k] < x2_TxPhi:
                d_TxPhi=(TxPhi[i,j,k] - x1_cmap)/(x2_TxPhi - x1_TxPhi)
            elif x3_TxPhi < TxPhi[i,j,k] < x4_TxPhi:
                d_TxPhi=(x4_TxPhi - TxPhi[i,j,k])/(x4_TxPhi - x3_TxPhi)        
            elif x2_TxPhi < TxPhi[i,j,k] < x3_TxPhi:
                d_TxPhi=1

            q_cmap = 1-d_cmap
            q_Vrad = 1-d_Vrad 
            q_TxZdr = 1-d_TxZdr 
            q_TxRho = 1-d_TxRho
            q_TxPhi = 1-d_TxPhi
            
            Q2=(Weight_cmap*q_cmap+Weight_Vrad*q_Vrad+Weight_TxZdr*q_TxZdr+Weight_TxRho*q_TxRho+Weight_TxPhi*q_TxPhi)/(Weight_cmap+Weight_Vrad+Weight_TxZdr+Weight_TxRho+Weight_TxPhi) 
                  
            if Q2 < 0.5:
                Q2 =0

print(Q2.shape)

"""
To plot the Quality matrix
#plot the possible amount of rain
fig1= pl.figure(figsize=(10, 10))
ax, im = wradlib.vis.plot_ppi(Q[:,0:200], #The first coordinate is angle and the second is radius
                              #reflectivity,
                              rf= 1/rscale,
                              az= azimuth,
                              elev= elangle,
                              fig= fig1,
                              site= sitecoords,
                              #proj='cg', #Another type of projection
                              proj= proj, #Plot
                              ax=111,
                              func='pcolormesh')

#To plot the exact point over the crater with a dotted white line
axe, ima = wradlib.vis.plot_ppi_crosshair(site=sitecoords, 
                                          ranges=[12000],
                                          angles=[165],
                                          proj=None,
                                          elev=elangle,
                                          line=dict(color='white'),
                                          circle={'edgecolor': 'white'},
                                          )

xlabel = ax.set_xlabel('distancia [m]')
ylabel = ax.set_ylabel('distancia [m]')
title = ax.set_title('Fecha {} hora {} GMT \n Intensidad de lluvia [mm/h], Ángulo de elevación {}°'.format(dateGMT,timeGMT,elangle))
cb = pl.colorbar(im, ax=ax)

"""
