# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 17:09:44 2022

@author: Eric Tellez

Ground clutter
This program is to take out the ground in the reflectivity profile

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
import matplotlib.pyplot as pl
import os
import glob
from osgeo import osr
import warnings
warnings.filterwarnings('ignore')


# define your cartesian reference system
# For Mexico City: https://epsg.io/?q=Mexico
proj = osr.SpatialReference()
proj.ImportFromEPSG(6371)

#To import files automatically
path= 'D:/ODIM_H5/**/*.h5'
list_of_files=glob.glob(path, recursive=True)
newest_file = max(list_of_files, key=os.path.getctime)
filename_with_path = wradlib.util.get_wradlib_data_file(newest_file)
raw = wradlib.io.read_opera_hdf5(filename_with_path)

#To get the name of the file and paste it into the name of the plots
filename = os.path.basename(filename_with_path) #Filename with extension
file = os.path.splitext(filename)  #Tuple of string with filename and extension

#rawclutter is the file without the explosion

for i in range(10):  #This number has to change if the number of elevation angle changes
    
    angle=raw["dataset%d/data2/what" % (i + 1)]["offset"] +(raw["dataset%d/data2/what" % (i + 1)]["gain"])*raw["dataset%d/data2/data" % (i + 1)]

    #Coordinates
    sitecoords = (raw["where"]["lon"], 
                  raw["where"]["lat"],
                  raw["where"]["height"])

    #elevation angle (very important)
    elangle = raw['dataset%d/where' % (i + 1)]['elangle'] #to obtain the elevation angle
    azimuth = raw['dataset%d/how' % (i + 1)]['startazA'] #to obtain all the azimuth angles
    rscale= raw['dataset%d/where' % (i + 1)]['rscale'] #to obtain the conversion factor of the distance


    #date and time is almost the same as the name of the archive
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

    """
    #Magaldi
    clutter = wradlib.clutter.filter_gabella(angle, tr1=12, n_p=6, tr2=1.1)
    ac1 += clutter
    data_no_clutter = wradlib.ipol.interpolate_polar(angle, clutter)



    """
    fig = pl.figure(figsize=(12,6))
    fig.suptitle('{} {} Local, {} {} GMT \n Ángulo de elevación {}°'.format(date,time,dateGMT,timeGMT,elangle), fontsize=20)

    clmap = wradlib.clutter.filter_gabella(angle,
                                           wsize=5,   #Average of the pixels, good number 5
                                           thrsnorain=0.0, # 
                                           tr1=12, #Good number 12
                                           n_p=8,  #Good number 8
                                           tr2=1.3,  #Good number for ground clutter 3, good number to take out pollution? maybe 7
                                           radial=False,
                                           cartesian=False)
    
    
    ax = fig.add_subplot(131)
    ax, pm = wradlib.vis.plot_ppi(angle[:,0:200], 
                                  #angle,
                                  #reflectivity,
                                  rf= 1/rscale,
                                  az= azimuth,
                                  elev= elangle,
                                  fig= fig,
                                  site= sitecoords,
                                  #proj='cg', #Another type of projection
                                  proj= proj, #Plot
                                  ax=ax,
                                  func='pcolormesh')
    
    xlabel = ax.set_xlabel('distancia [m]')
    ylabel = ax.set_ylabel('distancia [m]')
    title = ax.set_title('Reflectivity DBZH [dBz]')
    cb = pl.colorbar(pm, ax=ax)
    
    ax = fig.add_subplot(132)
    ax, pm = wradlib.vis.plot_ppi(clmap[:,0:200], 
                                  #clmap,
                                  #reflectivity,
                                  rf= 1/rscale,
                                  az= azimuth,
                                  elev= elangle,
                                  fig= fig,
                                  site= sitecoords,
                                  #proj='cg', #Another type of projection
                                  proj= proj, #Plot
                                  ax=ax,
                                  func='pcolormesh')
    
    xlabel = ax.set_xlabel('distancia [m]')
    ylabel = ax.set_ylabel('distancia [m]')
    title = ax.set_title('Cluttermap DBZH [dBz]')
    cb = pl.colorbar(pm, ax=ax)
    
    data_no_clutter = wradlib.ipol.interpolate_polar(angle, clmap)
    
    ax = fig.add_subplot(133)
    ax, pm = wradlib.vis.plot_ppi(data_no_clutter[:,0:200], 
                                  #data_no_clutter,
                                  #reflectivity,
                                  rf= 1/rscale,
                                  az= azimuth,
                                  elev= elangle,
                                  fig= fig,
                                  site= sitecoords,
                                  #proj='cg', #Another type of projection
                                  proj= proj, #Plot
                                  ax=ax,
                                  func='pcolormesh')
    
    xlabel = ax.set_xlabel('distancia [m]')
    ylabel = ax.set_ylabel('distancia [m]')
    title = ax.set_title('Data no clutter DBZH [dBz]')
    cb = pl.colorbar(pm, ax=ax)
    
    #folder_clutter='D:/Carpeta_Imag/clutter/'
    #fig.savefig(folder_clutter + file[0] + '_clutter%d' % (i)',dpi=100)  #To save the plot as an image
    
    
    """
    #################################################
    #################################################
    # Fuzzy clasification Crisologo 2015, Vulpiani 2012
    
    dat={}
    dat["ref"] = raw["dataset7/data2/what"]["offset"] +(raw["dataset7/data2/what"]["gain"])*raw["dataset7/data2/data"]
    dat["dop"] = raw["dataset7/data3/what"]["offset"] +(raw["dataset7/data3/what"]["gain"])*raw["dataset7/data3/data"]
    dat["zdr"] = raw["dataset7/data4/what"]["offset"] +(raw["dataset7/data4/what"]["gain"])*raw["dataset7/data4/data"]
    #KDP_propagation_phase_difference_rate_of_change=raw["dataset7/data5/what"]["offset"] +(raw["dataset7/data5/what"]["gain"])*raw["dataset7/data5/data"]
    dat["phi"] = raw["dataset7/data6/what"]["offset"] +(raw["dataset7/data6/what"]["gain"])*raw["dataset7/data6/data"]
    dat["rho"] = raw["dataset7/data7/what"]["offset"] +(raw["dataset7/data7/what"]["gain"])*raw["dataset7/data7/data"]
    dat["map"] = wradlib.io.read_opera_hdf5(filenameclutter3)
    #WRAD_doppler_velocity_spectrum_width=raw["dataset7/data8/what"]["offset"] +(raw["dataset7/data8/what"]["gain"])*raw["dataset7/data8/data"]
    
    print(dat.keys())
    weights = {"zdr": 0.4,
               "rho": 0.4,
               "rho2": 0.4,
               "phi": 0.1,
               "dop": 0.1,
               "map": 0.5
               }
    cmap, nanmask = wradlib.clutter.classify_echo_fuzzy(dat,
                                                        weights=weights,
                                                        thresh=0.5)
    
    fig = pl.figure(figsize=(18,16))
    
    #   Horizontal reflectivity
    ax = pl.subplot(121, aspect="equal")
    ax, pm = wradlib.vis.plot_ppi(np.ma.masked_invalid(dat["ref"]), ax=ax)
    ax = wradlib.vis.plot_ppi_crosshair(site=(0,0,0),
                                        ranges=[80,160,240])
    pl.xlim(-240,240)
    pl.ylim(-240,240)
    pl.xlabel("# bins from radar")
    pl.ylabel("# bins from radar")
    cbar = pl.colorbar(pm, shrink=0.3)
    cbar.set_label("dBZ", fontsize = "large")
    
    #   Echo classification
    ax = pl.subplot(122, aspect="equal")
    ax, pm = wradlib.vis.plot_ppi(np.ma.masked_array(cmap.astype(np.uint8),
                                                     np.isnan(dat["ref"])),
                                  ax=ax, cmap="bwr")
    ax = wradlib.vis.plot_ppi_crosshair(site=(0,0,0),
                                        ranges=[80,160,240])
    pl.xlim(-240,240)
    pl.ylim(-240,240)
    pl.xlabel("# bins from radar")
    pl.ylabel("# bins from radar")
    cbar = pl.colorbar(pm, shrink=0.3)
    cbar.set_label("meterol. echo=0 - non-meteorol. echo=1",
                   fontsize = "large")
    """
    