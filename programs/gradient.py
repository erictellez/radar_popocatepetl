# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 01:10:43 2021

@author: Eric Tellez
This software is to find the maximum altitude of each explosion


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
#def

import wradlib
import numpy
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as pl
from osgeo import osr
#from pde import  #partial differential equations module 
"""
#from scipy import optimize

results = dict() #to save all the minimums in a dictionary
results = 
"""
# define your cartesian reference system
# For Mexico City: https://epsg.io/?q=Mexico
proj = osr.SpatialReference()
proj.ImportFromEPSG(6371)


#filename = wradlib.util.get_wradlib_data_file('radar_data_examples/Explosiones/20210915_044742/ODIM_H5/0087_20210915_045031.h5')
filename = wradlib.util.get_wradlib_data_file('radar_data_examples/Explosiones/20200722_151800/0087_20200722_160000.h5')
raw = wradlib.io.read_opera_hdf5(filename)

reflectivity1=raw['dataset1/data2/data'] #angle 3.1
reflectivity2=raw['dataset2/data2/data'] #angle 4.5
reflectivity3=raw['dataset3/data2/data'] #angle 6.0
reflectivity4=raw['dataset4/data2/data'] #angle 8.2
reflectivity5=raw['dataset5/data2/data'] #angle 11.0
reflectivity6=raw['dataset6/data2/data'] #angle 14.0
reflectivity7=raw['dataset7/data2/data'] #angle 18.0
reflectivity8=raw['dataset8/data2/data'] #angle 28.0

#This matrix 
volume_reflectivity=numpy.stack((reflectivity1,
                                reflectivity2,
                                reflectivity3,
                                reflectivity4,
                                reflectivity5,
                                reflectivity6,
                                reflectivity7,
                                reflectivity8), axis=2)

#Coordinates
sitecoords = (raw["where"]["lon"], 
              raw["where"]["lat"],
              raw["where"]["height"])

azimuth = raw['dataset1/how']['startazA'] #to obtain all the azimuth angles
elangles = raw['dataset1/how']['elangles']
rscale= raw['dataset1/where']['rscale']

"""
#I have to place here the gradient of the data
The problem with the gradient is that we need to explore the gradient 
of all the data combined.

Maybe I have to built a 4D matrix with all the data


"""
#To get the maximum value
#maximum=spipy.optimize.maximize()

grad=numpy.gradient(reflectivity2)
grad_vol=numpy.gradient(volume_reflectivity)
#print(grad[0][0][0]) 
#polargrad=grad
#perhaps is better to calculate the laplacian

#numpy.max() #To find the maximum value
#numpy.argmax() #To find the indices of the maximum value


# to find indices greater than some value
refl_index_matrix = []
for i in range(len(volume_reflectivity)):
    for j in range(len(volume_reflectivity[i])):
        for k in range(len(volume_reflectivity[i][j])):
            if volume_reflectivity[i][j][k] >= 90: #This value of the reflectivity is heuristic so far
           #remember that this number, 90, is because the values are from 0 to 255 from Furuno raw data
                refl_index_matrix.append((i,j,k))

max_radius=numpy.amax(refl_index_matrix, axis=0)        
print(max_radius)
print(rscale)
max_distance=max_radius[1]*rscale
print(max_distance)
#To find the maximum index in this new list

#indice*rscale=distanciamaxima

#type(grad) #grad is list
#print(numpy.size(grad[0]))

#pl.plot(grad[0],grad[1])  #This plot is weird and I dont know what it means.
"""
fig0= pl.figure(figsize=(10, 10))
#Data plotted in contour format
im = wradlib.vis.plot_ppi(reflectivity1[:,0:200], #The first coordinate is angle and the second is radius
                          #reflectivity,
                          rf= 1/rscale,
                          az= azimuth,
                          elev= elangles,
                          fig= fig0,
                          site= sitecoords,
                          #proj='cg', #Another type of projection
                          proj= proj, #Plot
                          ax=111,
                          func='pcolormesh')

"""
#Contour function in direction 1 plotted in countour

#I need to plot the gradient with another plot, because is a vector field

fig1= pl.figure(figsize=(10, 10))
ax, im = wradlib.vis.plot_ppi(grad[0][:,0:200],
                          rf= 1/rscale,
                          az= azimuth,
                          elev= elangles,
                          fig= fig1,
                          site= sitecoords,
                          #proj='cg', #Another type of projection
                          proj= proj, #Plot
                          func='contour')

xlabel = ax.set_xlabel('distancia [m]')
ylabel = ax.set_ylabel('distancia [m]')
title = ax.set_title('Angular gradient of the reflectivity')
cb = pl.colorbar(im, ax=ax)

fig2= pl.figure(figsize=(10, 10))
#Gradient function in direction 2 plotted in contour
ax, im = wradlib.vis.plot_ppi(grad[1][:,0:200],
                          rf= 1/rscale,
                          az= azimuth,
                          elev= elangles,
                          fig= fig2,
                          site= sitecoords,
                          #proj='cg', #Another type of projection
                          proj= proj, #Plot
                          func='contour')

xlabel = ax.set_xlabel('distancia [m]')
ylabel = ax.set_ylabel('distancia [m]')
title = ax.set_title('Radial gradient of the reflectivity')
cb = pl.colorbar(im, ax=ax)

""" This plot is for volume-CAPPI
wradlib.vis.plot_max_plan_and_vert(trgx, 
                               trgy, 
                               trgz, 
                               vol, 
                               unit="Horizontal Reflectivity {0}".format(unit),
                               levels=range(17, 40), #This is the reflectivity scale
                               title='Vol-CAPPI: Radar {0}, {1}T{2}GMT {3}T{4}Altzomoni'.format(sensorname,dateGMT,timeGMT,date,time))
"""

