# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 01:40:49 2021

@author: Eric Tellez
This software is to obtain the ash concentration from the radar reflectivity
using the equations of Marzano and Vulpiani.
The program uses the CFRadial1 .nc data.


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
import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as pl
import numpy as np
import xarray as xr
try: 
    get_ipython().magic("matplotlib inline")
except:
    pl.ionn()

"""
#############################################
Load CFRadial1 Volume Data
Be sure to write the proper path of the files
Remember that the name of the files have the GMT hour, 5 or 6 hours later
of the hour in Altzomoni
fpath ='radar_data_examples/CFRadial/0087_20200626/0087_20200626_135500.nc' #Here goes the name of the file

"""

fpath ='radar_data_examples/CFRadial1/0087_20201206_211500.nc' #Here goes the name of the file
f = wrl.util.get_wradlib_data_file(fpath)
vol = wrl.io.open_cfradial1_dataset(f)

#Fix issues of CFRadial azimuth's
for i, swp in enumerate (vol):
    num_rays =int(360 // swp.azimuth.diff("azimuth").median())
    start_rays = swp.dims["azimuth"] - num_rays
    vol[i] = swp.isel(azimuth=slice(start_rays, start_rays + num_rays )).sortby("azimuth")  #This is the elevation angle

