# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 02:10:48 2022

@author: Eric Tellez

Maximum 2D distance of the reflectivity

This program calculate the maximum distance of the reflectivity in a 2D horizontal plane at constant angle

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

#def max_2D_distance

import wradlib
import numpy

"""
#nrays is x (rows), nbins is y (columns)
dataset# is the angle
dataset#/data# is the physical variable

data2 raw['dataset2/data2/what']['quantity']  is the horizontal reflectivity dBzH
"""

filename = wradlib.util.get_wradlib_data_file('D:/explosiones/20220909_034300local/H5/0087_20220909/0087_20220909_085000.h5')
raw = wradlib.io.read_opera_hdf5(filename)

#This is the conversion between 8 bits data (0-254) and reflectivity (0-100)
reflectivity=raw["dataset8/data2/what"]["offset"] +(raw["dataset8/data2/what"]["gain"])*raw['dataset8/data2/data']

rscale= raw['dataset9/where']['rscale']
elangle = raw['dataset9/how']['elangles']

# to find indices greater than some value
refl_index_matrix = []
for i in range(len(reflectivity)):
    for j in range(len(reflectivity[i])):
        if 27<= reflectivity[i][j] <= 38: #This value of the reflectivity is heuristic so far
            refl_index_matrix.append((i,j)) #This a list of indices

#max_radius_index is a matrix that contains two numbers
#the first one index [0] is the index of the pair of the maximum angle that fulfills 
#the condition of the maximum reflectivity
# and the second one index [1] is the index of the pair of the maximum radius that fulfills 
#the condition of the maximum reflectivity
#In this case we are only interested in the maximum radius.
max_radius_index=numpy.argmax(refl_index_matrix, axis=0) 
#print(max_radius_index) #matrix with two numbers
#print(refl_index_matrix[max_radius_index[1]]) #orderer pair of numbers 
#print(refl_index_matrix[max_radius_index[1]][0]) #one number

max_radius=numpy.amax(refl_index_matrix, axis=0)
#in this case the maximum value is the last index in the matrix
#print(max_radius)

max_distance=max_radius[1]*rscale*numpy.cos(elangle[0]*(numpy.pi)/180)
max_altitude=max_radius[1]*rscale*numpy.sin(elangle[0]*(numpy.pi)/180)
print("La distancia máxima de la pluma a este ángulo es", max_distance)
print("La altura máxima de la pluma sobre el nivel del mar a este ángulo es", max_altitude+4000)
print("La altura máxima de la pluma sobre el nivel del cráter a este ángulo es", max_altitude-1500)
#return