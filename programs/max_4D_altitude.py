# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 23:41:47 2022

@author: Eric Tellez

Maximum altitude in a real-time explosion.


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
import xarray as xr
from shapely.errors import ShapelyDeprecationWarning
from xmovie import Movie


# dataset# is angle and data# is physical variable

#import data
filename = wradlib.util.get_wradlib_data_file('radar_data_examples/Explosiones/20210915_044742/ODIM_H5/0087_20210915_045031.h5')
raw = wradlib.io.read_opera_hdf5(filename)
angle1 = raw["dataset1/data2/what"]["offset"] +(raw["dataset1/data2/what"]["gain"])*raw["dataset1/data2/data"]
angle2 = raw["dataset2/data2/what"]["offset"] +(raw["dataset2/data2/what"]["gain"])*raw["dataset2/data2/data"]
angle3 = raw["dataset3/data2/what"]["offset"] +(raw["dataset3/data2/what"]["gain"])*raw["dataset3/data2/data"]
angle4 = raw["dataset4/data2/what"]["offset"] +(raw["dataset4/data2/what"]["gain"])*raw["dataset4/data2/data"]
angle5 = raw["dataset5/data2/what"]["offset"] +(raw["dataset5/data2/what"]["gain"])*raw["dataset5/data2/data"]
angle6 = raw["dataset6/data2/what"]["offset"] +(raw["dataset6/data2/what"]["gain"])*raw["dataset6/data2/data"]
angle7 = raw["dataset7/data2/what"]["offset"] +(raw["dataset7/data2/what"]["gain"])*raw["dataset7/data2/data"]
angle8 = raw["dataset8/data2/what"]["offset"] +(raw["dataset8/data2/what"]["gain"])*raw["dataset8/data2/data"]

volume_reflectivity1=numpy.stack((angle1,angle2,angle3,angle4,angle5,angle6,angle7,angle8), axis=2)

filename = wradlib.util.get_wradlib_data_file('radar_data_examples/Explosiones/20210915_044742/ODIM_H5/0087_20210915_045031.h5')
raw = wradlib.io.read_opera_hdf5(filename)
angle1 = raw["dataset1/data2/what"]["offset"] +(raw["dataset1/data2/what"]["gain"])*raw["dataset1/data2/data"]
angle2 = raw["dataset2/data2/what"]["offset"] +(raw["dataset1/data2/what"]["gain"])*raw["dataset2/data2/data"]
angle3 = raw["dataset3/data2/what"]["offset"] +(raw["dataset1/data2/what"]["gain"])*raw["dataset3/data2/data"]
angle4 = raw["dataset4/data2/what"]["offset"] +(raw["dataset1/data2/what"]["gain"])*raw["dataset4/data2/data"]
angle5 = raw["dataset5/data2/what"]["offset"] +(raw["dataset1/data2/what"]["gain"])*raw["dataset5/data2/data"]
angle6 = raw["dataset6/data2/what"]["offset"] +(raw["dataset1/data2/what"]["gain"])*raw["dataset6/data2/data"]
angle7 = raw["dataset7/data2/what"]["offset"] +(raw["dataset1/data2/what"]["gain"])*raw["dataset7/data2/data"]
angle8 = raw["dataset8/data2/what"]["offset"] +(raw["dataset1/data2/what"]["gain"])*raw["dataset8/data2/data"]

volume_reflectivity2=numpy.stack((angle1,angle2,angle3,angle4,angle5,angle6,angle7,angle8), axis=2)

filename = wradlib.util.get_wradlib_data_file('radar_data_examples/Explosiones/20210915_044742/ODIM_H5/0087_20210915_045031.h5')
raw = wradlib.io.read_opera_hdf5(filename)
angle1 = raw["dataset1/data2/what"]["offset"] +(raw["dataset1/data2/what"]["gain"])*raw["dataset1/data2/data"]
angle2 = raw["dataset2/data2/what"]["offset"] +(raw["dataset1/data2/what"]["gain"])*raw["dataset2/data2/data"]
angle3 = raw["dataset3/data2/what"]["offset"] +(raw["dataset1/data2/what"]["gain"])*raw["dataset3/data2/data"]
angle4 = raw["dataset4/data2/what"]["offset"] +(raw["dataset1/data2/what"]["gain"])*raw["dataset4/data2/data"]
angle5 = raw["dataset5/data2/what"]["offset"] +(raw["dataset1/data2/what"]["gain"])*raw["dataset5/data2/data"]
angle6 = raw["dataset6/data2/what"]["offset"] +(raw["dataset1/data2/what"]["gain"])*raw["dataset6/data2/data"]
angle7 = raw["dataset7/data2/what"]["offset"] +(raw["dataset1/data2/what"]["gain"])*raw["dataset7/data2/data"]
angle8 = raw["dataset8/data2/what"]["offset"] +(raw["dataset1/data2/what"]["gain"])*raw["dataset8/data2/data"]

volume_reflectivity3=numpy.stack((angle1,angle2,angle3,angle4,angle5,angle6,angle7,angle8), axis=2)

filename = wradlib.util.get_wradlib_data_file('radar_data_examples/Explosiones/20210915_044742/ODIM_H5/0087_20210915_045031.h5')
raw = wradlib.io.read_opera_hdf5(filename)
angle1 = raw["dataset1/data2/what"]["offset"] +(raw["dataset1/data2/what"]["gain"])*raw["dataset1/data2/data"]
angle2 = raw["dataset2/data2/what"]["offset"] +(raw["dataset1/data2/what"]["gain"])*raw["dataset2/data2/data"]
angle3 = raw["dataset3/data2/what"]["offset"] +(raw["dataset1/data2/what"]["gain"])*raw["dataset3/data2/data"]
angle4 = raw["dataset4/data2/what"]["offset"] +(raw["dataset1/data2/what"]["gain"])*raw["dataset4/data2/data"]
angle5 = raw["dataset5/data2/what"]["offset"] +(raw["dataset1/data2/what"]["gain"])*raw["dataset5/data2/data"]
angle6 = raw["dataset6/data2/what"]["offset"] +(raw["dataset1/data2/what"]["gain"])*raw["dataset6/data2/data"]
angle7 = raw["dataset7/data2/what"]["offset"] +(raw["dataset1/data2/what"]["gain"])*raw["dataset7/data2/data"]
angle8 = raw["dataset8/data2/what"]["offset"] +(raw["dataset1/data2/what"]["gain"])*raw["dataset8/data2/data"]

volume_reflectivity4=numpy.stack((angle1,angle2,angle3,angle4,angle5,angle6,angle7,angle8), axis=2)

filename = wradlib.util.get_wradlib_data_file('radar_data_examples/Explosiones/20210915_044742/ODIM_H5/0087_20210915_045031.h5')
raw = wradlib.io.read_opera_hdf5(filename)
angle1 = raw["dataset1/data2/what"]["offset"] +(raw["dataset1/data2/what"]["gain"])*raw["dataset1/data2/data"]
angle2 = raw["dataset2/data2/what"]["offset"] +(raw["dataset1/data2/what"]["gain"])*raw["dataset2/data2/data"]
angle3 = raw["dataset3/data2/what"]["offset"] +(raw["dataset1/data2/what"]["gain"])*raw["dataset3/data2/data"]
angle4 = raw["dataset4/data2/what"]["offset"] +(raw["dataset1/data2/what"]["gain"])*raw["dataset4/data2/data"]
angle5 = raw["dataset5/data2/what"]["offset"] +(raw["dataset1/data2/what"]["gain"])*raw["dataset5/data2/data"]
angle6 = raw["dataset6/data2/what"]["offset"] +(raw["dataset1/data2/what"]["gain"])*raw["dataset6/data2/data"]
angle7 = raw["dataset7/data2/what"]["offset"] +(raw["dataset1/data2/what"]["gain"])*raw["dataset7/data2/data"]
angle8 = raw["dataset8/data2/what"]["offset"] +(raw["dataset1/data2/what"]["gain"])*raw["dataset8/data2/data"]

volume_reflectivity5=numpy.stack((angle1,angle2,angle3,angle4,angle5,angle6,angle7,angle8), axis=2)

hypervolume_reflectivity=numpy.dstack((volume_reflectivity1,volume_reflectivity2,volume_reflectivity3,volume_reflectivity4,volume_reflectivity1))

#azimuth = raw['dataset1/how']['startazA'] #to obtain all the azimuth angles
#elangles = raw['dataset1/how']['elangles'] #Elevation angles
rscale= raw['dataset1/where']['rscale'] #

dateGMT = raw['what']['startdate']
timeGMT = raw['what']['starttime']
date = raw['what']['Local_date']
time = raw['what']['Local_time']

"""
#I have to place here the gradient of the data
The problem with the gradient is that we need to explore the gradient 
of all the data combined.

Maybe I have to built a 4D matrix with all the data
"""
#To get the maximum value
#maximum=spipy.optimize.maximize()

grad=numpy.gradient(volume_reflectivity1)
#polargrad=grad
#perhaps is better to calculate the laplacian

#numpy.max() #To find the maximun value
#numpy.argmax() #To find the indices of the maximum value

# to find indices greater than some value
refl_index_matrix = []
for i in range(len(hypervolume_reflectivity)):
    for j in range(len(hypervolume_reflectivity[i])):
        for k in range(len(hypervolume_reflectivity[i,j])):
            for l in range(len(hypervolume_reflectivity[i,j,k])):
                if hypervolume_reflectivity1[i][j][k][l] >= 17: #This value of the reflectivity is heuristic so far
                    refl_index_matrix.append((i,j,k,l))

max_index=numpy.amax(refl_index_matrix, axis=0)        
#print(max_index) #maximum of each dimension
print(max_index[2]) 
volume_reflectivity[:,:,max_index[2]]

# to find the indices of the maximum distance in the highest angle
refl_index_highest_angle = []
for i in range(len(volume_reflectivity[:,:,max_index[2]])):
    for j in range(len(volume_reflectivity[i,:,max_index[2]])):
        if volume_reflectivity[i][j][max_index[2]] >= 102: #This value of the reflectivity is heuristic so far
        #remember that this number, 90, is because the values are from 0 to 255 from Furuno raw data
            refl_index_highest_angle.append((i,j,max_index[2])) #This a matrix of indices

#print(refl_index_highest_angle)
max_radius=numpy.max(refl_index_highest_angle, axis=0) #return the maximum value along axis 0 is the radius       
#in this case the maximum value is the last index in the matrix
print(max_radius)
max_distance=max_radius[1]*rscale
print(max_distance)

#The elevation is in spherical coordinates
elangle=raw['dataset%d/how' % (max_index[2])]['elangles'] #Elevation angles in degrees
elangle_rad=elangle[0]*numpy.pi/180
altitude_max=max_radius[1]*rscale*numpy.sin(elangle_rad)

print("La altura de la columna sobre el nivel del mar es", altitude_max+4000)
print("La altura de la columna sobre el cráter es", altitude_max-1500)

