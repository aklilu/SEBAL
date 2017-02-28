# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 09:32:01 2017
Tim Hessels

This script reprojects LANDSAF data (whole MSG disk) and clips to user extend

import is downloaded from: https://landsaf.ipma.pt/ and use the MSG extend

The data name needs to look similar as: HDF5_LSASAF_MSG_DSSF_MSG-Disk_201601101215.bz2
or HDF5_LSASAF_MSG_DSSF_MSG-Disk_201601101215

"""

import os
import subprocess
import shutil

# User parameters
latlim = [26, 37]
lonlim = [-13,2] 
file_name = r"J:\SEBAL_Tadla\LANDSAF\HDF5_LSASAF_MSG_DSSF_MSG-Disk_201601101215.bz2" 

# Get some general data
input_folder = os.path.dirname(file_name)
temp_folder = os.path.join(input_folder, 'Temporary')
if not os.path.exists(temp_folder):
    os.mkdir(temp_folder)
    
output_folder = os.path.dirname(file_name)
input_name = os.path.basename(file_name)
extension = os.path.splitext(input_name)[1]
file_name_only = os.path.splitext(input_name)[0]
file_name_tiff =file_name_only + '.tif'

# unzip bunzipfile if needed 
if str(extension) == '.bz2':
    fullCmd = '7z e %s -o%s' %(file_name,temp_folder)
    process = subprocess.Popen(fullCmd)
    process.wait() 
    input_folder = temp_folder
    
# Set projection of GOES/LANDSAF data
output_GOES_projected = os.path.join(input_folder,'GOES_projected_LANDSAF.tif')    
fullCmd = 'gdal_translate -a_srs  "+proj=geos +a=6378169 +b=6356583.8 +lon_0=0 +h=35785831" -a_ullr -5570248.832537 5570248.832537 5570248.832537 -5570248.832537 HDF5:"%s"://DSSF %s' %(os.path.join(input_folder, file_name_only), output_GOES_projected)
process = subprocess.Popen(fullCmd)
process.wait() 

# Reproject GOES/LANDSAF data and clip data
out_name = os.path.join(output_folder, file_name_tiff)
fullCmd = 'gdalwarp -overwrite -s_srs "+proj=geos +lon_0=0 +h=35785831 +x_0=0 +y_0=0 +a=6378169 +b=6356583.8 +units=m +no_defs" -t_srs EPSG:4326 -te %d %d %d %d -of GTiff %s %s' %(lonlim[0], latlim[0], lonlim[1], latlim[1], output_GOES_projected, out_name)
process = subprocess.Popen(fullCmd)
process.wait() 

# Save data as Tiff
if os.path.exists(temp_folder):
    shutil.rmtree(temp_folder)    
