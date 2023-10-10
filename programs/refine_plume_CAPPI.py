# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 12:44:24 2022

@author: Eric Tellez

Reading and visualizing the plume in an ODIM_H5 polar volume using all the 
variables that come out from the radar

This code is suited from the wradlib original to read the Furuno netCDF data

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
import numpy as np
import datetime as dt
from osgeo import osr

# dataset# is angle and data# is physical variable

#import the Furuno data
filename = wradlib.util.get_wradlib_data_file('radar_data_examples/Explosiones/20210915_044742/ODIM_H5/0087_20210915_045031.h5')
raw = wradlib.io.read_opera_hdf5(filename)

#rawclutter is the file without the explosion
#The more data the better
filenameclutter =wrl.util.get_wradlib_data_file('radar_data_examples/Explosiones/20210915_044742/ODIM_H5/0087_20210915_044742.h5') 
rawclutter1 = wrl.io.read_opera_hdf5(filenameclutter)
filenameclutter2 =wrl.util.get_wradlib_data_file('radar_data_examples/Explosiones/20210915_044742/ODIM_H5/0087_20210915_044824.h5')
rawclutter2 = wrl.io.read_opera_hdf5(filenameclutter2)
filenameclutter3 =wrl.util.get_wradlib_data_file('radar_data_examples/Explosiones/20210915_044742/ODIM_H5/0087_20210915_044949.h5')
rawclutter3 = wrl.io.read_opera_hdf5(filenameclutter3)


#data1 is not needed because that data is ranfall intensity (mm/h)

#data2 is reflection factor of the horizontal polarimetric radar cBZh
DBZH_angle1 = raw["dataset1/data2/what"]["offset"] +(raw["dataset1/data2/what"]["gain"])*raw["dataset1/data2/data"]
DBZH_angle2 = raw["dataset2/data2/what"]["offset"] +(raw["dataset2/data2/what"]["gain"])*raw["dataset2/data2/data"]
DBZH_angle3 = raw["dataset3/data2/what"]["offset"] +(raw["dataset3/data2/what"]["gain"])*raw["dataset3/data2/data"]
DBZH_angle4 = raw["dataset4/data2/what"]["offset"] +(raw["dataset4/data2/what"]["gain"])*raw["dataset4/data2/data"]
DBZH_angle5 = raw["dataset5/data2/what"]["offset"] +(raw["dataset5/data2/what"]["gain"])*raw["dataset5/data2/data"]
DBZH_angle6 = raw["dataset6/data2/what"]["offset"] +(raw["dataset6/data2/what"]["gain"])*raw["dataset6/data2/data"]
DBZH_angle7 = raw["dataset7/data2/what"]["offset"] +(raw["dataset7/data2/what"]["gain"])*raw["dataset7/data2/data"]
DBZH_angle8 = raw["dataset8/data2/what"]["offset"] +(raw["dataset8/data2/what"]["gain"])*raw["dataset8/data2/data"]

volume_DBZH=numpy.stack((DBZH_angle1,DBZH_angle2,DBZH_angle3,DBZH_angle4,DBZH_angle5,DBZH_angle6,DBZH_angle7,DBZH_angle8), axis=2)

#data3 is radial velocity VRAD + is away and - is toward the radar 
VRAD_angle1 = raw["dataset1/data3/what"]["offset"] +(raw["dataset1/data3/what"]["gain"])*raw["dataset1/data3/data"]
VRAD_angle2 = raw["dataset2/data3/what"]["offset"] +(raw["dataset2/data3/what"]["gain"])*raw["dataset2/data3/data"]
VRAD_angle3 = raw["dataset3/data3/what"]["offset"] +(raw["dataset3/data3/what"]["gain"])*raw["dataset3/data3/data"]
VRAD_angle4 = raw["dataset4/data3/what"]["offset"] +(raw["dataset4/data3/what"]["gain"])*raw["dataset4/data3/data"]
VRAD_angle5 = raw["dataset5/data3/what"]["offset"] +(raw["dataset5/data3/what"]["gain"])*raw["dataset5/data3/data"]
VRAD_angle6 = raw["dataset6/data3/what"]["offset"] +(raw["dataset6/data3/what"]["gain"])*raw["dataset6/data3/data"]
VRAD_angle7 = raw["dataset7/data3/what"]["offset"] +(raw["dataset7/data3/what"]["gain"])*raw["dataset7/data3/data"]
VRAD_angle8 = raw["dataset8/data3/what"]["offset"] +(raw["dataset8/data3/what"]["gain"])*raw["dataset8/data3/data"]

volume_VRAD=numpy.stack((VRAD_angle1,VRAD_angle2,VRAD_angle3,VRAD_angle4,VRAD_angle5,VRAD_angle6,VRAD_angle7,VRAD_angle8), axis=2)

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

#data6 is cross polarization difference phase phidp=phih-phiv
#is dependent directly on particle concentration (at least in water) higher value higher particles
PHIDP_angle1 = raw["dataset1/data6/what"]["offset"] +(raw["dataset1/data6/what"]["gain"])*raw["dataset1/data6/data"]
PHIDP_angle2 = raw["dataset2/data6/what"]["offset"] +(raw["dataset2/data6/what"]["gain"])*raw["dataset2/data6/data"]
PHIDP_angle3 = raw["dataset3/data6/what"]["offset"] +(raw["dataset3/data6/what"]["gain"])*raw["dataset3/data6/data"]
PHIDP_angle4 = raw["dataset4/data6/what"]["offset"] +(raw["dataset4/data6/what"]["gain"])*raw["dataset4/data6/data"]
PHIDP_angle5 = raw["dataset5/data6/what"]["offset"] +(raw["dataset5/data6/what"]["gain"])*raw["dataset5/data6/data"]
PHIDP_angle6 = raw["dataset6/data6/what"]["offset"] +(raw["dataset6/data6/what"]["gain"])*raw["dataset6/data6/data"]
PHIDP_angle7 = raw["dataset7/data6/what"]["offset"] +(raw["dataset7/data6/what"]["gain"])*raw["dataset7/data6/data"]
PHIDP_angle8 = raw["dataset8/data6/what"]["offset"] +(raw["dataset8/data6/what"]["gain"])*raw["dataset8/data6/data"]

volume_PHIDP=numpy.stack((PHIDP_angle1,PHIDP_angle2,PHIDP_angle3,PHIDP_angle4,PHIDP_angle5,PHIDP_angle6,PHIDP_angle7,PHIDP_angle8), axis=2)

#data7 is RHOHV copolar cross-correlation coefficient
RHOHV_angle1 = raw["dataset1/data7/what"]["offset"] +(raw["dataset1/data7/what"]["gain"])*raw["dataset1/data7/data"]
RHOHV_angle2 = raw["dataset2/data7/what"]["offset"] +(raw["dataset2/data7/what"]["gain"])*raw["dataset2/data7/data"]
RHOHV_angle3 = raw["dataset3/data7/what"]["offset"] +(raw["dataset3/data7/what"]["gain"])*raw["dataset3/data7/data"]
RHOHV_angle4 = raw["dataset4/data7/what"]["offset"] +(raw["dataset4/data7/what"]["gain"])*raw["dataset4/data7/data"]
RHOHV_angle5 = raw["dataset5/data7/what"]["offset"] +(raw["dataset5/data7/what"]["gain"])*raw["dataset5/data7/data"]
RHOHV_angle6 = raw["dataset6/data7/what"]["offset"] +(raw["dataset6/data7/what"]["gain"])*raw["dataset6/data7/data"]
RHOHV_angle7 = raw["dataset7/data7/what"]["offset"] +(raw["dataset7/data7/what"]["gain"])*raw["dataset7/data7/data"]
RHOHV_angle8 = raw["dataset8/data7/what"]["offset"] +(raw["dataset8/data7/what"]["gain"])*raw["dataset8/data7/data"]

volume_RHOHV=numpy.stack((RHOHV_angle1,RHOHV_angle2,RHOHV_angle3,RHOHV_angle4,RHOHV_angle5,RHOHV_angle6,RHOHV_angle7,RHOHV_angle8), axis=2)

#data8 is WRAD velocity spectrum width (m/s)
WRAD_angle1 = raw["dataset1/data8/what"]["offset"] +(raw["dataset1/data8/what"]["gain"])*raw["dataset1/data8/data"]
WRAD_angle2 = raw["dataset2/data8/what"]["offset"] +(raw["dataset2/data8/what"]["gain"])*raw["dataset2/data8/data"]
WRAD_angle3 = raw["dataset3/data8/what"]["offset"] +(raw["dataset3/data8/what"]["gain"])*raw["dataset3/data8/data"]
WRAD_angle4 = raw["dataset4/data8/what"]["offset"] +(raw["dataset4/data8/what"]["gain"])*raw["dataset4/data8/data"]
WRAD_angle5 = raw["dataset5/data8/what"]["offset"] +(raw["dataset5/data8/what"]["gain"])*raw["dataset5/data8/data"]
WRAD_angle6 = raw["dataset6/data8/what"]["offset"] +(raw["dataset6/data8/what"]["gain"])*raw["dataset6/data8/data"]
WRAD_angle7 = raw["dataset7/data8/what"]["offset"] +(raw["dataset7/data8/what"]["gain"])*raw["dataset7/data8/data"]
WRAD_angle8 = raw["dataset8/data8/what"]["offset"] +(raw["dataset8/data8/what"]["gain"])*raw["dataset8/data8/data"]

volume_WRAD=numpy.stack((WRAD_angle1,WRAD_angle2,WRAD_angle3,WRAD_angle4,WRAD_angle5,WRAD_angle6,WRAD_angle7,WRAD_angle8), axis=2)

# to find the indices that best describe the ash plume with all the variables together
plume_index_matrix = []
for i in range(len(volume_DBZH)):
    for j in range(len(volume_DBZH[i])):
        for k in range(len(volume_DBZH[i,j])):
            if volume_DBZH[i][j][k] >= 17: #This value for the reflectivity is heuristic so far
                if volume_VRAD[i][j][k] >= 64: #This value is heuristic
                    if -1 >= volume_ZDR[i][j][k] >= 1:
                        #if volume_KDP[i][j][k] >= :
                            if -0.5 >= volume_PHIDP[i][j][k] >= 0.5  :
                                if volume_RHOHV[i][j][k] >= :
                                    if volume_WRAD[i][j][k] >= :
                                           
            
                                        plume_index_matrix.append((i,j,k))
                                        


# this is the radar position tuple (longitude, latitude, altitude)
sitecoords = (raw["where"]["lon"], 
              raw["where"]["lat"],
              raw["where"]["height"])

# define your cartesian reference system
# For Mexico City: https://epsg.io/?q=Mexico
proj = osr.SpatialReference()
proj.ImportFromEPSG(6371)

# containers to hold Cartesian bin coordinates and data
xyz, data = np.array([]).reshape((-1, 3)), np.array([])

"""
#nrays is x (rows), nbins is y (columns)
dataset# is the angle
dataset#/data# is the physical variable

data2 raw['dataset2/data2/what']['quantity']  is the horizontal reflectivity dBzH
"""

how = raw['dataset1/how']['startazA'] #to obtain all the azimuth angles
maxaz = len(how) #It gives the lenght of the array
sector = abs(int(how[maxaz-1]-how[0]))+1  #Angle size of the scanned sector
#how[0] is the first angle of the measurement

# iterate over 8 elevation angles
for i in range(8): 
    #for j in range(2,9) # I need this cycle to obtain all the physical variables
    # get the scan metadata for each elevation
    where = raw["dataset%d/where" % (i + 1)] #to obtain nbins, nrays, rscale, rscale, elangle
    what = raw["dataset%d/data2/what" % (i + 1)] # to obtain the gain and the offset
    
    #nrays is x (rows), nbins is y (columns)
    rays=where["nrays"]
    bins=where["nbins"]
    
    # define arrays of polar coordinate arrays (azimuth and range)
    #az = np.arange(0., 360., 360/where["nrays"])
    az = np.arange(0., 360., sector/where["nrays"]) 

    # rstart is given in km, so multiply by 1000.
    rstart = where["rstart"] * 1000.
    r = np.arange(rstart,
                  rstart + bins * where["rscale"],
                  where["rscale"])
    
    # derive 3-D Cartesian coordinate tuples
    xyz_ = wrl.vpr.volcoords_from_polar(sitecoords, 
                                        where["elangle"],
                                        az, 
                                        r, 
                                        proj)
    
    #Creating an array of invalid data (values=255) or zeros to complete the circular sector
    #Value of 255 rise a problem in the edges of the circular sector.
    nodata=np.zeros(int(rays*((360/sector)-1))*bins)
    nodata=np.reshape(nodata, (int(rays*((360/(sector)-1))),bins))
    
    # get the scan data for this elevation
    #   here, you can do all the processing on the 2-D polar level
    #   e.g. clutter elimination, attenuation correction, ...
    #data_ = what["offset"] + (what["gain"])* raw[
    #    "dataset%d/data2/data" % (i + 1)] 
    
    """
    data_ =  what["offset"] +(what["gain"])*raw[
        "dataset%d/data2/data" % (i + 1)] 
    data_=np.append(data_,nodata).reshape((int(rays*(360/sector)),bins))
    """
    
    #Sometimes the data has different number of rows or columns. This statement is to correct that.
    #if raw["dataset%d/data2/data"%(i+1)] == rawclutter["dataset%d/data2/data"%(i+1)]
    #diffrows = raw["dataset%d/data2/data"%(i+1)][:2] - rawclutter["dataset%d/data2/data"%(i+1)]
    #diffcolumns = raw["dataset%d/data2/data"%(i+1)] - rawclutter["dataset%d/data2/data"%(i+1)]
    #columnsextra = np.zeros() 
    
    rawclutteraverage=(rawclutter1[
        "dataset%d/data2/data" % (i + 1)]+rawclutter2[
        "dataset%d/data2/data" % (i + 1)]+rawclutter3[
        "dataset%d/data2/data" % (i + 1)])/3
    
    #This is the conversion between 8 bits data (0-254) and reflectivity (0-100)
    data_ = what["offset"] +(what["gain"])*(raw[
            "dataset%d/data2/data" % (i + 1)] - rawclutteraverage)
                   # Here I can substract the ground, that means the clutter elimination
    
    #This code is to add the zero columns missing because the vol-cappi only plots 360 and in this case we have a 30º sector
    data_=np.append(data_,nodata).reshape((int(rays*(360/sector)),bins))

    """
    The next function is written based on 
    Gianfranco Vulpiani, Mario Montopoli, Luca Delli Passeri, Antonio G. Gioia, Pietro Giordano, and Frank S. Marzano. 
    On the use of dual-polarized c-band radar for operational rainfall retrieval in mountainous areas. 
    Journal of Applied Meteorology and Climatology, 51(2):405–425, Feb 2012. 
    doi:10.1175/JAMC-D-10-05024.1.         
    
    wradlib.clutter.classify_echo_fuzzy(dat, weights=None, trpz=None, thresh=0.5)
    """    
    
    # make sure the data is aligned to zero azimuth == due north
    # get azimuth of first ray
    zero_az = int(rays*how[0]/sector)
    # realign azimuth array to have 0 deg as first ray
    data_ = np.roll(data_, zero_az, axis=0)
    
    # transfer to containers
    xyz, data = np.vstack((xyz, xyz_)), np.append(data, data_.ravel())
    

# generate 3-D Cartesian target grid coordinates
maxrange = 15000. #This range is diameter. For Popo=35000 Furuno max range is 70000 in radius
minelev = 3.1     #minimum elevation angle set up by scan strategy
maxelev = 28.     #maximum elevation angle set up by scan strategy
maxalt = 10000.   #altitude (Good number = 10000)
horiz_res = 100. #This resolution is in meters (Good number = 100)
vert_res = 50.   #This resolution is in meters (Good number = 50)

#trgxyz are the coordinates
#trgshape is the size of the 3D matrix
trgxyz, trgshape = wrl.vpr.make_3d_grid(sitecoords, 
                                        proj, 
                                        maxrange,
                                        maxalt, 
                                        horiz_res, 
                                        vert_res, 
                                        minalt=5500) #Here you can set up the altitude of the radar or the border of the crater

# interpolate to Cartesian 3-D volume grid
tstart = dt.datetime.now()
gridder = wrl.vpr.CAPPI(xyz, 
                        trgxyz, 
                        trgshape, 
                        maxrange, 
                        minelev,
                        maxelev,
                        ipclass=wrl.ipol.Idw) #For interpolation


vol = np.ma.masked_invalid(gridder(data).reshape(trgshape))

#wrl.vpr.norm_vpr_stats(vol,)   #To visualize some statistics

print("3-D interpolation took:", dt.datetime.now() - tstart)

unit = raw['dataset2/data2/what']['quantity'] #the units of the plot
dateGMT = raw['what']['startdate']
timeGMT = raw['what']['starttime']
date = raw['what']['Local_date']
time = raw['what']['Local_time']
sensorname = raw['what']['source']

# diagnostic plot
trgx = trgxyz[:, 0].reshape(trgshape)[0, 0, :]
trgy = trgxyz[:, 1].reshape(trgshape)[0, :, 0]
trgz = trgxyz[:, 2].reshape(trgshape)[:, 0, 0]

wrl.vis.plot_max_plan_and_vert(trgx, 
                               trgy, 
                               trgz, 
                               vol, 
                               unit="Horizontal Reflectivity {0}".format(unit),
                               levels=range(17, 80), #This is the reflectivity scale
                               #levels=range(0, 100),
                               title='Vol-CAPPI: Radar {0}, {1}T{2}GMT {3}T{4}Altzomoni'.format(sensorname,dateGMT,timeGMT,date,time))