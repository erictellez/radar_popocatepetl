# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 11:21:23 2022

@author: Eric Tellez

Ground clutter
This program is to take out the ground in the refelctivity profile

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
import numpy as np
import os
import glob
from osgeo import osr
import warnings
warnings.filterwarnings('ignore')
try:
    get_ipython().magic("matplotlib inline")
except:
    pl.ion()

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


#rawclutter is the file without the explosion
#The more data the better
filenameclutter =wradlib.util.get_wradlib_data_file('explosiones/20210915_044742/ODIM_H5/0087_20210915_044742.h5') 
rawclutter1 = wradlib.io.read_opera_hdf5(filenameclutter)
filenameclutter2 =wradlib.util.get_wradlib_data_file('explosiones/20210915_044742/ODIM_H5/0087_20210915_044824.h5')
rawclutter2 = wradlib.io.read_opera_hdf5(filenameclutter2)
filenameclutter3 =wradlib.util.get_wradlib_data_file('explosiones/20210915_044742/ODIM_H5/0087_20210915_044949.h5')
rawclutter3 = wradlib.io.read_opera_hdf5(filenameclutter3)

#to average the ground clutter
rawclutteraverage=(rawclutter1[
    "dataset1/data2/data"]+rawclutter2[
    "dataset1/data2/data"]+rawclutter3[
    "dataset1/data2/data"])/3


filename = wradlib.util.get_wradlib_data_file('explosiones/20210915_044742/ODIM_H5/0087_20210915_045031.h5')
raw = wradlib.io.read_opera_hdf5(filename)
angle=raw["dataset1/data2/what"]["offset"] +(raw[
    "dataset1/data2/what"]["gain"])*(raw["dataset1/data2/data"]-rawclutteraverage)

#Coordinates
sitecoords = (raw["where"]["lon"], 
              raw["where"]["lat"],
              raw["where"]["height"])

azimuth = raw['dataset1/how']['startazA'] #to obtain all the azimuth angles
elangle = raw['dataset1/how']['elangles']
rscale= raw['dataset1/where']['rscale']

"""
#Magaldi
clutter = wradlib.clutter.filter_gabella(angle, tr1=12, n_p=6, tr2=1.1)
ac1 += clutter
data_no_clutter = wradlib.ipol.interpolate_polar(angle, clutter)



"""
clmap = wradlib.clutter.filter_gabella(angle,
                                       wsize=5,
                                       thrsnorain=0.,
                                       tr1=6.,
                                       n_p=8,
                                       tr2=1.3,
                                       radial=False,
                                       cartesian=False)

fig = pl.figure(figsize=(12,8))
ax = fig.add_subplot(121)
ax, pm = wradlib.vis.plot_ppi(angle[:,0:200], 
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

ax = fig.add_subplot(122)
ax, pm = wradlib.vis.plot_ppi(clmap[:,0:200], 
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
"""
#########################################################
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