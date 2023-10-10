# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 13:31:36 2022

@author: Eric Tellez

Maximum altitude in a static frame explosion

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

# dataset# is angle and data# is physical variable

#import data
#filename = wradlib.util.get_wradlib_data_file('radar_data_examples/Explosiones/20210915_044742/ODIM_H5/0087_20210915_045403.h5')
filename = wradlib.util.get_wradlib_data_file('radar_data_examples/Explosiones/20200722_151800/0087_20200722_150000.h5')
raw = wradlib.io.read_opera_hdf5(filename)
#print(raw.keys())
"""
#nrays is x (rows) , nbins is y (columns)
dataset# is the angle
dataset#/data# is the physical variable

data2 raw['dataset2/data2/what']['quantity']  is the horizontal reflectivity dBzH

(rows, columns, depths)
(angles, radius, altitude)
"""


#rawclutter is the file without the explosion
#The more data the better
filenameclutter = wradlib.util.get_wradlib_data_file('radar_data_examples/Explosiones/20200722_151800/0087_20200722_140000.h5') 
rawclutter1 = wradlib.io.read_opera_hdf5(filenameclutter)
filenameclutter2 =wradlib.util.get_wradlib_data_file('radar_data_examples/Explosiones/20200722_151800/0087_20200722_140500.h5')
rawclutter2 = wradlib.io.read_opera_hdf5(filenameclutter2)
filenameclutter3 =wradlib.util.get_wradlib_data_file('radar_data_examples/Explosiones/20200722_151800/0087_20200722_141000.h5')
rawclutter3 = wradlib.io.read_opera_hdf5(filenameclutter3)

#to average the ground clutter
rawclutteraverage1=(rawclutter1[
    "dataset1/data2/data"]+rawclutter2[
    "dataset1/data2/data"]+rawclutter3[
    "dataset1/data2/data"])/3

#This is the conversion between 8 bits data (0-254) and reflectivity (0-100)
#reflectivity=raw["dataset1/data2/what"]["offset"] +(raw["dataset1/data2/what"]["gain"])*raw['dataset4/data2/data']
angle1 = raw["dataset1/data2/what"]["offset"] +(raw[
    "dataset1/data2/what"]["gain"])*(raw["dataset1/data2/data"]-rawclutteraverage1)

rawclutteraverage2=(rawclutter1[
    "dataset2/data2/data"]+rawclutter2[
    "dataset2/data2/data"]+rawclutter3[
    "dataset2/data2/data"])/3
angle2 = raw["dataset2/data2/what"]["offset"] +(raw[
    "dataset2/data2/what"]["gain"])*(raw["dataset2/data2/data"]-rawclutteraverage2)

rawclutteraverage3=(rawclutter1[
    "dataset3/data2/data"]+rawclutter2[
    "dataset3/data2/data"]+rawclutter3[
    "dataset3/data2/data"])/3
angle3 = raw["dataset3/data2/what"]["offset"] +(raw[
    "dataset3/data2/what"]["gain"])*(raw["dataset3/data2/data"]-rawclutteraverage3)

rawclutteraverage4=(rawclutter1[
    "dataset4/data2/data"]+rawclutter2[
    "dataset4/data2/data"]+rawclutter3[
    "dataset4/data2/data"])/3
angle4 = raw["dataset4/data2/what"]["offset"] +(raw[
    "dataset4/data2/what"]["gain"])*(raw["dataset4/data2/data"]-rawclutteraverage4)

rawclutteraverage5=(rawclutter1[
    "dataset5/data2/data"]+rawclutter2[
    "dataset5/data2/data"]+rawclutter3[
    "dataset5/data2/data"])/3
angle5 = raw["dataset5/data2/what"]["offset"] +(raw[
    "dataset5/data2/what"]["gain"])*(raw["dataset5/data2/data"]-rawclutteraverage5)

rawclutteraverage6=(rawclutter1[
    "dataset6/data2/data"]+rawclutter2[
    "dataset6/data2/data"]+rawclutter3[
    "dataset6/data2/data"])/3
angle6 = raw["dataset6/data2/what"]["offset"] +(raw[
    "dataset6/data2/what"]["gain"])*(raw["dataset6/data2/data"]-rawclutteraverage6)

rawclutteraverage7=(rawclutter1[
    "dataset7/data2/data"]+rawclutter2[
    "dataset7/data2/data"]+rawclutter3[
    "dataset7/data2/data"])/3
angle7 = raw["dataset7/data2/what"]["offset"] +(raw[
    "dataset7/data2/what"]["gain"])*(raw["dataset7/data2/data"]-rawclutteraverage7)

rawclutteraverage8=(rawclutter1[
    "dataset8/data2/data"]+rawclutter2[
    "dataset8/data2/data"]+rawclutter3[
    "dataset8/data2/data"])/3
angle8 = raw["dataset8/data2/what"]["offset"] +(raw[
    "dataset8/data2/what"]["gain"])*(raw["dataset8/data2/data"]-rawclutteraverage8)

#the order of the angles is inverted for the program to look for the first maximum which is in the highest angle
volume_reflectivity=numpy.stack((angle1,angle2,angle3,angle4,angle5,angle6,angle7,angle8), axis=2)
#volume_reflectivity=numpy.stack((angle8,angle7,angle6,angle5,angle4,angle3,angle2,angle1), axis=2)

#data5 is KDP specific differential phase (deg/km)
KDP_angle1 = raw["dataset1/data5/what"]["offset"] +(raw["dataset1/data5/what"]["gain"])*raw["dataset1/data5/data"]
KDP_angle2 = raw["dataset2/data5/what"]["offset"] +(raw["dataset2/data5/what"]["gain"])*raw["dataset2/data5/data"]
KDP_angle3 = raw["dataset3/data5/what"]["offset"] +(raw["dataset3/data5/what"]["gain"])*raw["dataset3/data5/data"]
KDP_angle4 = raw["dataset4/data5/what"]["offset"] +(raw["dataset4/data5/what"]["gain"])*raw["dataset4/data5/data"]
KDP_angle5 = raw["dataset5/data5/what"]["offset"] +(raw["dataset5/data5/what"]["gain"])*raw["dataset5/data5/data"]
KDP_angle6 = raw["dataset6/data5/what"]["offset"] +(raw["dataset6/data5/what"]["gain"])*raw["dataset6/data5/data"]
KDP_angle7 = raw["dataset7/data5/what"]["offset"] +(raw["dataset7/data5/what"]["gain"])*raw["dataset7/data5/data"]
KDP_angle8 = raw["dataset8/data5/what"]["offset"] +(raw["dataset8/data5/what"]["gain"])*raw["dataset8/data5/data"]

volume_KDP=numpy.stack((KDP_angle1,KDP_angle2,KDP_angle3,KDP_angle4,KDP_angle5,KDP_angle6,KDP_angle7,KDP_angle8), axis=2)
#volume_KDP=numpy.stack((KDP_angle8,KDP_angle7,KDP_angle6,KDP_angle5,KDP_angle4,KDP_angle3,KDP_angle2,KDP_angle1), axis=2)

#data7 is RHOHV copolar cross-correlation coefficient
rawclutterrhohv=(rawclutter1[
    "dataset1/data7/data"]+rawclutter2[
    "dataset1/data7/data"]+rawclutter3[
    "dataset1/data7/data"])/3
RHOHV_angle1 = raw["dataset1/data7/what"]["offset"] +(raw["dataset1/data7/what"]["gain"])*(raw["dataset1/data7/data"]-rawclutterrhohv)
rawclutterrhohv=(rawclutter1[
    "dataset2/data7/data"]+rawclutter2[
    "dataset2/data7/data"]+rawclutter3[
    "dataset2/data7/data"])/3
RHOHV_angle2 = raw["dataset2/data7/what"]["offset"] +(raw["dataset2/data7/what"]["gain"])*(raw["dataset2/data7/data"]-rawclutterrhohv)
rawclutterrhohv=(rawclutter1[
    "dataset3/data7/data"]+rawclutter2[
    "dataset3/data7/data"]+rawclutter3[
    "dataset3/data7/data"])/3
RHOHV_angle3 = raw["dataset3/data7/what"]["offset"] +(raw["dataset3/data7/what"]["gain"])*(raw["dataset3/data7/data"]-rawclutterrhohv)
rawclutterrhohv=(rawclutter1[
    "dataset4/data7/data"]+rawclutter2[
    "dataset4/data7/data"]+rawclutter3[
    "dataset4/data7/data"])/3
RHOHV_angle4 = raw["dataset4/data7/what"]["offset"] +(raw["dataset4/data7/what"]["gain"])*(raw["dataset4/data7/data"]-rawclutterrhohv)
rawclutterrhohv=(rawclutter1[
    "dataset5/data7/data"]+rawclutter2[
    "dataset5/data7/data"]+rawclutter3[
    "dataset5/data7/data"])/3
RHOHV_angle5 = raw["dataset5/data7/what"]["offset"] +(raw["dataset5/data7/what"]["gain"])*(raw["dataset5/data7/data"]-rawclutterrhohv)
rawclutterrhohv=(rawclutter1[
    "dataset6/data7/data"]+rawclutter2[
    "dataset6/data7/data"]+rawclutter3[
    "dataset6/data7/data"])/3
RHOHV_angle6 = raw["dataset6/data7/what"]["offset"] +(raw["dataset6/data7/what"]["gain"])*(raw["dataset6/data7/data"]-rawclutterrhohv)
rawclutterrhohv=(rawclutter1[
    "dataset7/data7/data"]+rawclutter2[
    "dataset7/data7/data"]+rawclutter3[
    "dataset7/data7/data"])/3
RHOHV_angle7 = raw["dataset7/data7/what"]["offset"] +(raw["dataset7/data7/what"]["gain"])*(raw["dataset7/data7/data"]-rawclutterrhohv)
rawclutterrhohv=(rawclutter1[
    "dataset8/data7/data"]+rawclutter2[
    "dataset8/data7/data"]+rawclutter3[
    "dataset8/data7/data"])/3
RHOHV_angle8 = raw["dataset8/data7/what"]["offset"] +(raw["dataset8/data7/what"]["gain"])*(raw["dataset8/data7/data"]-rawclutterrhohv)

volume_RHOHV=numpy.stack((RHOHV_angle1,RHOHV_angle2,RHOHV_angle3,RHOHV_angle4,RHOHV_angle5,RHOHV_angle6,RHOHV_angle7,RHOHV_angle8), axis=2)
#volume_RHOHV=numpy.stack((RHOHV_angle8,RHOHV_angle7,RHOHV_angle6,RHOHV_angle5,RHOHV_angle4,RHOHV_angle3,RHOHV_angle2,RHOHV_angle1), axis=2)

#data4 is ZDR Differential reflectivity ZDR=Zh/Zv
ZDR_angle1 = raw["dataset1/data4/what"]["offset"] +(raw["dataset1/data4/what"]["gain"])*raw["dataset1/data4/data"]
ZDR_angle2 = raw["dataset2/data4/what"]["offset"] +(raw["dataset2/data4/what"]["gain"])*raw["dataset2/data4/data"]
ZDR_angle3 = raw["dataset3/data4/what"]["offset"] +(raw["dataset3/data4/what"]["gain"])*raw["dataset3/data4/data"]
ZDR_angle4 = raw["dataset4/data4/what"]["offset"] +(raw["dataset4/data4/what"]["gain"])*raw["dataset4/data4/data"]
ZDR_angle5 = raw["dataset5/data4/what"]["offset"] +(raw["dataset5/data4/what"]["gain"])*raw["dataset5/data4/data"]
ZDR_angle6 = raw["dataset6/data4/what"]["offset"] +(raw["dataset6/data4/what"]["gain"])*raw["dataset6/data4/data"]
ZDR_angle7 = raw["dataset7/data4/what"]["offset"] +(raw["dataset7/data4/what"]["gain"])*raw["dataset7/data4/data"]
ZDR_angle8 = raw["dataset8/data4/what"]["offset"] +(raw["dataset8/data4/what"]["gain"])*raw["dataset8/data4/data"]

volume_ZDR=numpy.stack((ZDR_angle1,ZDR_angle2,ZDR_angle3,ZDR_angle4,ZDR_angle5,ZDR_angle6,ZDR_angle7,ZDR_angle8), axis=2)
#volume_ZDR=numpy.stack((ZDR_angle8,ZDR_angle7,ZDR_angle6,ZDR_angle5,ZDR_angle4,ZDR_angle3,ZDR_angle2,ZDR_angle1), axis=2)

"""
angle=raw[].shape[0]
radius=raw[].shape[1]
volume_reflectivity=[]
#print(volume_reflectivity.shape)
for i in range(angle):
    volume_reflectivity.append([])
    for j in range(radius):
        #This is the conversion between 8 bits data (0-254) and reflectivity (0-100)
        volume_reflectivity=raw["dataset%d/data2/what" % (i+1)]["offset"] +(raw["dataset%d/data2/what" % (i+1)]["gain"])*raw["dataset%d/data2/data" % (i+1)]
        #To make the volume containers
        #volume_reflectivity=numpy.append(volume_reflectivity,plane_reflectivity,axis=0).reshape(int(len(plane_reflectivity[:,0])),int(len(plane_reflectivity[0,:])),i)
        volume_reflectivity=numpy.stack(volume_reflectivity,axis=2)
        print(volume_reflectivity.shape)
"""   
#volume_reflectivity.shape
#azimuth = raw['dataset1/how']['startazA'] #to obtain all the azimuth angles
#elangles = raw['dataset1/how']['elangles'] #Elevation angles
rscale= raw['dataset1/where']['rscale'] #


# to find indices greater than some value
refl_index_matrix = []
for i in range(len(volume_reflectivity)): 
    for j in range(100,len(volume_reflectivity[i])):
        for k in range(len(volume_reflectivity[i,j])):
            #if volume_KDP[i][j][k] != 19.234999975:  #This value is important to see the ash plume     
                if volume_RHOHV[i][j][k] < 0.8:  #values below 0.8 are non-meteorological objects 
                    if -0.5 <= volume_ZDR[i][j][k] <= 0.5:   #This value is only for the ash
                        if 17 <= volume_reflectivity[i][j][k] <= 80: #This value of the reflectivity is heuristic so far
                            refl_index_matrix.append((i,j,k))

#print(refl_index_matrix)
#max_radius_index=numpy.unravel_index(numpy.argmax(refl_index_matrix, axis=0), refl_index_matrix.shape)    
max_radius_index=numpy.argmax(refl_index_matrix, axis=0)
print(max_radius_index) #maximum of each dimension separated
print(refl_index_matrix[max_radius_index[0]]) #ordered triple with the maximum in the first one
print(refl_index_matrix[max_radius_index[1]]) #ordered triple with the maximum in the second one
print(refl_index_matrix[max_radius_index[2]]) #ordered triple with the maximum in the third one

#print(refl_index_matrix[max_radius_index[1]][0])
#print(refl_index_matrix[max_radius_index[1]][1])

max_elements=[]
for i, value in enumerate(refl_index_matrix):
    if value == (i,i,max_radius_index[2]):
        max_elements.append(i)
    
print(max_elements)
    

print(volume_reflectivity[refl_index_matrix[max_radius_index[0]]])
print(volume_reflectivity[refl_index_matrix[max_radius_index[1]]])
print(volume_reflectivity[refl_index_matrix[max_radius_index[2]]])

#print(volume_KDP[refl_index_matrix[max_radius_index[0]]])
#print(volume_KDP[refl_index_matrix[max_radius_index[1]]])
#print(volume_KDP[refl_index_matrix[max_radius_index[2]]])

max_radius=numpy.amax(refl_index_matrix, axis=0)
print(max_radius)

elangle=raw['dataset%d/how' % (max_radius[2]+1)]['elangles'] #Elevation angles in degrees
elangle_rad=elangle[0]*numpy.pi/180
print(elangle[0])
#The elevation is in spherical coordinates
max_altitude=refl_index_matrix[max_radius_index[2]][1]*rscale*numpy.sin(elangle_rad)
max_distance=refl_index_matrix[max_radius_index[2]][1]*rscale*numpy.cos(elangle_rad)

sitecoords = (raw["where"]["lon"], 
              raw["where"]["lat"],
              raw["where"]["height"])

print("La distancia máxima de la pluma a este ángulo es", max_distance)
print("La altura de la columna sobre el nivel del mar es", max_altitude+4000)
print("La altura de la columna sobre el cráter es", max_altitude-1500)

"""
altitude=open('altitude.txt', 'a')
altitude.write('maximum altitude' % altitude_max-1500)
altitude.close()
"""