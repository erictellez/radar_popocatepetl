# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 16:44:01 2022

@author: Eric Tellez

This program is to generate and visualize all the variables from the main physical variables
Standard deviation of every variable
Texture of every variable
First derivative
Second derivative
"""

#import numpy
#import 
for all_files

for i in range(10): #Number of angles
#RATE_rainfall_intensity=raw["dataset%d/data1/what"%(i+3)]["offset"] +(raw["dataset%d/data1/what"%(i+3)]["gain"])*raw["dataset%d/data1/data"%(i+3)] #This dataset is not that important
DBZH_horizontal_reflectivity=raw["dataset%d/data2/what" % (i+3)]["offset"] +(raw["dataset%d/data2/what"%(i+3)]["gain"])*raw["dataset%d/data2/data"%(i+3)]
VRAD_radial_velocity=raw["dataset%d/data3/what" % (i+3)]["offset"] +(raw["dataset%d/data3/what"%(i+3)]["gain"])*raw["dataset%d/data3/data"%(i+3)]
ZDR_reflection_factor_difference=raw["dataset%d/data4/what" % (i+3)]["offset"] +(raw["dataset%d/data4/what"%(i+3)]["gain"])*raw["dataset%d/data4/data"%(i+3)]
KDP_propagation_phase_difference_rate_of_change=raw["dataset%d/data5/what"%(i+3)]["offset"]+(raw["dataset%d/data5/what"%(i+3)]["gain"])*raw["dataset%d/data5/data"%(i+3)]
PHIDP_differential_propagation_phase=raw["dataset%d/data6/what"%(i+3)]["offset"] +(raw["dataset%d/data6/what"%(i+3)]["gain"])*raw["dataset%d/data6/data"%(i+3)]
RHOHV_copolar_correlation_coefficient=raw["dataset%d/data7/what"%(i+3)]["offset"] +(raw["dataset%d/data7/what"%(i+3)]["gain"])*raw["dataset%d/data7/data"%(i+3)]


#This is standard desviation 
WRAD_doppler_velocity_spectrum_width=raw["dataset%d/data8/what"%(i+3)]["offset"] +(raw["dataset%d/data8/what"%(i+3)]["gain"])*raw["dataset%d/data8/data"%(i+3)]
SD_DBZH
SD_ZDR
SD_KDP
SD_PHIDP
SD_RHOHV

#Texture
# http://hydro.ou.edu/files/publications/2007/A%20Fuzzy%20Logic%20Algorithm%20for%20the%20Separation%20of%20Precipitating%20from%20Nonprecipitating%20Echoes%20Using%20Polarimetric%20Radar%20Observations.pdf
TX_VRAD
TX_DBZH
TX_ZDR
TX_KDP
TX_PHIDP
TX_RHOHV

D1_VRAD
D1_DBZH
D1_ZDR
D1_KDP
D1_PHIDP
D1_RHOHV

D2_VRAD
D2_DBZH
D2_ZDR
D2_KDP
D2_PHIDP
D2_RHOHV