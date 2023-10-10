# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 14:59:02 2022

@author: Eric Tellez

This program is to make an alert when the radar detect explosion
"""

import wradlib
import numpy
import winsound

#nrays is x (rows) angle, nbins is y (columns) radius
#the center of the crater is at x-143 and y-153 pixels moreless two pixels
#Because each pixel represents 75 meters in y, then the crater is at 153*75=11475 meters
 
#Conversion of scale to match 0-95 in the scale of reflectivity



if nray>:
    
    winsound.Beep(440,500)