# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 23:47:10 2021

@author: ERIC TELLEZ
Reading and visualizing an ODIM_H5 polar volume

This code is suited from the wradlib original to read the Furuno netCDF data

Differential reflectivity


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

# read the data (Furuno data)

#rawclutter is the file without the explosion
#The more data the better
filenameclutter =wrl.util.get_wradlib_data_file('radar_data_examples/Explosiones/20210915_044742/ODIM_H5/0087_20210915_044742.h5') 
rawclutter1 = wrl.io.read_opera_hdf5(filenameclutter)
filenameclutter2 =wrl.util.get_wradlib_data_file('radar_data_examples/Explosiones/20210915_044742/ODIM_H5/0087_20210915_044824.h5')
rawclutter2 = wrl.io.read_opera_hdf5(filenameclutter2)
filenameclutter3 =wrl.util.get_wradlib_data_file('radar_data_examples/Explosiones/20210915_044742/ODIM_H5/0087_20210915_044949.h5')
rawclutter3 = wrl.io.read_opera_hdf5(filenameclutter3)


#filename = wrl.util.get_wradlib_data_file('radar_data_examples/ODIM_H5/0087_20210911/0087_20210911_174500.h5')
filename = wrl.util.get_wradlib_data_file('radar_data_examples/Explosiones/20210915_044742/ODIM_H5/0087_20210915_045653.h5')
raw = wrl.io.read_opera_hdf5(filename)
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

data4 raw['dataset2/data4/what']['quantity']  is radar reflection factor difference ZDR
or differenctial reflectivity Zh-Zv
Zero or nearly zero for spherical objects
Positive for horizontal oriented objects
Negative for vertical oriented objects

It is likely that ash has no preferred orientation, so these values should be near zero 
but I have to think about it.
"""

how = raw['dataset1/how']['startazA'] #to obtain all the azimuth angles
maxaz = len(how) #It gives the lenght of the array
sector = abs(int(how[maxaz-1]-how[0]))+1  #Angle size of the scanned sector
#how[0] is the first angle of the measurement

# iterate over 8 elevation angles
for i in range(8):
    # get the scan metadata for each elevation
    where = raw["dataset%d/where" % (i + 1)] #to obtain nbins, nrays, rscale, rscale, elangle
    what = raw["dataset%d/data4/what" % (i + 1)] # to obtain the gain and the offset
    
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
    
    #Creating an array of invalida data (values=255) to complete the circular sector
    nodata=np.ones(int(rays*((360/sector)-1))*bins)*255
    nodata=np.reshape(nodata, (int(rays*((360/(sector)-1))),bins))
    
    # get the scan data for this elevation
    #   here, you can do all the processing on the 2-D polar level
    #   e.g. clutter elimination, attenuation correction, ...
    #data_ = what["offset"] + (what["gain"])* raw[
    #    "dataset%d/data2/data" % (i + 1)] 
    
    """
    data_ =  what["offset"] +(what["gain"])*raw[
        "dataset%d/data4/data" % (i + 1)] 
    data_=np.append(data_,nodata).reshape((int(rays*(360/sector)),bins))
    """
    
    #Sometimes the data has different number of rows or columns. This statement is to correct that.
    #if raw["dataset%d/data2/data"%(i+1)] == rawclutter["dataset%d/data2/data"%(i+1)]
    #diffrows = raw["dataset%d/data4/data"%(i+1)][:2] - rawclutter["dataset%d/data2/data"%(i+1)]
    #diffcolumns = raw["dataset%d/data2/data"%(i+1)] - rawclutter["dataset%d/data2/data"%(i+1)]
    #columnsextra = 
    
    rawclutteraverage=(rawclutter1[
        "dataset%d/data4/data" % (i + 1)]+rawclutter2[
        "dataset%d/data4/data" % (i + 1)]+rawclutter3[
        "dataset%d/data4/data" % (i + 1)])/3
    
    data_ = (what["offset"] +(what["gain"])*(raw[
            "dataset%d/data4/data" % (i + 1)]))*100# - rawclutteraverage)
                   # Here I can substract the ground, that means the clutter elimination
    
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
    # realign azimuth array to have 0deg as first ray
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

#print("3-D interpolation took:", dt.datetime.now() - tstart)
"""
tstart = dt.datetime.now()
vertical = wrl.vpr.CartesianVolume(xyz, 
                                   trgxyz, 
                                   trgshape, 
                                   maxrange, 
                                   minelev, 
                                   maxelev, 
                                   ipclass=wrl.ipol.Idw) 
                                  

vol = np.ma.masked_invalid(vertical(data).reshape(trgshape))
"""
vol = np.ma.masked_invalid(gridder(data).reshape(trgshape))
print("3-D interpolation took:", dt.datetime.now() - tstart)

unit = raw['dataset2/data4/what']['quantity'] #the units of the plot
dateGMT = raw['what']['startdate']
timeGMT = raw['what']['starttime']
date = raw['what']['Local_date']
time = raw['what']['Local_time']
sensorname = raw['what']['source']

# diagnostic plot
trgx = trgxyz[:, 0].reshape(trgshape)[0, 0, :]
trgy = trgxyz[:, 1].reshape(trgshape)[0, :, 0]
trgz = trgxyz[:, 2].reshape(trgshape)[:, 0, 0]

#For ZDR the max doesnt work because ash has a possible nearly zero value
wrl.vis.plot_max_plan_and_vert(trgx, 
                               trgy, 
                               trgz, 
                               vol, 
                               unit="Differential reflectivity {0}".format(unit),
                               levels=range(-200, 300), #This is the ZDR scale
                               title='CAPPI: Radar {0}, {1}T{2}GMT {3}T{4}Altzomoni'.format(sensorname,dateGMT,timeGMT,date,time))

#print(vol) To read the maximum altitude of the plume
"""
wrl.vis.plot_plan_and_vert(trgx, 
                           trgy, 
                           trgz, 
                           vol, 
                           unit="Horizontal Reflectivity {0}".format(unit),
                           levels=range(-32, 60), 
                           title='CAPPI: Radar {0}, {1}T{2}GMT {3}T{4}Altzomoni'.format(sensorname,dateGMT,timeGMT,date,time))
"""