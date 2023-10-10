# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 12:46:01 2022

@author: Eric Tellez

Program to calculate the initial velocity of the explosion with a system of equations
of Torricelli equation
The program acquires the change in altitude and the change in time of the explosion
from the data. 


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


def initialvelocity(deltaT,deltaY):

    #deltaT is change in time from the beggining of the explosion until the maximum altitude
    #deltaY is change in altitude from the border of the crater to the maximum altitude
    #viy is initial velocity in y
    #Assuming that the explosion is always vertical in the first seconds and
    #the final velocity is always zero in the y direction (vfy=0) because it reach a maximum

    #vfy=viy+acceleration*deltaT
    #0=viy+acceleration*deltaT
    acceleration=2*deltaY/(deltaT^2) #time dependent

    #Now using the Torricelli equation
    viy=2*deltaY/deltaT

    return (viy, acceleration)

def kineticenergy():
    
    #program to calculate the kinetic energy of the explosion
    E=(m*viy^2)/2