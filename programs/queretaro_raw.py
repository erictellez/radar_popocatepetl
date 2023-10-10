# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 18:49:11 2023

@author: Eric Téllez

Software para leer los datos del radar de Querétaro
que estén en formato de Visala Sigment Iris

"""

import wradlib
import matplotlib.pyplot as pl
import numpy

fpath = "D:/Qro/RAW_NA_000_236_20151226053654" #Ruta de los archivos
f = wradlib.util.get_wradlib_data_file(fpath)
fcontent = wradlib.io.read_iris(f, keep_old_sweep_data=True)

# Imprime las llaves principales del archivo
print(fcontent.keys())
print()  #Dejé dos espacios para visualizar mejor
print()

#Estas llaves las saqué a partir de las llaves principales del archivo
#print(fcontent["product_hdr"].keys())  #Diccionario
#print()
#print(fcontent["product_hdr"]["structure_header"].keys())  #Diccionario
#Si se necesitan más llaves hay que seguir la estructura anterior, 
#por ejemplo la llave "structure_header" está dentro de la llave "product_hdr"
#Si arroja un error la llave hay que ver que no sea un número entero u otra cosa

#print(fcontent["product_type"]) #RAW y CAPPI, no sé si haya más tipos de archivo
#print()
#print(fcontent["ingest_header"].keys())   #Llaves de diccionario
#print() 
print(fcontent["nsweeps"])  #Número entero
print()
#print(fcontent["nrays"])  #Número entero
#print()
#print(fcontent["nbins"])  #Número entero
#print()
#print(fcontent["data_types"]) #Cadenas, son 3
#print()
print(fcontent["data"].keys()) #Llaves con una etiqueta con el número 3
print()
#print(fcontent["raw_product_bhdrs"])
#print()
print(fcontent["data"][3].keys()) #Llave
print()


print(fcontent["data"][3]["ingest_data_hdrs"].keys())  #Llave
print(fcontent["data"][3]["ingest_data_hdrs"]["DB_DBZ"]) #Diccionario ordenado
print()
print(fcontent["data"][3]["sweep_data"].keys())
print()
print(fcontent["data"][3]["sweep_data"]["DB_DBZ"]) #Este diccionario son los datos
print()
print()

D= fcontent["data"][3]["sweep_data"]["DB_DBZ"]

a=[]
for i in D.keys():
  a+=[[i,sum(D[i])]]


filename = 'datos.txt'
outfile = open(filename, 'w')
outfile.writelines([str(i)+'\n' for i in a])
outfile.close()

fig = pl.figure(figsize=(10, 10))
swp = fcontent["data"][3]["sweep_data"]
ax, im = wradlib.vis.plot_ppi(swp["DB_DBT"]["data"], fig=fig, proj="cg")

fig = pl.figure(figsize=(10, 10))
swp = fcontent["data"][3]["sweep_data"]
ax, im = wradlib.vis.plot_ppi(swp["DB_DBZ"]["data"], fig=fig, proj="cg")

fig = pl.figure(figsize=(10, 10))
swp = fcontent["data"][3]["sweep_data"]
ax, im = wradlib.vis.plot_ppi(swp["DB_VEL"]["data"], fig=fig, proj="cg")
