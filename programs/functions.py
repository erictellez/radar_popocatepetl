# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 14:12:24 2022

@author: Eric Tellez
"""


def open_all_angles(file, phys_variable):
    
    #open file
    filename = wradlib.util.get_wradlib_data_file('radar_data_examples/Explosiones/20200722_151800/0087_20200722_150000.h5')
    raw = wradlib.io.read_opera_hdf5(filename)
    
    #define the dictionary for the physical variables
    phys_variable = {
        "RATE":1,
        "reflectivity":2,
        ""}


    if phys_variable in raw.keys():
        raw[phys_variable] = 'RATE' 
        for i in range(8):
            what = raw["dataset%d/data1/what" % (i + 1)]
            angle = what["offset"] +(what["gain"])*(raw[
            "dataset%d/data1/data" % (i + 1)])
    if phys_variable in raw.keys():
        raw[phys_variable] = 'RATE'



def plot_all_angles():
    
    
def open_all_physical_variables():
    
    
    
def plot_all_physical_variables():