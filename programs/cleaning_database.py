# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 13:45:35 2022

@author: Eric Téllez

Cleaning database

This program is to celan database because some files have one more column or row than the others
and because of that the calculations are a little bit harder. So far, the amount of this files is about 1/50

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
import glob
import numpy
from osgeo import osr
import warnings
warnings.filterwarnings('ignore')


# define your cartesian reference system
# For Mexico City: https://epsg.io/?q=Mexico
proj = osr.SpatialReference()
proj.ImportFromEPSG(6371)

#To import files automatically
path= 'D:/explosiones/20220909_061100local/H5/**/*.h5'
list_of_files=glob.glob(path, recursive=True)  #This is a list
all_files=len(list_of_files)
#print(all_files)

#dataset%d is the angle
#dataset/data%d/ is the physical variable

for a in range(1):  #number of elevation angles

    DBZH=numpy.array([]).reshape(-1,1,1)
    L=DBZH.shape 
   
    for i in range(all_files): #number of files
        current_file = list_of_files[i]
        filename_path = wradlib.util.get_wradlib_data_file(current_file)
        raw = wradlib.io.read_opera_hdf5(filename_path)
        
        rscale = raw['dataset%d/where' %(a+1)]['rscale'] #to obtain the conversion factor of the distance. It is the same for all the angles
    
        #nrays is x (rows), nbins is y (columns)
        rays = raw["dataset%d/where" % (a + 1)]["nrays"] #to obtain nbins, nrays, rscale, elangle
        bins = raw["dataset%d/where" % (a + 1)]["nbins"]
        #print(rays)
        #print(bins)
    
        if rays!=317: #or bins!=401:
            print(list_of_files[i])   #Name of the file different 