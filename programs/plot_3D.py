# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 00:40:48 2022

@author: Eric Tellez

Plot 3D spherical coordinates


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
import numpy
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as axes3d

x=volume_reflectivity[0]*numpy.sin(volume_reflectivity[2])*numpy.cos(volume_reflectivity[1])
y=volume_reflectivity[0]*numpy.sin(volume_reflectivity[2])*numpy.sin(volume_reflectivity[1])
z=volume_reflectivity[0]*numpy.cos(volume_reflectivity[2])

ax = pl.axes(projection='3d')
ax.scatter(x, y, z, c=z, cmap='viridis', linewidth=0.5);
ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap='viridis', edgecolor='none');
