# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 18:26:11 2022

@author: Eric Tellez

Comparing point by point the values of all the variables that comes from the radar

This code is suited from the wradlib original to compare all the data that comes out 
from the Furuno radar.

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

# dataset# is angle and data# is physical variable

#import data
filename = wradlib.util.get_wradlib_data_file('radar_data_examples/Explosiones/20210915_044742/ODIM_H5/0087_20210915_045031.h5')
raw = wradlib.io.read_opera_hdf5(filename)

#data1 is not needed because that data is ranfall intensity (mm/h)
for i in range(8):  #This number has to change if the number of elevation angle changes
   
    RATE_rainfall_intensity=raw["dataset%d/data1/what" % (i + 3)]["offset"] +(raw["dataset%d/data1/what" % (i + 3)]["gain"])*raw["dataset%d/data1/data" % (i + 3)] #This dataset is not that important
    DBZH_horizontal_reflectivity=raw["dataset%d/data2/what" % (i + 3)]["offset"] +(raw["dataset%d/data2/what" % (i + 3)]["gain"])*raw["dataset%d/data2/data" % (i + 3)]
    VRAD_radial_velocity=raw["dataset%d/data3/what" % (i + 3)]["offset"] +(raw["dataset%d/data3/what" % (i + 3)]["gain"])*raw["dataset%d/data3/data"% (i + 3)]
    ZDR_reflection_factor_difference=raw["dataset%d/data4/what" % (i + 3)]["offset"] +(raw["dataset%d/data4/what" % (i + 3)]["gain"])*raw["dataset%d/data4/data" % (i + 3)]
    KDP_propagation_phase_difference_rate_of_change=raw["dataset%d/data5/what" % (i + 3)]["offset"] +(raw["dataset%d/data5/what" % (i + 3)]["gain"])*raw["dataset%d/data5/data" % (i + 3)]
    PHIDP_differential_propagation_phase=raw["dataset%d/data6/what" % (i + 3)]["offset"] +(raw["dataset%d/data6/what" % (i + 3)]["gain"])*raw["dataset%d/data6/data" % (i + 3)]
    RHOHV_copolar_correlation_coefficient=raw["dataset%d/data7/what" % (i + 3)]["offset"] +(raw["dataset%d/data7/what" % (i + 3)]["gain"])*raw["dataset%d/data7/data" % (i + 3)]
    WRAD_doppler_velocity_spectrum_width=raw["dataset%d/data8/what" % (i + 3)]["offset"] +(raw["dataset%d/data8/what" % (i + 3)]["gain"])*raw["dataset%d/data8/data" % (i + 3)]
    #raw['dataset4/data9/data'] #I dont know what this dataset means

    volume_DBZH=numpy.append((volume_DBZH,DBZH_horizontal_reflectivity), axis=0)

    volume_VRAD=numpy.append((VRAD_angle1,VRAD_angle2,VRAD_angle3,VRAD_angle4,VRAD_angle5,VRAD_angle6,VRAD_angle7,VRAD_angle8), axis=2)

    volume_ZDR=numpy.append((ZDR_angle1,ZDR_angle2,ZDR_angle3,ZDR_angle4,ZDR_angle5,ZDR_angle6,ZDR_angle7,ZDR_angle8), axis=2)

    volume_KDP=numpy.append((KDP_angle1,KDP_angle2,KDP_angle3,KDP_angle4,KDP_angle5,KDP_angle6,KDP_angle7,KDP_angle8), axis=2)

    #data6 is cross polarization difference phase phidp=phih-phiv
    #is dependent directly on particle concentration (at least in water) higher value higher particles

    volume_PHIDP=numpy.stack((PHIDP_angle1,PHIDP_angle2,PHIDP_angle3,PHIDP_angle4,PHIDP_angle5,PHIDP_angle6,PHIDP_angle7,PHIDP_angle8), axis=2)

    
    volume_RHOHV=numpy.stack((RHOHV_angle1,RHOHV_angle2,RHOHV_angle3,RHOHV_angle4,RHOHV_angle5,RHOHV_angle6,RHOHV_angle7,RHOHV_angle8), axis=2)

    volume_WRAD=numpy.stack((WRAD_angle1,WRAD_angle2,WRAD_angle3,WRAD_angle4,WRAD_angle5,WRAD_angle6,WRAD_angle7,WRAD_angle8), axis=2)

    # to find the indices that best describe the ash plume with all the variables together
plume_index_matrix = []
for i in range(len(volume_DBZH)):
    for j in range(len(volume_DBZH[i])):
        for k in range(len(volume_DBZH[i,j])):
            if volume_DBZH[i][j][k] >= 17: #This value for the reflectivity is heuristic so far
                if volume_VRAD[i][j][k] >= 64: #This value is heuristic
                    if -1 >= volume_ZDR[i][j][k] <= 1:
                        #if volume_KDP[i][j][k] >= :
                            if -0.5 >= volume_PHIDP[i][j][k] <= 0.5  :
                                if volume_RHOHV[i][j][k] >= :
                                    if volume_WRAD[i][j][k] >= :
                                        plume_index_matrix.append((i,j,k))