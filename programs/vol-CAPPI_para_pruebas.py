# -*- coding: utf-8 -*-
"""
Created on Sun Sep 12 02:31:25 2021

@author: ERIC TELLEZ

Reading and visualizing an ODIM_H5 polar volume
The code is suited from the wradlib original to read the Furuno netCDF data

Specifically the reflectivity in the data dBz


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

tprogram = dt.datetime.now()

#To import files automatically
path= 'C:/Users/radar1/Desktop/actividad_19_mayo/H5/0087_20230520/0087_20230520*.h5'
#path= 'D:/ODIM_H5/0087_20221129/0087_20221129_23*.h5'
list_of_files=glob.glob(path, recursive=True)
all_files=len(list_of_files)


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
 
for i in range (all_files):
    current_file=list_of_files[i]
    filename_path = wrl.util.get_wradlib_data_file(current_file)
    raw = wrl.io.read_opera_hdf5(filename_path)
     
    #To get the name of the file and paste it into the name of the plots
    filename = os.path.basename(filename_path) #Filename with extension
    file = os.path.splitext(filename)  #Tuple of string with filename and extension
   
    # this is the radar position tuple (longitude, latitude, altitude)
    sitecoords = (raw["where"]["lon"], 
                 raw["where"]["lat"],
                 raw["where"]["height"])
   
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
        
    # iterate over the elevation angles
    for a in range(10):
        # get the scan metadata for each elevation
        where = raw["dataset%d/where" % (a + 1)] #to obtain nbins, nrays, rscale, elangle
        what = raw["dataset%d/data2/what" % (a + 1)] # to obtain the gain and the offset
       
        #nrays is x (rows), nbins is y (columns)
        rays=where["nrays"]
        bins=where["nbins"]
       
        # define arrays of polar coordinate arrays (azimuth and range)
        az = np.arange(0., 359., 360/where["nrays"]) #this line is to 360 sectors
        #az = np.arange(0., 360., sector/where["nrays"]) #This line is to sectors smaller than 360, ie the ones that are produced by sppi scans
       
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
        #nodata=np.ones(int(rays*((360/sector)-1))*bins)*255
        nodata=np.zeros(int(rays*((360/sector)-1))*bins)
        nodata=np.reshape(nodata, (int(rays*((360/(sector)-1))),bins))

        #This is the conversion between 8 bits data (0-254) and reflectivity (0-100)
        data_ = what["offset"]+(what["gain"])*(raw[
            "dataset%d/data2/data" % (a + 1)])#-what["offset"]+(what["gain"])*(second_clutter[
                #"dataset%d/data2/data" % (a + 3)])        
        
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
    maxrange = 30000. #This range is radius. Popo's crater is at 11000. Furuno max range is 70000 in radius
    minelev = 3.1     #minimum elevation angle set up by scan strategy
    maxelev = 28.     #maximum elevation angle set up by scan strategy
    minalt = 5000.    #minimum altitude maxrange*sin(minelev)
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
                                   levels=range(1, 57), #This is the reflectivity scale
                                   #levels=range(0, 95), #Maximum 95
                                   title='{0} {1} local, {2} {3} GMT'.format(date,time,dateGMT,timeGMT)) #title in the graph
                                   #saveto='C:/Users/radar1/Desktop/20220909_070000/plots/VCAPPI_{0}'.format(file[0])) #name of the file

print("Whole program took:", dt.datetime.now() - tprogram)