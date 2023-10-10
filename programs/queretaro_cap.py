# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 19:17:59 2023

@author: Eric Tellez

Programa para leer los datos del radar de Querétaro,
formato CAPPI de Visala Sigment Iris
"""

import wradlib 
import matplotlib.pyplot as pl
import numpy

fpath = "D:/Qro/CAP_Z_030_240_20180701034506"
f = wradlib.util.get_wradlib_data_file(fpath)
fcontent = wradlib.io.read_iris(f, keep_old_sweep_data=False)

# Llaves principales
print(fcontent.keys())
print()
print()

print(fcontent["product_hdr"].keys())
print()
print(fcontent["product_hdr"]["structure_header"].keys()) # 4 llaves
print()
print(fcontent["product_hdr"]["product_configuration"].keys()) # 33 llaves
print()
print(fcontent["product_hdr"]["product_end"].keys())  # 55 llaves
print()


print(fcontent["product_type"]) #string
print()
print(fcontent["nbins"]) #entero
print()
print(fcontent["data"].keys()) #Llave de diccionario número 0
print()
#print(fcontent["data"][0]) #Numpy array
#print()

print(fcontent["data"][0].shape) #Tamaño de la matriz de datos
print()
print(type(fcontent["data"][0].shape))  #Tipo de datos
print()

"""
#Parece que se necesita la función de vol-cappi

# generate 3-D Cartesian target grid coordinates
maxrange = 30000. #This range is radius. Popo's crater is at 11000. Furuno max range is 70000 in radius
minelev = 0.0     #minimum elevation angle set up by scan strategy
maxelev = 28.     #maximum elevation angle set up by scan strategy
minalt = 4000.    #minimum altitude maxrange*sin(minelev)
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
   

# diagnostic plot
trgx = trgxyz[:, 0].reshape(trgshape)[0, 0, :]
trgy = trgxyz[:, 1].reshape(trgshape)[0, :, 0]
trgz = trgxyz[:, 2].reshape(trgshape)[:, 0, 0]

fig = pl.figure(figsize=(10, 10))
swp = fcontent["data"][0]
ax, im = wradlib.vis.plot_max_plan_and_vert(trgx,trgy,trgz,swp)
"""