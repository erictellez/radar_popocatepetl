# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 12:07:06 2021

@author: Eric Tellez

This software is to obtain the ash concentration from the radar reflectivity
using the equations of Marzano and Vulpiani 
The software uses the ODIM_H5 .h5 data.


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

#Make the computational filter to calculate ashes
#Using VARR proposed by Marzano et al.
#This calculations use single polarization radar observables
#Make sure to make the corrections for dual polarization VARR-Px

import wradlib as wrl
import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as pl
import math
import h5py   #to read h5py archives
#import pandas as pd  #This is to save the file in csv
import numpy as np
from scipy.integrate import trapz #to numerical integration
from scipy.special import gamma, factorial
import xarray as xr
try: 
    get_ipython().magic("matplotlib inline")
except:
    pl.ionn()

###################################
#Load H5 files 

#fpath = 'radar_data_examples/explosiones/20210917_054230/ODIM_H5/0087_20210917_054313.h5' # Remember that we already defined the main path
fpath = 'radar_data_examples/explosiones/20210917_054230/ODIM_H5/0087_20210917_054230.h5' # Remember that we already defined the main path

#fpath = 'radar_data_examples/explosiones/20210915_044742/ODIM_H5/0087_20210915_045031.h5' # Remember that we already defined the main path
f = wrl.util.get_wradlib_data_file(fpath)
fcontent = wrl.io.read_opera_hdf5(f)

# which keywords can be used to access the content?
# print(fcontent.keys())
# print the entire content including values of data and metadata
# (numpy arrays will not be entirely printed)
# print(fcontent['dataset1/data2/data'])

"""
Remember that the dataset1/data1/data corresponds 
to elevation_angle/meteorological_parameter/data.
dataset1=3.1 and data2=dBz

dataset#/how contains the elevation angle and the azimuth angle 
of each measurement and that corresponds to X axis of the reflectivity 
data labeled with rays
fcontent['dataset#/how']['elangles'] elevation angles
"""

nbins=fcontent['dataset1/where']['nbins']  #total bins in the radial direction
nrays=fcontent['dataset1/where']['nrays']  #total bins in the azimuth direction
print(nbins)
print(nrays)

#To get the maximum range in x
maximumrange=fcontent['dataset1/where']['nbins']*fcontent['dataset1/where']['rscale']
print(maximumrange)

type(fcontent['dataset1/how']) #This is a dictionary
type(fcontent['dataset1/how']['startazA']) #This is an array with azimuth angles
type(fcontent['dataset1/data2/data']) #This is an array
type(fcontent['where']) #This is a dictionary with (altitude,latitude,longitude)
type(fcontent['where']['lon']) #This is an array with only one entry: longitude

"""
########################################
First attempt
VARR method single polarization
Marzano y VUlpiani Paper
Volcanic Ash Cloud Retrieval by Ground-Based
Microwave Weather Radar

I have to research for this quantity 
and also I have to write down the reference.

This paper 
It is possible that the answer is in the Alatorre paper.
Alatorre-Ibargüengoitia, M. A., Arciniega-Ceballos, A., Linares López, C., Dingwell, D. B., Delgado-Granados, H., Alatorre-Ibargüengoitia, M. A., Arciniega-Ceballos, A., Linares López, C., Dingwell, D. B., & Delgado-Granados, H. (2019). Fragmentation behavior of eruptive products of Popocatépetl volcano: An experimental contribution. Geofísica Internacional, 58(1), 49–72.
Aproximately 2567 kg/m3 = 2567000 g/m3 but this is for dense rock
Another value for less dense ashes is 610 kg/m3=610000 g/m3

rhoa is the density of the ash (in grams per cubic meter) (empirical)

rhoa=610000

I have to research for this quantity
and also I have to write down the reference.
Dm is the number-weighted mean diameter of the ash (in milimeters)
Dm=c*(DBZa^d)*C

va(D)=av*D^(bv) is the terminal fall ash velocity (in meters per second)
wup is the vertical component of the air speed
av and bv are empirical coefficients

#Ca is the mass concentration (in grams per cubic meter)
#Ra is the ashfall rate (in kilograms per hour per square meter)
"""
#rhoa=610

#With the St. Helens data (Harris & Rose, 1983)
#in meters*s-1
#av=5.558
#bv=0.722

#with the wilson's data (5-10 km height) 
#av=7.460
#bv=1.0

#fcontent['dataset1/data2/data'] is the measured reflectivity


"""
I have to build a netCDF file with all the angles and only the refelctivity
"""

#Ca = 3.21*(10**(5))*(rhoa/Dm**3)*fcontent['dataset1/data2/data']
#Ra = 2.03*(10**(-4))*(av*rhoa/Dm**(3+bv))*fcontent['dataset1/data2/data']
#print(Ca)
#print(Ra)

#Ca31 = 3.21*10e-5*(rhoa/Dn^3)*fcontent['dataset1/data2/data']
#Ra31 = 2.03*10e-4*(av*rhoa/Dn^(3+bv))*fcontent['dataset1/data2/data']

#Ca45 = 3.21*10e-5*(rhoa/Dn^3)*fcontent['dataset2/data2/data']
#Ra45 = 2.03*10e-4*(av*rhoa/Dn^(3+bv))*fcontent['dataset2/data2/data']

#Ca60 = 3.21*10e-5*(rhoa/Dn^3)*fcontent['dataset3/data2/data']
#Ra60 = 2.03*10e-4*(av*rhoa/Dn^(3+bv))*fcontent['dataset3/data2/data']

#Ca82 = 3.21*10e-5*(rhoa/Dn^3)*fcontent['dataset4/data2/data']
#Ra82 = 2.03*10e-4*(av*rhoa/Dn^(3+bv))*fcontent['dataset4/data2/data']

#Ca110 = 3.21*10e-5*(rhoa/Dn^3)*fcontent['dataset5/data2/data']
#Ra110 = 2.03*10e-4*(av*rhoa/Dn^(3+bv))*fcontent['dataset5/data2/data']

#Ca140 = 3.21*10e-5*(rhoa/Dn^3)*fcontent['dataset6/data2/data']
#Ra140 = 2.03*10e-4*(av*rhoa/Dn^(3+bv))*fcontent['dataset6/data2/data']

#Ca180 = 3.21*10e-5*(rhoa/Dn^3)*fcontent['dataset7/data2/data']
#Ra180 = 2.03*10e-4*(av*rhoa/Dn^(3+bv))*fcontent['dataset7/data2/data']

#Ca280 = 3.21*10e-5*(rhoa/Dn^3)*fcontent['dataset8/data2/data']
#Ra280 = 2.03*10e-4*(av*rhoa/Dn^(3+bv))*fcontent['dataset8/data2/data']


###############################################################
"""
From Vulpiani, Ripepe, Valade paper
Mass discharge rate retrieval combining weather radar 
and thermal camera observations

#Here I have to set a cycle 
#for i in range(8)
    #DBZ%d = fcontent["dataset%d/data2/data" % (i + 1)]

#ash equivalent reflectivity because radar is calibrated assuming 
#the dielectric factor of water 
DBZa1=fcontent['dataset1/data2/data']-202+3.77 #aproximately 202 is the maximum
#It is possible that 202 is a god number since it hits the volcano
DBZa2=fcontent['dataset2/data2/data']+3.77
DBZa3=fcontent['dataset3/data2/data']+3.77
DBZa4=fcontent['dataset4/data2/data']-154+3.77 #154 is the maxiun before the explosion and 169 is the maximun during explosion
DBZa5=fcontent['dataset5/data2/data']+3.77
DBZa6=fcontent['dataset6/data2/data']+3.77
DBZa7=fcontent['dataset7/data2/data']+3.77
DBZa8=fcontent['dataset8/data2/data']+3.77
"""
#Rate=fcontent['dataset4/data1/data']
DBZ=fcontent['dataset4/data2/data']
#Vrad=fcontent['dataset4/data3/data']
#Zdr=fcontent['dataset4/data4/data']
KDP=fcontent['dataset4/data5/data']
#phidp=fcontent['dataset4/data6/data']
#rhohv=fcontent['dataset4/data7/data']
#Wrad= fcontent['dataset4/data8/data']

#It seems that the reflectivity of the ash is 154
#3.77 is the difference in the dialectric constant 
#DBZa=DBZ-154+3.77 #We can visualize the plot better with this one
DBZa=np.subtract(DBZ,150.33) #154 is a provisional number, a maximum reflectivity withouth the ashes

#I need to see if a distribution of the density of the ash plume over the crater is gaussian.
#Or what kind of distribution it has.

a0=0.18
b=0.27

#a=rhoa*a0
a=1.5*a0
c=0.585
d=0.311
e=-0.313

Ca=a*DBZa**b
Dm=c*(DBZa**d)*Ca**e  #Assuming the particles are spheres
print(Ca)
print(Dm)
print(DBZa)
#DF=pd.DataFrame(DBZ)
#DF.to_csv("DBZ.csv") #to save in csv file

"""
#Retrieval of the Mass Discharge Rate
av=62.6
bv=0.5
mu=1
wup=1   #research this quantity from the videos of cenapred

#flux density
jm=math.cos(fcontent['dataset1/where']['elangle'])*Ca*(wup-((gamma(4+bv+mu))/(((mu+1)**bv)*factorial(3+mu)))*av*Dm**bv)
#print(jm)

#Mass discharge rate
#With the data just above the volcano vent with can calculate the MDR 
#because all the mass passes thru this angular section

#To compute the integral
#MDR=Double integral of jm rdrdphi
LimiteBajoRadio=0
LimiteAltoRadio=nbins
n=100
r=np.linspace(LimiteBajoRadio,LimiteAltoRadio,n)
I_trapz1=trapz(jm,r)

LimiteBajoAngulo=fcontent['dataset1/how']['startazA'][0]
LimiteAltoAngulo=fcontent['dataset1/how']['startazA'][nrays-1]
n=100
phi=np.linspace(LimiteBajoAngulo,LimiteAltoAngulo,n)
I_trapz2=trapz(I_trapz1,phi)
"""


#There exists a moment in time with wind=0 or close to zero when
#we can calculate all the mass of the ash cloud
#Total mass discharge
#TMD= triple integral of jm


"""
Ca1=a*DBZa1**b
Dm1=c*(DBZa1**d)*Ca1**e
Ca2=a*DBZa2**b
Dm2=c*(DBZa2**d)*Ca2**e
Ca3=a*DBZa3**b
Dm3=c*(DBZa3**d)*Ca3**e
Ca4=a*DBZa4**b
Dm4=c*(DBZa4**d)*Ca4**e
Ca5=a*DBZa5**b
Dm5=c*(DBZa5**d)*Ca5**e
Ca6=a*DBZa6**b
Dm6=c*(DBZa6**d)*Ca6**e
Ca7=a*DBZa7**b
Dm7=c*(DBZa7**d)*Ca7**e
Ca8=a*DBZa8**b
Dm8=c*(DBZa8**d)*Ca8**e
"""

# Coordinates are always the same
# (longitude,latitude,altitude)
#sitio=(-98.65487,19.11921,4007.0)
sitio=(fcontent['where']['lon'], #This form is more general
       fcontent['where']['lat'],
       fcontent['where']['height'])

#plot Dm
fig = pl.figure(figsize=(10, 10))
im = wrl.vis.plot_ppi(Dm,
                      rf=1/fcontent['dataset1/where']['rscale'],
                      az=fcontent['dataset1/how']['startazA'],
                      fig=fig,
                      proj=None) #Plot

#Plot Ca
fig = pl.figure(figsize=(10, 10))
im = wrl.vis.plot_ppi(Ca,
                      rf=1/fcontent['dataset1/where']['rscale'],
                      az=fcontent['dataset1/how']['startazA'],
                      fig=fig,
                      proj=None) #Plot

#plot DBZa mm6/mm3
fig = pl.figure(figsize=(10, 10))
im = wrl.vis.plot_ppi(DBZa,
                      rf=1/fcontent['dataset1/where']['rscale'],
                      az=fcontent['dataset1/how']['startazA'],
                      fig=fig,
                      proj=None) #Plot
"""
#plot DBZa mm6/mm3
fig = pl.figure(figsize=(10, 10))
im = wrl.vis.plot_ppi(DBZa,
                      rf=1/fcontent['dataset1/where']['rscale'],
                      az=fcontent['dataset1/how']['startazA'],
                      fig=fig,
                      proj='cg') #Plot with curvilinear grid axes


#plot Rate of rain mm/h
fig = pl.figure(figsize=(10, 10))
im = wrl.vis.plot_ppi(Rate,
                      rf=1/fcontent['dataset1/where']['rscale'],
                      az=fcontent['dataset1/how']['startazA'],
                      fig=fig,
                      proj=None) #Plot
"""

#plot KDP
fig = pl.figure(figsize=(10, 10))
im = wrl.vis.plot_ppi(KDP,
                      rf=1/fcontent['dataset1/where']['rscale'],
                      az=fcontent['dataset1/how']['startazA'],
                      fig=fig,
                      proj=None) #Plot
###############################################################