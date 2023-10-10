# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 21:28:59 2022

@author: radar1
"""

"""
Created on Wed Sep 21 17:51:57 2022

@author: radar1
"""

# Author: Jonathan J. Helmus (jhelmus@anl.gov)
# License: BSD 3 clause

import matplotlib.pyplot as plt
import pyart
from pyart.testing import get_test_data
import glob
import os
import _netCDF4

#To import files automatically
#path= 'D:/explosiones/20210915_232800GMT/CFRadial1/*.nc'
#list_of_files=glob.glob(path, recursive=True)
#all_files=len(list_of_files)

# Read the data, a cfradial file
filename = get_test_data('D:/explosiones/20210915_232800GMT/CFRadial1/*.nc')
radar = pyart.io.read(filename)

# Create a cross section at 225 and 270 degrees azimuth
xsect = pyart.util.cross_section_ppi(radar, [150, 180])

# Set the colorbar label
colorbar_label = 'Equivalent \n reflectivity factor \n (dBZ)'

display = pyart.graph.RadarDisplay(xsect)
fig = plt.figure()
ax1 = fig.add_subplot(211)
display.plot('reflectivity_horizontal', 0, vmin=-32, vmax=64., colorbar_label=colorbar_label)
plt.ylim(0, 15)
ax2 = fig.add_subplot(212)
display.plot('reflectivity_horizontal', 1, vmin=-32, vmax=64., colorbar_label=colorbar_label)
plt.ylim(0, 15)

plt.tight_layout()
plt.show()