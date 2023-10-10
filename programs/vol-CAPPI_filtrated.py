# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 19:25:02 2022

@author: Eric Tellez

Vol-CAPPI filtrated

This program is to plot the ash in Vol-CAPPI with the dbzh but only the dbzh that
fulfill the consditions imposed by the other variables. So the dbzh is filtrated. 


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
import glob
import os
import warnings
warnings.filterwarnings('ignore')

#import xarray as xr
#from shapely.errors import ShapelyDeprecationWarning
#from xmovie import Movie


#To import files automatically
path= 'D:/explosiones/20220909_034300local/H5/0087_20220909/0087_20220909_095000.h5'
list_of_files=glob.glob(path, recursive=True)
newest_file = max(list_of_files, key=os.path.getctime)
filename_with_path = wrl.util.get_wradlib_data_file(newest_file)
raw = wrl.io.read_opera_hdf5(filename_with_path)

path_clutter='D:/Ground_Clutter/Clutter_base/Clutter_popo_30km.npy'
Clutter = np.load(path_clutter)

"""
#Here I have to import the data to make the movie
# Load test dataset
ds = xr.tutorial.open_dataset('air_temperature').isel(time=slice(0, 150))
# Create movie object
mov = Movie(ds.air)
"""
  
# define your cartesian reference system
# For Mexico City: https://epsg.io/?q=Mexico
proj = osr.SpatialReference()
proj.ImportFromEPSG(6371)
    
# containers to hold Cartesian bin coordinates and data
xyz, data = np.array([]).reshape((-1, 3)), np.array([])
data_filtrated=np.array([]).reshape((-1, 3))

"""
#nrays is x (rows), nbins is y (columns)
dataset# is the angle
dataset#/data# is the physical variable
    
data2 raw['dataset2/data2/what']['quantity']  is the horizontal reflectivity dBzH
"""

# this is the radar position tuple (longitude, latitude, altitude)
sitecoords = (raw["where"]["lon"], 
              raw["where"]["lat"],
              raw["where"]["height"])

how = raw['dataset1/how']['startazA'] #to obtain all the azimuth angles
maxaz = len(how) #It gives the lenght of the array
sector = abs(int(how[maxaz-1]-how[0]))+1  #Angle size of the scanned sector
#how[0] is the first angle of the measurement

#To get the name of the file and paste it into the name of the plots
filename = os.path.basename(filename_with_path) #Filename with extension
file = os.path.splitext(filename)  #Tuple of string with filename and extension   


# iterate over the elevation angles
for i in range(8):
    # get the scan metadata for each elevation 
    where = raw["dataset%d/where" % (i + 3)] #to obtain nbins, nrays, rscale, elangle
    what = raw["dataset%d/data2/what" % (i + 3)] # to obtain the gain and the offset
    
    #nrays is x (rows), nbins is y (columns)
    rays=where["nrays"]
    bins=where["nbins"]
        
    # define arrays of polar coordinate arrays (azimuth and range)
    #az = np.arange(0., 360., 360/where["nrays"])
    az = np.arange(0., 359., sector/where["nrays"]) 
            
    # rstart is given in km, so multiply by 1000.
    rstart = where["rstart"] * 1000.
    r = np.arange(rstart,
                  rstart + 401 * where["rscale"],
                  where["rscale"])
            
    # derive 3-D Cartesian coordinate tuples
    xyz_ = wrl.vpr.volcoords_from_polar(sitecoords, 
                                        where["elangle"],
                                        az, 
                                        r, 
                                        proj)

    #Creating an array of invalid data (values=255) or zeros to complete the circular sector
    #Value of 255 rise a problem in the edges of the circular sector.
    #nodata=np.ones(int(rays*((360/sector)-1))*bins)*255
    nodata=np.zeros(int(rays*((360/sector)-1))*401)
    nodata=np.reshape(nodata, (int(rays*((360/(sector)-1))),401))
    
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
    """
    rawclutteraverage=(rawclutter1[
                    "dataset%d/data2/data" % (i + 1)]+rawclutter2[
                    "dataset%d/data2/data" % (i + 1)]+rawclutter3[
                    "dataset%d/data2/data" % (i + 1)])/3
    """
    #This is the conversion between 8 bits data (0-254) and reflectivity (0-100)
    data_ = what["offset"] +(what["gain"])*(raw[
        "dataset%d/data2/data" % (i + 3)])
    
    data_filtrated=data_[:,0:401]#-Clutter[i,:,:]
    # Here I can substract the ground, that means the clutter elimination
    
    
    
    #RATE_rainfall_intensity=raw["dataset%d/data1/what"%(i+3)]["offset"] +(raw["dataset%d/data1/what"%(i+3)]["gain"])*raw["dataset%d/data1/data"%(i+3)] #This dataset is not that important
    #DBZH_horizontal_reflectivity=raw["dataset%d/data2/what"%(i+3)]["offset"] +(raw["dataset%d/data2/what"%(i+3)]["gain"])*raw["dataset%d/data2/data"%(i+3)]
    
    VRAD_radial_velocity=raw["dataset%d/data3/what"%(i+3)]["offset"]+(raw["dataset%d/data3/what"%(i+3)]["gain"])*raw["dataset%d/data3/data"%(i+3)]
    ZDR_reflection_factor_difference=raw["dataset%d/data4/what"%(i+3)]["offset"]+(raw["dataset%d/data4/what"%(i+3)]["gain"])*raw["dataset%d/data4/data"%(i+3)]
    KDP_propagation_phase_difference_rate_of_change=raw["dataset%d/data5/what"%(i+3)]["offset"] +(raw["dataset%d/data5/what"%(i+3)]["gain"])*raw["dataset%d/data5/data"%(i+3)]
    PHIDP_differential_propagation_phase=raw["dataset%d/data6/what"%(i+3)]["offset"]+(raw["dataset%d/data6/what"%(i+3)]["gain"])*raw["dataset%d/data6/data"%(i+3)]
    RHOHV_copolar_correlation_coefficient=raw["dataset%d/data7/what"%(i+3)]["offset"]+(raw["dataset%d/data7/what"%(i+3)]["gain"])*raw["dataset%d/data7/data"%(i+3)]
    WRAD_doppler_velocity_spectrum_width=raw["dataset%d/data8/what"%(i+3)]["offset"]+(raw["dataset%d/data8/what"%(i+3)]["gain"])*raw["dataset%d/data8/data"%(i+3)]
    
    
    # to find the indices that best describe the ash plume with all the variables together
    for j in range(rays):
        for k in range(bins):
    
            if 0.8 >= RHOHV_copolar_correlation_coefficient[j,k] <= 1.26492:         
                if -1.22874511>= KDP_propagation_phase_difference_rate_of_change[j,k]>= 0.156019595: 
                    if -4>= ZDR_reflection_factor_difference[j,k] <= 4: 
                        if -0.5>= PHIDP_differential_propagation_phase[j,k]<= 0.5: 
                            if -30>= VRAD_radial_velocity[j,k]<=30:    
                                if 0>= WRAD_doppler_velocity_spectrum_width[j,k] <= 5: 
                                    data_filtrated[i,j,k]=data_filtrated[i,j,k]
                                else: 
                                    data_filtrated[i,j,k]=0
                                                    
    #This code is to add the zero columns missing because the vol-cappi only plots 360 and in this case we have a 30º sector
    data_filtrated=np.append(data_filtrated,nodata).reshape((int(rays*(360/sector)),401))
    
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
    xyz, data = np.vstack((xyz, xyz_)), np.append(data, data_filtrated.ravel())
            

# generate 3-D Cartesian target grid coordinates
maxrange = 15000. #This range is diameter. For Popo=35000 Furuno max range is 70000 in radius
minelev = 3.1     #minimum elevation angle set up by scan strategy
maxelev = 28.     #maximum elevation angle set up by scan strategy
minalt = 5500.    #minimum altitude maxrange*sin(minelev)
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
                                        minalt) #Here you can set up the altitude of the radar or the border of the crater

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

unit = raw['dataset2/data2/what']['quantity'].decode('UTF-8') #the units of the plot
dateGMT = raw['what']['startdate'].decode('UTF-8')
dateGMT = dateGMT[:4]+"-"+ dateGMT[4:]
dateGMT = dateGMT[:7]+"-"+ dateGMT[7:]
timeGMT = raw['what']['starttime'].decode('UTF-8')
timeGMT = timeGMT[:2]+":"+ timeGMT[2:]
timeGMT = timeGMT[:5]+":"+ timeGMT[5:]
date = raw['what']['Local_date'].decode('UTF-8')
date = date[:4]+"-"+ date[4:]
date = date[:7]+"-"+ date[7:]
time = raw['what']['Local_time'].decode('UTF-8')
time = time[:2]+":"+ time[2:]
time = time[:5]+":"+ time[5:]
sensorname = raw['what']['source'].decode('UTF-8')

# diagnostic plot
trgx = trgxyz[:, 0].reshape(trgshape)[0, 0, :]
trgy = trgxyz[:, 1].reshape(trgshape)[0, :, 0]
trgz = trgxyz[:, 2].reshape(trgshape)[:, 0, 0]

wrl.vis.plot_max_plan_and_vert(trgx, 
                               trgy, 
                               trgz, 
                               vol, 
                               unit="Horizontal Reflectivity {0}".format(unit),
                               levels=range(27, 38), #This is the reflectivity scale. The best plume is seen from 27-38
                               #levels=range(0, 100),
                               title='{0} {1} local, {2} {3} GMT'.format(date,time,dateGMT,timeGMT), #title in the graph
                               )#saveto='D:/Carpeta_Imag/VCAPPI/VCAPPI_{0}'.format(file[0])) #name of the file

