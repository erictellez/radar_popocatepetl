# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 21:13:25 2023

@author: Eric Tellez

Plot the data over the Popocatepetl volcano map region
"""

import wradlib
import numpy as np
from matplotlib import pyplot as pl

pl.rcParams["figure.figsize"] = [7.00, 3.50]
pl.rcParams["figure.autolayout"] = True
im = pl.imread("map_popo.jpg")
fig, ax = pl.subplots()
im = ax.imshow(im, extent=[0, 300, 0, 300])
x = np.array(range(300))
#ax.plot(x, x, ls='dotted', linewidth=2, color='red')
#plt.show()



fig = pl.figure(figsize=(20,10))
ax = fig.add_subplot(241)
ax, pm = wradlib.vis.plot_ppi(DBZH_clutter,#[:,0:200], 
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
