# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 20:13:47 2022

@author: Eric Tellez

Entropy
"""

import wradlib
import matplotlib.pyplot as pl
import os
from osgeo import osr
import glob
import numpy
import warnings
warnings.filterwarnings('ignore')
from skimage.io import imread, imshow
from skimage import data
from skimage.util import img_as_ubyte
from skimage.filters.rank import entropy
from skimage.morphology import disk
from skimage.color import rgb2hsv, rgb2gray, rgb2yuv

