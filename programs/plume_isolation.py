# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 20:37:08 2022

@author: Eric Tellez

Isolation of the plume by pixels

"""

import wradlib
import numpy
from osgeo import osr

# define your cartesian reference system
# For Mexico City: https://epsg.io/?q=Mexico
proj = osr.SpatialReference()
proj.ImportFromEPSG(6371)


filename = wradlib.util.get_wradlib_data_file('radar_data_examples/Explosiones/20210915_044742/ODIM_H5/0087_20210915_045403.h5')
#filename = wradlib.util.get_wradlib_data_file('radar_data_examples/Explosiones/20200722_151800/0087_20200722_153000.h5')
raw = wradlib.io.read_opera_hdf5(filename)

#RATE_rainfall_intensity=raw['dataset4/data1/data'] #This dataset is not that important
DBZH_horizontal_reflectivity=raw["dataset5/data2/what"]["offset"] +(raw["dataset5/data2/what"]["gain"])*raw["dataset5/data2/data"]
VRAD_radial_velocity=raw["dataset5/data1/what"]["offset"] +(raw["dataset5/data3/what"]["gain"])*raw["dataset5/data3/data"]
ZDR_reflection_factor_difference=raw["dataset5/data4/what"]["offset"] +(raw["dataset5/data4/what"]["gain"])*raw["dataset5/data4/data"]
KDP_propagation_phase_difference_rate_of_change=raw["dataset5/data5/what"]["offset"] +(raw["dataset5/data5/what"]["gain"])*raw["dataset5/data5/data"]
PHIDP_differential_propagation_phase=raw["dataset5/data6/what"]["offset"] +(raw["dataset5/data6/what"]["gain"])*raw["dataset5/data6/data"]
RHOHV_copolar_correlation_coefficient=raw["dataset5/data7/what"]["offset"] +(raw["dataset5/data7/what"]["gain"])*raw["dataset5/data7/data"]
WRAD_doppler_velocity_spectrum_width=raw["dataset5/data8/what"]["offset"] +(raw["dataset5/data8/what"]["gain"])*raw["dataset5/data8/data"]
#raw['dataset4/data9/data'] #I dont know what this dataset means

# I have to inspect every pixel
# first the pixels of the Vrad must be random values because is a turbulent flow
for pixel_angle in range(VRAD_radial_velocity):
    for pixel_radius in range(VRAD_radial_velocity):
        for pixel_height in range():
            if Vrad[pixelangle]-Vrad[pixelangle+1]-Vrad