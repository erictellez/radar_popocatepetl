# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 14:36:47 2022

@author: Eric Tellez

This software is to clean the ground clutter in the last layer of the data, 28 degrees


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

filename = wradlib.util.get_wradlib_data_file('D:/explosiones/20220909_034300local/H5/0087_20220909/0087_20220909_085000.h5')
raw = wradlib.io.read_opera_hdf5(filename)

#dataset is the angle, data is the variable
#nrays is x (rows), nbins is y (columns)

#This is the conversion between 8 bits data (0-254) and reflectivity (0-100)
reflectivity=raw["dataset8/data2/what"]["offset"] +(raw["dataset8/data2/what"]["gain"])*raw['dataset8/data2/data']

rscale= raw['dataset9/where']['rscale']
elangle = raw['dataset9/how']['elangles']

# to find indices greater than some value
#the main noise of the reflectivity is from radius=bins=120 to 160
#the main noise of the reflectivity is from angle=rays=130 to 160


for i in range(len(reflectivity)):
    for j in range(len(reflectivity[i])):
        if 1<= reflectivity[i][j] <= 15: #If the value is in this region is problably noise in this particular angle
            reflectivity[i][j]==0
            


