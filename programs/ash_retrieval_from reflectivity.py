# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 12:27:24 2022

@author: Eric Tellez

Ash retrieval

This code is written to calculate the concentration and rate of a volcanic explosion


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
import os
import glob
import warnings
warnings.filterwarnings('ignore')

"""
#To import files automatically
path= 'D:/explosiones/20220909_034300local/H5/**/*.h5'
list_of_files=glob.glob(path, recursive=True)
all_files=len(list_of_files)

for i in range (all_files):
    current_file=list_of_files[i]
    filename_path = wradlib.util.get_wradlib_data_file(current_file)
    raw = wradlib.io.read_opera_hdf5(filename_path)
     
    #To get the name of the file and paste it into the name of the plots
    filename = os.path.basename(filename_path) #Filename with extension
    file = os.path.splitext(filename)  #Tuple of string with filename and extension
"""

###################################
#Load H5 files 
#fpath = 'radar_data_examples/explosiones/20210917_054230/ODIM_H5/0087_20210917_054313.h5' # Remember that we already defined the main path
fpath = 'radar_data_examples/explosiones/20210917_054230/ODIM_H5/0087_20210917_054230.h5' # Remember that we already defined the main path
#fpath = 'radar_data_examples/explosiones/20210915_044742/ODIM_H5/0087_20210915_045031.h5' # Remember that we already defined the main path
f = wradlib.util.get_wradlib_data_file(fpath)
fcontent = wradlib.io.read_opera_hdf5(f)
###################################

#Three diameter of the ashes
fine_ash
    average_Dn=0.01 
coarse_ash
    average_Dn=0.1
lapilli
    average_Dn=1

standard_deviation_Dn=0.2

#three concentration regimes
light
    average_Ca=0.1
moderate
    average_Ca=1
intense
    average_Ca=5

standard_deviation_Ca=0.5

#ash density
rhoa=1

mu=0.5




Ca=3.21*10^(-5)*(rhoa/Dn^3)*
Ra=2.03*10^(-4)*((av*rhoa)/Dn^(3+bv))*



